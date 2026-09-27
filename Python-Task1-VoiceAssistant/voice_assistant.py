import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import requests
import smtplib
import threading
import time
import os
import json

from urllib.parse import quote
from dotenv import load_dotenv

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.stem import WordNetLemmatizer


# ============================================================
# NLTK SETUP
# ============================================================

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


lemmatizer = WordNetLemmatizer()


# ============================================================
# LOAD PRIVATE INFORMATION FROM .ENV
# ============================================================

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# ============================================================
# SPEECH RECOGNITION
# ============================================================

r = sr.Recognizer()


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):

    print("Assistant:", text)

    engine = pyttsx3.init("sapi5")

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


# ============================================================
# NLTK NLP INTENT CLASSIFICATION
# ============================================================

training_data = [

    # ---------------- GREETING ----------------

    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("hello assistant", "greeting"),
    ("hey assistant", "greeting"),
    ("nice to meet you", "greeting"),

    # ---------------- TIME ----------------

    ("what time is it", "time"),
    ("tell me the time", "time"),
    ("can you tell me the current time", "time"),
    ("what is the current time", "time"),
    ("please tell me the time", "time"),
    ("do you know the time", "time"),

    # ---------------- DATE ----------------

    ("what is today's date", "date"),
    ("tell me today's date", "date"),
    ("what date is it", "date"),
    ("what is the current date", "date"),
    ("please tell me the date", "date"),

    # ---------------- WEATHER ----------------

    ("what is the weather", "weather"),
    ("tell me the weather", "weather"),
    ("how is the weather today", "weather"),
    ("what is the temperature", "weather"),
    ("tell me today's temperature", "weather"),
    ("is it hot today", "weather"),

    # ---------------- SEARCH ----------------

    ("search python", "search"),
    ("search for python", "search"),
    ("search something on google", "search"),
    ("look up python", "search"),
    ("find information about python", "search"),
    ("google python", "search"),

    # ---------------- EMAIL ----------------

    ("send an email", "email"),
    ("send email", "email"),
    ("please send an email", "email"),
    ("can you send an email", "email"),
    ("send an email for me", "email"),

    # ---------------- REMINDER ----------------

    ("set a reminder", "reminder"),
    ("remind me later", "reminder"),
    ("set a reminder for me", "reminder"),
    ("please set a reminder", "reminder"),
    ("i want to set a reminder", "reminder"),

    # ---------------- WEBSITES ----------------

    ("open youtube", "youtube"),
    ("launch youtube", "youtube"),

    ("open google", "google"),
    ("launch google", "google"),

    ("open github", "github"),
    ("launch github", "github"),

    ("open chatgpt", "chatgpt"),
    ("launch chatgpt", "chatgpt"),

    ("open instagram", "instagram"),
    ("launch instagram", "instagram"),

    ("open linkedin", "linkedin"),
    ("launch linkedin", "linkedin"),

    # ---------------- NAME ----------------

    ("what is your name", "name"),
    ("who are you", "name"),
    ("tell me about yourself", "name"),
    ("what are you", "name"),
    ("who is speaking", "name"),

    # ---------------- KNOWLEDGE ----------------

    ("what is python", "knowledge"),
    ("what is django", "knowledge"),
    ("what is github", "knowledge"),
    ("what is fastapi", "knowledge"),
    ("what is artificial intelligence", "knowledge"),
    ("tell me about python", "knowledge"),
    ("explain django", "knowledge"),
    ("tell me about github", "knowledge"),

    # ---------------- EXIT ----------------

    ("exit", "exit"),
    ("quit", "exit"),
    ("goodbye", "exit"),
    ("bye", "exit"),
    ("close assistant", "exit"),
    ("stop assistant", "exit")
]


# ============================================================
# TEXT PROCESSING
# ============================================================

def preprocess(sentence):

    words = nltk.word_tokenize(sentence.lower())

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word.isalnum()
    ]

    return words


# ============================================================
# CREATE TRAINING FEATURES
# ============================================================

def create_features(sentence):

    words = preprocess(sentence)

    return {
        word: True
        for word in words
    }


training_features = [
    (create_features(sentence), intent)
    for sentence, intent in training_data
]


# ============================================================
# TRAIN NLTK CLASSIFIER
# ============================================================

classifier = NaiveBayesClassifier.train(
    training_features
)


# ============================================================
# PREDICT INTENT
# ============================================================

