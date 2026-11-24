import os
import threading
import time
import urllib.request
import webview
from server import app


class Api:
    """JS -> Python көпірі: тұтас экран және терезе өлшемі (pywebview)."""
    def __init__(self):
        self.window = None
        self.fs = False

    def set_fullscreen(self, on):
        on = bool(on)
        if self.window and on != self.fs:
            self.window.toggle_fullscreen()
            self.fs = on

    def set_size(self, w, h):
        if self.window and not self.fs:
            self.window.resize(int(w), int(h))


def run_server():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()

    for i in range(30):
        try:
            urllib.request.urlopen("http://127.0.0.1:5000")
            break
        except Exception:
            time.sleep(1)

    api = Api()
    api.window = webview.create_window(
        "Qairu Blackout", "http://127.0.0.1:5000",
        width=1280, height=720, js_api=api
    )
    # private_mode=False: баптаулар мен сақтаулар келесі іске қосуда жоғалмайды
    store = os.path.join(os.path.expanduser("~"), ".qairu_blackout")
    os.makedirs(store, exist_ok=True)
    webview.start(private_mode=False, storage_path=store)
