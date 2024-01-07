import time

import numpy as np
from mss import mss, tools
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract\tesseract.exe'
import mouse
import keyboard

from TarkovAPI import getItemInfo, getBestTrader

def TakeScreenshotAtMouse():
    print("Processing...")
    mousePos = mouse.get_position()
    with mss() as sct:
        # The screen part to capture
        mon = sct.monitors[1]
        monitor = {"top": mon["top"] + (mousePos[1]-10),
                   "left": mon["left"] + mousePos[0],
                   "width": (mousePos[0]+450) - mousePos[0],
                   "height": (mousePos[1]+20) - (mousePos[1]-10),
                   "mon": mon}

        # Grab the data
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        ocr = pytesseract.image_to_string(img)
        ocr_clean = " ".join(str(ocr).split(" ")[1:]).rstrip()
        item_info = getItemInfo(ocr_clean)
        if item_info == 0:
            return
        best_trader_info = getBestTrader(item_info)
        print(f"Name: {item_info['name']}")
        print(f"Short Name: {item_info['shortName']}")
        print(f"Flea Market 24h AVG: ₽{item_info['avg24hPrice']:,}")
        print(f"Best Trader: {best_trader_info['vendor']['name']}")
        print(f"Best Trader Price: ₽{best_trader_info['price']:,}")
        print("---------------------------------------------------")

def SaveScreenshot(sct_img):
    output = f"sct-{sct_img.top}x{sct_img.left}_{sct_img.width}x{sct_img.height}.png"
    tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

if __name__ == "__main__":
    print("Running")
    keyboard.add_hotkey('j', TakeScreenshotAtMouse)
    while not keyboard.is_pressed('k'):
        time.sleep(0.5)
    else:
        print("Quitting")