def detect_intent(command):

    features = create_features(command)

    intent = classifier.classify(features)

    probability = classifier.prob_classify(features)

    confidence = probability.prob(intent)

    print("Detected Intent:", intent)
    print("Confidence:", round(confidence, 2))

    if confidence < 0.45:
        return "unknown"

    return intent


# ============================================================
# SEND EMAIL
# ============================================================

def send_email():

    try:

        message = """\
Subject: Voice Assistant Test

Hello,

This email was sent by my Python Voice Assistant.

Regards,
Vipul
"""

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            EMAIL_RECEIVER,
            message
        )

        server.quit()

        speak("Email sent successfully.")

    except Exception as e:

        print("Email Error:", e)

        speak(
            "Sorry, I could not send the email."
        )


# ============================================================
# REMINDER
# ============================================================

def reminder(seconds):

    time.sleep(seconds)

    print(
        "Reminder: Time is over."
    )

    speak(
        "Your reminder is ringing now."
    )


# ============================================================
# GET REMINDER TIME
# ============================================================

def get_seconds():

    speak(
        "For how many seconds should I set the reminder?"
    )

    try:

        with sr.Microphone(
            device_index=1
        ) as source:

            print(
                "Speak reminder time..."
            )

            r.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = r.listen(source)

        command = r.recognize_google(
            audio
        ).lower()

        print(
            "You:",
            command
        )

        numbers = {

            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,

            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60
        }

        for word, value in numbers.items():

            if word in command:

                return value

        for word in command.split():

            if word.isdigit():

                return int(word)

        return None

    except sr.UnknownValueError:

        speak(
            "I could not understand. "
            "Please repeat the reminder time."
        )

        return None

    except sr.RequestError:

        speak(
            "Speech recognition service is not available."
        )

        return None


# ============================================================
# GENERAL KNOWLEDGE
# ============================================================

def general_knowledge(command):

    if "python" in command:

        speak(
            "Python is a high level programming language "
            "used for web development, automation, data science "
            "and many other applications."
        )

        return True

    elif "django" in command:

        speak(
            "Django is a Python web framework used to build "
            "web applications."
        )

        return True

    elif "github" in command:

        speak(
            "GitHub is a platform used to store, manage and "
            "share software code."
        )

        return True

    elif "fastapi" in command:

        speak(
            "FastAPI is a modern Python framework used "
            "to build APIs."
        )

        return True

    elif (
        "artificial intelligence" in command
        or "ai" in command
    ):

        speak(
            "Artificial intelligence is technology that allows "
            "computers to perform tasks that normally require "
            "human intelligence."
        )

        return True

    return False


# ============================================================
# CONFIGURABLE CUSTOM COMMANDS
# ============================================================

COMMANDS_FILE = "commands.json"


