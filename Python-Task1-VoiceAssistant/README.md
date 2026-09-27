# 🎙️ Jarvis AI – Python Voice Assistant

<p align="center">
  <b>Oasis Infobyte Internship | Python Programming | Task 1</b>
</p>

<p align="center">
  A Python-based voice assistant that listens to spoken commands,
  processes user requests, and performs useful tasks through voice interaction.
</p>

---

## 📌 Project Overview

**Jarvis AI** is a Python-based voice assistant developed as part of the
**Oasis Infobyte Python Programming Internship – Task 1**.

The project combines speech recognition, text-to-speech, web automation,
API integration, email automation, reminders, custom commands, and
basic natural-language intent processing.

The assistant listens to commands through a microphone, converts speech
into text, identifies the requested action, performs the task, and provides
a spoken response to the user.

---

## ✨ Key Features

### 🎤 Voice Input

- Captures voice commands through a microphone.
- Uses the `SpeechRecognition` library.
- Automatically adjusts for ambient noise.
- Converts spoken commands into text.

---

### 🔊 Text-to-Speech

- Uses `pyttsx3` for voice responses.
- Uses Windows `SAPI5` speech engine.
- Provides spoken feedback for assistant responses.
- Displays assistant responses in the terminal.

---

### 🧠 Intent Recognition

The assistant processes user commands and identifies different
types of requests such as:

- Greeting
- Time
- Date
- Weather
- Search
- Email
- Reminder
- Website opening
- General knowledge
- Exit commands

The project uses NLP-related processing with NLTK and intent-based
command handling.

---

### 🕐 Time & Date

The assistant can provide:

- Current time
- Current date

Example commands:

```text
What is the time?
What is today's date?
```
