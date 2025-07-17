import speech_recognition as sr
import webbrowser
import pyttsx3
from difflib import get_close_matches
import sys
import musicliberary  # Your music dictionary file

# Speak function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Open websites
def open_site(url):
    webbrowser.open(url)

# Play song with fuzzy matching
def play_song_fuzzy(spoken_name):
    song_list = list(musicliberary.music.keys())
    match = get_close_matches(spoken_name, song_list, n=1, cutoff=0.5)
    if match:
        best_match = match[0]
        speak(f"Playing {best_match}")
        webbrowser.open(musicliberary.music[best_match])
    else:
        speak("Sorry, I couldn't find a song matching that name.")

# Site commands
site_commands = {
    "open google": lambda: open_site("http://google.com"),
    "open whatsapp": lambda: open_site("http://whatsapp.com"),
    "open youtube": lambda: open_site("http://youtube.com"),
    "open facebook": lambda: open_site("http://facebook.com"),
    "open instagram": lambda: open_site("http://instagram.com")
}

# Process commands including exit
def processCommand(c):
    c = c.lower().strip()

    if "exit" in c or "jarvis exit" in c:
        speak("Goodbye, Kaamil! Shutting down.")
        sys.exit()

    for phrase, action in site_commands.items():
        if phrase in c:
            action()
            return

    if c.startswith("play "):
        song_name = c[5:].strip()
        play_song_fuzzy(song_name)
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis... Say 'Jarvis' to start.")
    r = sr.Recognizer()

    # Wait for wake word
    while True:
        try:
            with sr.Microphone() as source:
                print("Waiting for 'Jarvis'...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
                wake = r.recognize_google(audio)

                if wake.lower() == "jarvis":
                    speak("Yes, I'm listening.")
                    break
        except Exception as e:
            print(f"Wake word error: {e}")

    # Jarvis active mode
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for command...")
                audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"Command: {command}")
                processCommand(command)
        except Exception as e:
            print(f"Command error: {e}")
