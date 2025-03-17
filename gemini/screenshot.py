import pyautogui
import time

def take_screenshot():
    time.sleep(3)
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return "screenshot.png"
