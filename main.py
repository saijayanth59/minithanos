import gemini
import spotify
from RealtimeSTT import AudioToTextRecorder


def process_input(text):
    if "play" in text.lower():
        spotify.play_song(text.lower().split("play")[1])


if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="en")
    while True:
        recorder.text(process_input)
