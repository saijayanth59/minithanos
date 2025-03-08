import pyautogui as pg
from time import sleep
import subprocess

def play_song(name):
    subprocess.run("spotify")
    sleep(2)
    pg.hotkey("ctrl", "k")
    pg.write(name)
    sleep(4)
    pg.hotkey("shift", "enter")
    pg.press("esc")
        
play_song("Die with a smile") 