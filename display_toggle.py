from pystray import Icon, MenuItem as Item, Menu
from PIL import Image
import requests
import threading
import datetime
import os
import sys
import json

if getattr(sys, 'frozen', False):
    # Compiled into an executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as a .py script
    BASE_DIR = os.path.dirname(__file__)

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
ICON_FILE = os.path.join(BASE_DIR, "icon.ico")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    URLS = json.load(f)

LOG_FILE = os.path.join(os.path.dirname(__file__), "error_log.txt")

def send_request(url):
    def _threaded():
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"✅ Successfully sent request to: {url}")
        except Exception as e:
            error_entry = f"[{datetime.datetime.now().isoformat()}] ❌ Failed to reach {url} — {str(e)}\n"
            print(error_entry.strip())
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(error_entry)
    threading.Thread(target=_threaded).start()

def make_items(side):
    def handler_factory(url):
        return lambda icon, item: send_request(url)

    return [Item(label, action=handler_factory(url)) for label, url in URLS[side].items()]

def create_menu():
    return Menu(
        Item('Left Display', Menu(*make_items('left'))),
        Item('Right Display', Menu(*make_items('right'))),
        Item('Quit', lambda icon, item: icon.stop())
    )

def create_icon():
    image = Image.open(ICON_FILE)
    return Icon("Display Input Switcher", image, "Display Switcher", create_menu())

if __name__ == '__main__':
    icon = create_icon()
    icon.run()
