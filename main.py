import speech_recognition as sr
import webbrowser
import pyttsx3
from difflib import get_close_matches
import sys
import musicliberary  # Your music dictionary file
import time
import openai
import json
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your API Key

# ----------------------- Playlist URL -----------------------

playlist_url = "https://open.spotify.com/playlist/7q1sJnepIBWPhECLW2lS2O?si=f06aba68f5ec4ade"

# ----------------------- Speech Functions -----------------------

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
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

def play_playlist():
    speak("Playing your playlist.")
    webbrowser.open(playlist_url)

# ----------------------- Memory System -----------------------

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)

memory = load_memory()

def remember_user_name(command):
    if "my name is" in command:
        name = command.split("my name is")[-1].strip().capitalize()
        memory["name"] = name
        save_memory(memory)
        speak(f"Nice to meet you, {name}!")

def identify_user():
    name = memory.get("name")
    if name:
        speak(f"Welcome back, {name}!")
    else:
        speak("Hi, I don't know your name yet. Please tell me by saying 'My name is ...'")

# ----------------------- OpenAI ChatGPT -----------------------

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Jarvis."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        speak(answer)
    except Exception as e:
        speak("Sorry, I couldn't connect to ChatGPT right now.")
        print("OpenAI error:", e)

# ----------------------- NLP Interpreter -----------------------

def interpret_command(command):
    doc = nlp(command)
    
    if "playlist" in command and "play" in command:
        return "play_playlist", None

    if any(token.lemma_ == "play" for token in doc):
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ in ["dobj", "pobj"]:
                return "play_song", chunk.text

    if "open" in command:
        for site in site_commands:
            if site.replace("open ", "") in command:
                return "open_site", site

    if "name" in command and "my" in command:
        return "remember_name", command

    return "chat", command

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
    task, value = interpret_command(command)
    if task == "play_song":
        play_song_fuzzy(value)
    elif task == "play_playlist":
        play_playlist()
    elif task == "open_site":
        site_commands[value]()
    elif task == "remember_name":
        remember_user_name(value)
    elif task == "chat":
        chat_with_gpt(value)

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
            identify_user()
            break

    # Command listening loop
    while True:
        user_command = listen_for_input("What can I do for you?")
        if user_command:
            process_command(user_command)
            if "exit" in user_command or "quit" in user_command:
                speak("Goodbye!")
                sys.exit()