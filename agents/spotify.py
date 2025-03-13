import pyautogui as pg
from time import sleep
import subprocess

def play_song(name: str) -> None:
    """
    Play a song on Spotify.
    Args:
        name (str): The name of the song.
    """
    subprocess.run("spotify")
    sleep(5)
    pg.hotkey("ctrl", "k")
    pg.write(name)
    sleep(4)
    pg.hotkey("shift", "enter")
    pg.press("esc")
    
if __name__ == '__main__':
    play_song("dancing with your ghost")