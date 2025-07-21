import speech_recognition as sr
import webbrowser
import pyttsx3
from difflib import get_close_matches
import sys
import musicliberary  # Your music dictionary file
import time

# ----------------------- Speech Functions -----------------------

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # Speed of speech
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose female voice; use [0] for male
    engine.say(text)
    engine.runAndWait()

# ----------------------- Helper Functions -----------------------

def open_site(url):
    webbrowser.open(url)
    speak(f"Opening {url.replace('http://', '').replace('www.', '')}")

def play_song_fuzzy(spoken_name):
    song_list = list(musicliberary.music.keys())
    match = get_close_matches(spoken_name.lower(), [s.lower() for s in song_list], n=1, cutoff=0.5)

    if match:
        for key in musicliberary.music:
            if key.lower() == match[0]:
                best_match = key
                break
        speak(f"Playing {best_match}")
        webbrowser.open(musicliberary.music[best_match])
    else:
        speak("Sorry, I couldn't find a matching song.")

# ----------------------- Website Shortcuts -----------------------

site_commands = {
    "open google": lambda: open_site("http://google.com"),
    "open youtube": lambda: open_site("http://youtube.com"),
    "open whatsapp": lambda: open_site("http://whatsapp.com"),
    "open facebook": lambda: open_site("http://facebook.com"),
    "open instagram": lambda: open_site("http://instagram.com")
}

# ----------------------- Command Processor -----------------------

def process_command(command):
    command = command.lower().strip()

    if "exit" in command or "shutdown" in command:
        speak("Goodbye, Kaamil! Shutting down.")
        sys.exit()

    for phrase, action in site_commands.items():
        if phrase in command:
            action()
            return

    if command.startswith("play "):
        song_name = command.replace("play ", "").strip()
        play_song_fuzzy(song_name)
    else:
        speak("Sorry, I didn't understand that command.")

# ----------------------- Voice Assistant -----------------------

def listen_for_input(prompt=""):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Sorry, there seems to be a connection issue.")
        return None

# ----------------------- Main Logic -----------------------

if __name__ == "__main__":
    speak("Initializing Jarvis... Say 'Jarvis' to wake me up.")

    # Wake word loop
    while True:
        wake_word = listen_for_input()
        if wake_word and "jarvis" in wake_word:
            speak("Yes Kaamil, I'm listening.")
            break

    # Command listening loop
    while True:
        user_command = listen_for_input("What can I do for you?")
        if user_command:
            process_command(user_command)
