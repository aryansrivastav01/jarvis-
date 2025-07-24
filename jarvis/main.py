# import speech_recognition as sr
# import webbrowser
# import pyttsx3
# import pocketsphinx
# import musiclibrary
# import googlesearch


# recognizer = sr.Recognizer()
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def processcommand(c):
#     try:
#         c = c.lower()
#         if "open google" in c:
#             webbrowser.open("https://www.google.com/")
#         elif "open youtube" in c:
#             webbrowser.open("https://www.youtube.com/")
#         elif c.startswith("play"):
#             song = c.split(" ", 1)[1]  # everything after 'play'
#             link = musiclibrary.music[song]
#             webbrowser.open(link)
#         elif c.startswith("search"):
#             sea = c.split(" ", 1)[1]
#             link2 = googlesearch.search[sea]
            
             
    
#     except Exception as e:
#         speak("Sorry, an error occurred while processing the command.")
#         print("Command processing error:", e)

# if __name__ == "__main__":
#     speak("Initializing Phoenix...")

#     r = sr.Recognizer()

#     while True:
#         try:
#             with sr.Microphone() as source:
#                 print("Listening for wake word...")
#                 audio = r.listen(source, timeout=2, phrase_time_limit=2)
#             word = r.recognize_google(audio)
#             print(word)

#             if word.lower() == "phoenix":
#                 speak("Ya")
#                 speak("Yes, I am here")

#                 with sr.Microphone() as source:
#                     print("Listening for command...")
#                     audio = r.listen(source)
#                     command = r.recognize_google(audio)
#                     print("Command received:", command)
#                     processcommand(command)

#         except Exception as e:
#             print("Listening error: {0}".format(e))
#             # Do NOT call processcommand(command) here — it might not exist yet

            
            
import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
import pocketsphinx
import musiclibrary
import googlesearch

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    t = threading.Thread(target=run)
    t.start()

def processcommand(c):
    try:
        c = c.lower()
        if "open google" in c:
            webbrowser.open("https://www.google.com/")
            speak("Opening Google")
        elif "open youtube" in c:
            webbrowser.open("https://www.youtube.com/")
            speak("Opening YouTube")
        elif c.startswith("play"):
            song = c.split(" ", 1)[1]
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                webbrowser.open(link)
                speak(f"Playing {song}")
            else:
                speak("Song not found in your library.")
        elif c.startswith("search"):
            query = c.split(" ", 1)[1]
            if query in googlesearch.search:
                link2 = googlesearch.search[query]
                webbrowser.open(link2)
                speak(f"Searching for {query}")
            else:
                speak("I couldn't find the search result.")
        else:
            speak("Sorry, I didn't understand that command.")
    except Exception as e:
        speak("Sorry, an error occurred while processing the command.")
        print("Command processing error:", e)

if __name__ == "__main__":
    speak("Initializing Phoenix...")

    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            word = r.recognize_google(audio)
            print("Wake word detected:", word)

            if word.lower() == "phoenix":
                speak("Yes, I am here")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print("Command received:", command)
                    processcommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results; check your internet connection.", e)
        except Exception as e:
            print("Listening error:", e)
