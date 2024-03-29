import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from selenium import webdriver

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("Speech recognition timed out. Please try again.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return "None"

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('', '')
    server.sendmail('', to, content)
    server.close()


def is_email_intent(query):
    email_keywords = ['send email', 'email', 'compose email']
    for keyword in email_keywords:
        if keyword in query:
            return True
    return False


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if is_email_intent(query):
            try:
                speak("Who do you want to send the email to?")
                recipient = takeCommand()

                speak("What should I say in the email?")
                content = takeCommand()

                sendEmail(recipient, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e,"Sorry. I am not able to send this email.")
                speak("Sorry. I am not able to send this email.")

        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\\vs codes\\project 1.txt"
            os.startfile(codePath)

        elif 'open' in query:
            # Extract the website name from the user's command
            website_name = query.replace('open', '').strip()

            # Add the protocol (http:// or https://) if missing
            if not website_name.startswith(('http://', 'https://')):
                website_names = 'https://' + website_name + '.com'

                website_url = website_names
                browser = webdriver.Edge()  # You may need to download the ChromeDriver executable
                browser.get(website_url)

        elif 'exit' in query:
            break
