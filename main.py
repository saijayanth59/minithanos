import pyttsx3
from time import sleep
import gemini
import speech_recognition as sr


engine = pyttsx3.init()
engine.setProperty('volume', 1)
engine.setProperty('rate', 150)

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    while True:
        print("Say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_whisper(audio)
            response = gemini.model.generate_content(text)
            for chunk in response:
                engine.say(chunk.text)
                print(chunk.text)
                engine.runAndWait()
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Error with the speech recognition service")
        except Exception as e:
            print("Error:", e)
