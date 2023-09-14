import pyttsx3
import sys
import speech_recognition as sr
import datetime
import psutil
import os
import subprocess
from Functionalities.writeOnFocusedTab import writeOnTab



engine = pyttsx3.init("sapi5")  # Initializing voice engine

voices = engine.getProperty("voices")

engine.setProperty("voice", voices[0].id)  # Set voice


# Text to Speak
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Take Command (Voice to Text)
def textcommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(
            source, timeout=5, phrase_time_limit=10
        )  # Listen for up to 5 seconds with a 10-second phrase time limit

    try:
        print("Processing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        speak("I can't understand ...")
        return "none"

    return query


# Greet Module (like: Good Morning)
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 11:
        speak("Good Morning Sir")
    elif hour > 15 and hour <= 17:
        speak("Good Afternoon Sir")
    else:
        speak("Hello Sir")

    speak("How may I help you")

# Check Weither App running
def is_app_running(app_name):
    app_name = app_name.lower()
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name'].lower()
            if app_name in process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Open Tab Function
def OpenAnotherTab(query):
    text_to_open = query.replace("open", "").replace("another", "").strip()
    speak(f"Opening {text_to_open}...")

    try:
        subprocess.Popen(text_to_open, shell=True)
    except Exception as e:
        speak(f"Sorry, I couldn't find {text_to_open}. Please make sure it's installed.")
        print(f"Error: {e}")
    return True

# Open Tab Function
def OpenTab(query):
    app_to_open = query.replace("open", "").strip()
    if is_app_running(app_to_open):
        return speak(f"{app_to_open} is already running ...")

    speak(f"Opening {app_to_open}...")

    try:
        subprocess.Popen(app_to_open, shell=True)
    except Exception as e:
        speak(f"Sorry, I couldn't find {app_to_open}. Please make sure it's installed.")
        print(f"Error: {e}")
    return True

# Close Tab Function
def CloseTab(query):
    app_name = query.replace("close", "").strip()
    speak(f"Closing {app_name} ...")

    try:
        subprocess.run(["taskkill", "/F", "/IM", app_name + ".exe"], check=True)
        return True 
    except subprocess.CalledProcessError as e:
        speak("Sorry, App is Not closed, Some error occured")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    wish()

    # Queries ---
    while True:
        query = textcommand().lower()

        if "exit" in query:
            speak("Bye Sir")
            break
        # Notepad 
        elif "open camera" in query:
            # path = "C:\\Windows\\system32\\notepad.exe"
            OpenTab(query)
        elif "open command prompt" in query:
            speak("Opening Command Prompt")
            subprocess.Popen(["cmd.exe", "/c", "dir"])
        elif "open" in query:
            # path = "C:\\Windows\\system32\\notepad.exe"
            OpenTab(query)
        elif "open another" in query:
            # path = "C:\\Windows\\system32\\notepad.exe"
            OpenAnotherTab(query)
        elif "write" in query:
            writeOnTab(query)
        elif "close notepad" in query:
            CloseTab(query)
        # Command Prompt
        else:
            None
