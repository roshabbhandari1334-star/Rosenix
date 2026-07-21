"""
J.A.R.V.I.S. AI OS Launcher
Boots the FastAPI backend server and launches the standalone Desktop Window UI.
"""

import sys
import os
import time
import threading
import webbrowser
import uvicorn

# Add current project root directory to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config.settings import settings

def start_backend_server():
    """Runs Uvicorn FastAPI Server"""
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, log_level="warning")

def main():
    print("=" * 60)
    print("           ROSENIX AI OS INTERFACE INITIATING           ")
    print("=" * 60)

    # 1. Start FastAPI server in background thread
    server_thread = threading.Thread(target=start_backend_server, daemon=True)
    server_thread.start()

    # Wait 1.5 seconds for FastAPI server port to open
    time.sleep(1.5)
    app_url = f"http://{settings.HOST}:{settings.PORT}"
    print(f"[Rosenix Backend] Server live at {app_url}")

    # 2. Try launching pywebview Desktop Window
    try:
        import webview
        print("[Rosenix UI] Launching Native Desktop Window via PyWebView...")
        window = webview.create_window(
            title="Rosenix AI OS",
            url=app_url,
            width=1280,
            height=850,
            min_size=(900, 600),
            resizable=True,
            background_color='#050811'
        )
        webview.start(gui='auto', debug=False)
    except Exception as e:
        print(f"[JARVIS UI Notice] Desktop window wrapper note ({e}). Falling back to App Mode Browser Window...")
        webbrowser.open(app_url)
        print("[JARVIS UI] Running J.A.R.V.I.S. Interface in App Mode Window.")
        # Keep main thread alive while backend thread runs
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[JARVIS System] Shutting down J.A.R.V.I.S. AI OS...")

if __name__ == "__main__":
    main()
