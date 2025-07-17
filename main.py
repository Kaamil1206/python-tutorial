import speech_recognition as sr
import webbrowser
import pyttsx3
import musicliberary

# Speak text using pyttsx3
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Action functions
def open_site(url):
    webbrowser.open(url)

def play_song(song):
    link = musicliberary.music.get(song)
    if link:
        webbrowser.open(link)
    else:
        speak(f"I couldn't find the song {song}")

# Command dictionary
command_map = {
    "open google": lambda: open_site("http://google.com"),
    "open whatsapp": lambda: open_site("http://whatsapp.com"),
    "open youtube": lambda: open_site("http://youtube.com"),
    "open facebook": lambda: open_site("http://facebook.com"),
    "open instagram": lambda: open_site("http://instagram.com"),
}

# Command processing
def processCommand(c):
    c = c.lower()

    for trigger, action in command_map.items():
        if trigger in c:
            action()
            return

    if c.startswith("play "):
        song = c.split(" ", 1)[1]
        play_song(song)
    else:
        speak("Sorry, I didn't understand that command.")

# Main function
if __name__ == "__main__":
    speak("Initializing Jarvis... Say 'Jarvis' to start.")

    r = sr.Recognizer()

    # Step 1: Wait for wake word once
    while True:
        try:
            with sr.Microphone() as source:
                print("Waiting for 'Jarvis'...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes, I'm listening.")
                break  # Exit wake word loop

        except Exception as e:
            print(f"Wake word error: {e}")

    # Step 2: Continuous command mode (Jarvis is active)
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
