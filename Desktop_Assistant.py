"""Desktop Assistant a.k.a JARVIS, an interactive python code to send emails without
typing a single word, doing Wikipedia searches without opening web browsers,
and performing many other daily tasks like playing music with the help of a single voice command."""

import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import googlesearch as gs
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # add any voice available in your system


def send_email(receiver, message):
    """send out an email to the receiver by recognizing the voice input"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')  # add your email address and password
    server.sendmail('youremail@gmail.com', receiver, message)  # add your email address
    server.close()


def speak(audio):
    """Says out the given input"""
    engine.say(audio)  # speaks the passed audio
    engine.runAndWait()


def wish_me():
    """Wishes the user upon execution"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am JARVIS, Please tell me how may I help you?")


def take_command():
    """It takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query_inp = r.recognize_google(audio, language='en-in')
        print("User said:", query_inp)

    except Exception as exp:
        f = open("error.txt", "a")  # stores error if any
        f.write(str(exp))
        f.close()
        print("Say that again please!")
        return "None"
    return query_inp


if __name__ == '__main__':
    wish_me()
    while True:
        query = take_command().lower()
        # Logic for tasks based on query
        if 'wikipedia' in query:  # search wikipedia
            print("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:  # open youtube
            webbrowser.open("youtube.com")

        elif 'open google' in query:  # open google
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:  # open stackoverflow
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:  # play music from your added directory
            music_dir = 'D:\\songs'  # add your specific directory
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'open calculator' in query:  # open calculator
            calc_path = 'C:\\Windows\\system32\\calc.exe'  # add your specific directory
            os.startfile(calc_path)

        elif 'open pycharm' in query:  # open the python code editor
            # add your specific directory
            pycharm_path = 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.3.3\\bin\\pycharm64.exe'
            os.startfile(pycharm_path)

        elif 'the time' in query:  # tells the time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  # current time
            speak(f"Sir, the time is {strTime}")

        elif 'email to name' in query:  # sends an e-mail
            try:
                speak("What should I say?")
                content = take_command()  # take the message from voice input
                to = "name@gmail.com"
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                fp = open("error.txt", "a")  # stores error if any
                fp.write(str(e))
                fp.close()
                speak("Sorry Sir, I am not able to send this email")

        elif 'shutdown' in query:  # exit the program
            print("BYE sir, Have a good day!")
            speak("BYE sir, Have a good day!")
            exit()

        else:  # perform google search if no case match
            try:
                for j in gs.search(query, tld="co.in", num=5, stop=5, pause=2):
                    print(j)
            except Exception as e:
                file = open("error.txt", "a")  # stores error if any
                file.write(str(e))
                file.close()
                print("No request match!")
                speak("No request match!")
