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
    time.sleep(5)  
    url = f"http://localhost:{port}"
    
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=2)
            break 
        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(1)
            else:
                print("Server not responding, but trying to open browser...")
    
    success = False
    
    try:
        webbrowser.open(url)
        print(f"Browser opened automatically: {url}")
        success = True
    except Exception as e:
        print(f"webbrowser method failed: {e}")
        
    if not success and os.name == 'nt': 
        try:
            subprocess.run(['cmd', '/c', 'start', '', url], check=False, shell=False)
            print("✓ Trying to open with Windows start command...")
            success = True
        except Exception as e1:
            try:
                subprocess.run(['powershell', '-Command', f'Start-Process "{url}"'], 
                             check=False, shell=False)
                print("✓ Trying to open with PowerShell...")
                success = True
            except Exception as e2:
                try:
                    os.system(f'start "" "{url}"')
                    print("✓ Trying with os.system...")
                    success = True
                except Exception as e3:
                    print(f"All methods failed: {e1}, {e2}, {e3}")
    
    if not success:
        print(f"IMPORTANT: Open manually in your browser: {url}")
        print("   Copy and paste this URL in your preferred browser.")


def setup_config():
    config_path = REAL_BASE_DIR / "config.ini"

    if not config_path.exists():
        print("\n=== Initial configuration ===")
        print("To use this application you need an OpenRouter API key.")
        print("You can get one at: https://openrouter.ai/keys\n")

        api_key = input("Enter your OpenRouter API key: ").strip()

        with open(config_path, "w") as f:
            f.write(f"[API]\n")
            f.write(f"OPENROUTER_API_KEY={api_key}\n")

        print(" Configuration saved\n")

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
            print("Running from packaged executable")
        else:
            print("Running from source code")

        setup_config()

        port = find_free_port()
        if not port:
            print("ERROR: Could not find an available port")
            input("Press Enter to exit...")
            sys.exit(1)

        print(f"Port found: {port}")
        print(f"The application will be available at: http://localhost:{port}")
        print(f"Preparing Flask...")

        os.environ["FLASK_PORT"] = str(port)

        sys.path.insert(0, str(BASE_DIR))
        sys.path.insert(0, str(BASE_DIR / "src"))

        os.chdir(BASE_DIR)

        try:
            from app_wrapper import app
            print("Using optimized configuration for packaging")
        except ImportError as e:
            print(f"app_wrapper import failed: {e}")
            try:
                from app import app
                print("Using original app.py")
            except ImportError as e2:
                print(f"ERROR: Could not import app_wrapper or app: {e2}")
                input("Press Enter to exit...")
                sys.exit(1)

        app.config["SECRET_KEY"] = "secret-bot-kla"

        print("Starting thread to open browser...")
        browser_thread = threading.Thread(target=open_browser, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()

        print(f"\nFLASK SERVER STARTING ON PORT: {port}")
        print(f"FULL URL: http://localhost:{port}")
        print("\n Available routes:")
        print(f"   - Individual analysis: http://localhost:{port}/")
        print(f"   - Batch processing: http://localhost:{port}/batch")
        print("\nTo stop the server, close this window or press Ctrl+C.")
        print("\n" + "="*60)
        if getattr(sys, "frozen", False):
            print("WINDOWS EXECUTABLE - INSTRUCTIONS:")
            print("   • The browser should open automatically")
            print("   • If it doesn't open, Windows may be blocking it")
            print("   • Solution: Copy this URL manually:")
        else:
            print("If the browser did not open automatically:")
            print("   Copy this URL into your browser:")
        print(f" http://localhost:{port}")
        print("="*60 + "\n")

        try:
            print("STARTING FLASK SERVER...")
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
        except Exception as e:
            print(f"ERROR STARTING SERVER: {e}")
            input("Press Enter to exit...")
        except KeyboardInterrupt:
            print("\n\nServer stopped correctly")
            time.sleep(1)
            
    except Exception as e:
        print(f"ERROR IN MAIN: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nFull error details:")
        traceback.print_exc()
        print("\n" + "="*50)
        print("Press Enter to close...")
        input()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        input("Press Enter to close...")
