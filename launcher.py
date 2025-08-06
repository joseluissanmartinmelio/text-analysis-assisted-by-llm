import webbrowser
import time
import socket
import sys
import os
import threading
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


def find_free_port(start_port=5000):
    port = start_port
    while port < 65535:
        if check_port(port):
            return port
        port += 1
    return None


def open_browser(port):
    time.sleep(2)
    webbrowser.open(f"http://localhost:{port}")


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
    print(
        """
    ╔════════════════════════════════════════════╗
    ║     Llm assistant by José San Martin       ║
    ╚════════════════════════════════════════════╝
    """
    )

    setup_config()

    port = find_free_port()
    if not port:
        print("Could not find an available port")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"Starting server on port {port}...")

    os.environ["FLASK_PORT"] = str(port)

    sys.path.insert(0, str(BASE_DIR))
    sys.path.insert(0, str(BASE_DIR / "src"))

    os.chdir(BASE_DIR)

    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()

    try:
        from app_wrapper import app

        print("Using optimized configuration for packaging")
    except ImportError:
        from app import app

        print("Using original app.py")

    app.config["SECRET_KEY"] = "secret-bot-kla"

    print(f"\n Application running on: http://localhost:{port}")
    print("\n Available routes:")
    print(f"   - Individual analysis: http://localhost:{port}/")
    print(f"   - Batch processing: http://localhost:{port}/batch")
    print("\nTo stop the server, close this window or press Ctrl+C.\n")

    try:
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n Server stopped correctly")
        time.sleep(1)


if __name__ == "__main__":
    main()
