from RealtimeSTT import AudioToTextRecorder
from agents.god import do


def process_input(text):
    if "gemini" in text.lower():
        print(text)
        print(do(text))


if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="en", spinner=False)
    while True:
        recorder.text(process_input)
