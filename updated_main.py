import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize recognizer and pyttsx3
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your NewsAPI Key Here>"

# Initialize Pygame once
pygame.init()
pygame.mixer.init()

# OpenAI API client setup (avoid hardcoding in production)
client = OpenAI(api_key="use your own api key ")  # Replace with env variable or config securely

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        print(f"Speech Error: {e}")

def aiProcess(command):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks. Keep responses short."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Sorry, I couldn't connect to OpenAI."

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                for article in articles[:5]:  # Limit to 5 headlines
                    speak(article['title'])
            else:
                speak("Sorry, couldn't fetch news at the moment.")
        except:
            speak("Network error while fetching news.")
    else:
        speak(aiProcess(c))

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio).lower()

            if word == "jarvis":
                speak("Yes")
                with sr.Microphone() as source:
                    print("Jarvis Active. Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.WaitTimeoutError:
            pass  # Normal timeout
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Network issue with speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