def load_custom_commands():

    try:

        with open(
            COMMANDS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        print(
            "commands.json not found."
        )

        return {}

    except json.JSONDecodeError:

        print(
            "Invalid commands.json file."
        )

        return {}


def custom_commands(command):

    commands = load_custom_commands()

    command = command.lower().strip()

    for trigger, data in commands.items():

        if trigger.lower() in command:

            response = data.get(
                "response",
                "Opening custom command."
            )

            url = data.get("url")

            speak(response)

            if url:

                webbrowser.open(url)

            return True

    return False


# ============================================================
# START ASSISTANT
# ============================================================

speak(
    "Hello Vipul, I am your assistant."
)


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    try:

        with sr.Microphone(
            device_index=1
        ) as source:

            print(
                "\nSpeak..."
            )

            r.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = r.listen(source)

        # ----------------------------------------------------
        # VOICE TO TEXT
        # ----------------------------------------------------

        command = r.recognize_google(
            audio
        ).lower()

        print(
            "You:",
            command
        )

        # ----------------------------------------------------
        # CHECK CUSTOM COMMANDS FIRST
        # ----------------------------------------------------

        if custom_commands(command):

            continue

        # ----------------------------------------------------
        # NLP INTENT DETECTION
        # ----------------------------------------------------

        intent = detect_intent(command)

        # ====================================================
        # GREETING
        # ====================================================

        if intent == "greeting":

            speak(
                "Hello Vipul. How can I help you?"
            )

        # ====================================================
        # TIME
        # ====================================================

        elif intent == "time":

            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            speak(
                "The current time is "
                + current_time
            )

        # ====================================================
        # DATE
        # ====================================================

        elif intent == "date":

            current_date = datetime.datetime.now().strftime(
                "%d %B %Y"
            )

            speak(
                "Today's date is "
                + current_date
            )

        # ====================================================
        # WEATHER
        # ====================================================

        elif intent == "weather":

            city = "Udaipur"

            if not WEATHER_API_KEY:

                speak(
                    "Weather API key is not configured."
                )

            else:

                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city}"
                    f"&appid={WEATHER_API_KEY}"
                    "&units=metric"
                )

                response = requests.get(
                    url,
                    timeout=10
                )

                data = response.json()

                if response.status_code == 200:

                    temperature = data["main"]["temp"]

                    weather = data["weather"][0]["description"]

                    speak(
                        f"The temperature in {city} is "
                        f"{temperature} degrees Celsius "
                        f"with {weather}."
                    )

                else:

                    speak(
                        "Sorry, I could not get the weather."
                    )

        # ====================================================
        # SEARCH
        # ====================================================

        elif intent == "search":

            topic = command

            remove_words = [
                "search",
                "google",
                "look up",
                "find"
            ]

            for word in remove_words:

                topic = topic.replace(
                    word,
                    "",
                    1
                )

            topic = topic.strip()

            if topic:

                speak(
                    "Searching for "
                    + topic
                )

                search_url = (
                    "https://www.google.com/search?q="
                    + quote(topic)
                )

                webbrowser.open(
                    search_url
                )

            else:

                speak(
                    "Please tell me what you want to search."
                )

        # ====================================================
        # OPEN YOUTUBE
        # ====================================================

        elif intent == "youtube":

            speak(
                "Opening YouTube."
            )

            webbrowser.open(
                "https://www.youtube.com"
            )

        # ====================================================
        # OPEN GOOGLE
        # ====================================================

        elif intent == "google":

            speak(
                "Opening Google."
            )

            webbrowser.open(
                "https://www.google.com"
            )

        # ====================================================
        # OPEN GITHUB
        # ====================================================

        elif intent == "github":

            speak(
                "Opening GitHub."
            )

            webbrowser.open(
                "https://github.com"
            )

        # ====================================================
        # OPEN CHATGPT
        # ====================================================

        elif intent == "chatgpt":

            speak(
                "Opening ChatGPT."
            )

            webbrowser.open(
                "https://chatgpt.com"
            )

        # ====================================================
        # OPEN INSTAGRAM
        # ====================================================

        elif intent == "instagram":

            speak(
                "Opening Instagram."
            )

            webbrowser.open(
                "https://www.instagram.com"
            )

        # ====================================================
        # OPEN LINKEDIN
        # ====================================================

        elif intent == "linkedin":

            speak(
                "Opening LinkedIn."
            )

            webbrowser.open(
                "https://www.linkedin.com"
            )

        # ====================================================
        # NAME
        # ====================================================

        elif intent == "name":

            speak(
                "I am your Python voice assistant."
            )

        # ====================================================
        # SEND EMAIL
        # ====================================================

        elif intent == "email":

            if (
                not EMAIL_ADDRESS
                or not EMAIL_PASSWORD
                or not EMAIL_RECEIVER
            ):

                speak(
                    "Email settings are not configured."
                )

            else:

                speak(
                    "Sending email."
                )

                send_email()

        # ====================================================
        # REMINDER
        # ====================================================

        elif intent == "reminder":

            seconds = get_seconds()

            if seconds is not None:

                threading.Thread(
                    target=reminder,
                    args=(seconds,),
                    daemon=True
                ).start()

                speak(
                    f"Reminder set for {seconds} seconds."
                )

            else:

                speak(
                    "I could not set the reminder."
                )

        # ====================================================
        # GENERAL KNOWLEDGE
        # ====================================================

        elif intent == "knowledge":

            if not general_knowledge(command):

                speak(
                    "Sorry, I do not have an answer "
                    "for that question yet."
                )

        # ====================================================
        # EXIT
        # ====================================================

        exit_commands = [
                                "exit",
                               "quit",
                              "goodbye",
                                "bye",
                                "close assistant",
                                "stop assistant"
                   ]

        if command in exit_commands:
                 speak("Goodbye Vipul. Have a nice day.")
                 break

        # ====================================================
        # UNKNOWN COMMAND
        # ====================================================

        else:

            speak(
                "Sorry, I could not understand that. "
                "Please repeat your command."
            )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except sr.UnknownValueError:

        speak(
            "Sorry, I could not understand your voice. "
            "Please repeat."
        )

    except sr.RequestError:

        speak(
            "Speech recognition service is not available."
        )

    except Exception as e:

        print(
            "Error:",
            e
        )

        speak(
            "Sorry, something went wrong."
        )