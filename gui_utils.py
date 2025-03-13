import pyautogui as pg
import pyperclip

def write_text(text):
    for line in text.split("\n"):
        pg.hotkey("home")
        pyperclip.copy(line)
        pg.hotkey("ctrl", "v")
        pg.press("enter")

def press_shortcut(shortcut):
    pg.hotkey(*shortcut)