from pystray import Icon, MenuItem as Item, Menu
from PIL import Image
import requests
import threading
import datetime
import os
import sys
import json

# Determine base directory depending on whether we're running from source or a compiled executable
if getattr(sys, "frozen", False):
    # Running as a compiled executable (e.g. via PyInstaller --onefile)
    BASE_DIR = sys._MEIPASS
    CONFIG_PATH = os.path.dirname(sys.executable)
else:
    # Running as a .py script
    BASE_DIR = os.path.dirname(__file__)
    CONFIG_PATH = BASE_DIR

CONFIG_FILE = os.path.join(CONFIG_PATH, "config.json")
ICON_FILE = os.path.join(BASE_DIR, "icon.ico")
LOG_FILE = os.path.join(CONFIG_PATH, "error_log.txt")

# Load URLs from config file
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    URLS = json.load(f)


def send_request(url):
    def _threaded():
        try:
            if type(url) is str:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                print(f"✅ Successfully sent request to: {url}")
            elif type(url) is list:
                for i in url:
                    response = requests.get(i, timeout=5)
                    response.raise_for_status()
                    print(f"✅ Successfully sent request to: {i}")
        except Exception as e:
            error_entry = f"[{datetime.datetime.now().isoformat()}] ❌ Failed to reach {url} — {str(e)}\n"
            print(error_entry.strip())
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(error_entry)

    threading.Thread(target=_threaded).start()


def make_items(side):
    def handler_factory(url):
        return lambda icon, item: send_request(url)

    return [
        Item(label, action=handler_factory(url)) for label, url in URLS[side].items()
    ]


def make_button(side):
    return lambda icon, item: send_request(URLS[side])


def create_menu():
    return Menu(
        Item("Left Display", Menu(*make_items("left"))),
        Item("Center", Menu(*make_items("center"))),
        Item("Right Display", Menu(*make_items("right"))),
        Item("MacBook", make_button("mac")),
        Item("Quit", lambda icon, item: icon.stop()),
    )


def create_icon():
    image = Image.open(ICON_FILE)
    return Icon("Display Input Switcher", image, "Display Switcher", create_menu())


if __name__ == "__main__":
    icon = create_icon()
    icon.run()
