import os
from dotenv import load_dotenv
from RealtimeSTT import AudioToTextRecorder
import elevenlabs
from agents.god import do

load_dotenv()


def process_input(text):
    if "gemini" in text.lower():
        print(text)
        response = do(text)
        print(response)
        audio = client.generate(
            voice="Jessica",
            voice_settings=elevenlabs.VoiceSettings(
                use_speaker_boost=True,
                speed=1,
                stability=0.5,
                similarity_boost=0.7,
                style=0.3,
            ),
            text=response,
            model="eleven_flash_v2_5"
        )
        elevenlabs.play(audio)


if __name__ == "__main__":
    client = elevenlabs.ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    recorder = AudioToTextRecorder(language="en", spinner=True)
    while True:
        text = recorder.text()
        process_input(text)
        recorder.stop()
