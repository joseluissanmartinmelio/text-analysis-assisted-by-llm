import webbrowser
import time
import socket
import sys
import os
import threading
import subprocess
import urllib.request
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
    REAL_BASE_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).parent
    REAL_BASE_DIR = BASE_DIR


def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("127.0.0.1", port))
    sock.close()
    return result != 0


def find_free_port(start_port=8000):
    port = start_port
    while port < 65535:
        if check_port(port):
            return port
        port += 1
    return None


def open_browser(port):
    # Esperar más tiempo para que Flask esté completamente iniciado
    time.sleep(5)  
    url = f"http://localhost:{port}"
    
    # Verificar que el servidor esté realmente funcionando antes de abrir navegador
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=2)
            break  # Servidor está listo
        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(1)  # Esperar 1 segundo más
            else:
                print("⚠ Servidor no responde, pero intentando abrir navegador...")
    
    success = False
    
    try:
        # Intentar abrir con webbrowser estándar
        webbrowser.open(url)
        print(f"✓ Navegador abierto automáticamente: {url}")
        success = True
    except Exception as e:
        print(f"⚠ Método webbrowser falló: {e}")
        
    # En Windows, intentar comandos alternativos si el primero falló
    if not success and os.name == 'nt':  # Windows
        try:
            # Método 1: start con URL directa
            subprocess.run(['cmd', '/c', 'start', '', url], check=False, shell=False)
            print("✓ Intentando abrir con comando Windows start...")
            success = True
        except Exception as e1:
            try:
                # Método 2: powershell
                subprocess.run(['powershell', '-Command', f'Start-Process "{url}"'], 
                             check=False, shell=False)
                print("✓ Intentando abrir con PowerShell...")
                success = True
            except Exception as e2:
                try:
                    # Método 3: usando os.system como último recurso
                    os.system(f'start "" "{url}"')
                    print("✓ Intentando con os.system...")
                    success = True
                except Exception as e3:
                    print(f"⚠ Todos los métodos fallaron: {e1}, {e2}, {e3}")
    
    if not success:
        print(f"📌 IMPORTANTE: Abre manualmente en tu navegador: {url}")
        print("   Copia y pega esta URL en tu navegador preferido.")


def setup_config():
    config_path = REAL_BASE_DIR / "config.ini"

    if not config_path.exists():
        print("\n=== Initial condiguration ===")
        print("To use this application you need an OpenRouter API key.")
        print("You can get one at: https://openrouter.ai/keys\n")

        api_key = input("Enter your OpenRouter API key: ").strip()

        with open(config_path, "w") as f:
            f.write(f"[API]\n")
            f.write(f"OPENROUTER_API_KEY={api_key}\n")

        print(" Saved configuration\n")

    with open(config_path, "r") as f:
        for line in f:
            if "OPENROUTER_API_KEY" in line:
                key = line.split("=")[1].strip()
                os.environ["OPENROUTER_API_KEY"] = key
                break


def main():
    try:
        is_packaged = getattr(sys, "frozen", False)
        
        print(
            """
        ╔════════════════════════════════════════════╗
        ║     Llm assistant by José San Martin       ║
        ╚════════════════════════════════════════════╝
        """
        )
        
        if is_packaged:
            print("🔧 Ejecutando desde ejecutable empaquetado")
        else:
            print("🔧 Ejecutando desde código fuente")

        setup_config()

        port = find_free_port()
        if not port:
            print("❌ ERROR: Could not find an available port")
            input("Press Enter to exit...")
            sys.exit(1)

        print(f"✅ Puerto encontrado: {port}")
        print(f"🌐 La aplicación estará disponible en: http://localhost:{port}")
        print(f"⏳ Preparando Flask...")

        os.environ["FLASK_PORT"] = str(port)

        sys.path.insert(0, str(BASE_DIR))
        sys.path.insert(0, str(BASE_DIR / "src"))

        os.chdir(BASE_DIR)

        try:
            from app_wrapper import app
            print("✓ Using optimized configuration for packaging")
        except ImportError as e:
            print(f"⚠ app_wrapper import failed: {e}")
            try:
                from app import app
                print("✓ Using original app.py")
            except ImportError as e2:
                print(f"❌ ERROR: No se pudo importar ni app_wrapper ni app: {e2}")
                input("Press Enter to exit...")
                sys.exit(1)

        app.config["SECRET_KEY"] = "secret-bot-kla"

        print("🌐 Iniciando hilo para abrir navegador...")
        browser_thread = threading.Thread(target=open_browser, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()

        print(f"\n🚀 SERVIDOR FLASK INICIANDO EN PUERTO: {port}")
        print(f"📍 URL COMPLETA: http://localhost:{port}")
        print("\n Available routes:")
        print(f"   - Individual analysis: http://localhost:{port}/")
        print(f"   - Batch processing: http://localhost:{port}/batch")
        print("\nTo stop the server, close this window or press Ctrl+C.")
        print("\n" + "="*60)
        if getattr(sys, "frozen", False):
            print("🖥️  EJECUTABLE WINDOWS - INSTRUCCIONES:")
            print("   • El navegador debería abrirse automáticamente")
            print("   • Si no se abre, Windows puede estar bloqueándolo")
            print("   • Solución: Copia esta URL manualmente:")
        else:
            print("🌐 Si el navegador no se abrió automáticamente:")
            print("   Copia esta URL en tu navegador:")
        print(f"   👉 http://localhost:{port}")
        print("="*60 + "\n")

        try:
            print("🔥 INICIANDO SERVIDOR FLASK...")
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
        except Exception as e:
            print(f"❌ ERROR AL INICIAR SERVIDOR: {e}")
            input("Press Enter to exit...")
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped correctly")
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ ERROR EN MAIN: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        print("\nDetalle completo del error:")
        traceback.print_exc()
        print("\n" + "="*50)
        print("Presiona Enter para cerrar...")
        input()
    except KeyboardInterrupt:
        print("\n✅ Aplicación cerrada por el usuario")
        input("Presiona Enter para cerrar...")
