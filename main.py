import speech_recognition as sr
import webbrowser
import pyttsx3
import musicliberary

# Function to make Jarvis speak
def speak(text):
    engine = pyttsx3.init()  # ✅ Moved inside the function
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("http://whatsapp.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("http://instagram.com")
# Main program
if __name__ == "__main__":
    speak("Initializing Jarvis....")

    while True:
        # Listen for the wake word "Jarvis"
        r = sr.Recognizer()

        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)

            if (word.lower() == "jarvis"):
                speak("Ya")  # ✅ This will now work

                # Listen For command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)  # ✅ Also fixed the missing argument

        except Exception as e:
            print("error; {0}".format(e))
