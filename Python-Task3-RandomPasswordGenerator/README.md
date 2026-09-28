# 🔐 Random Password Generator

## 📌 Project Description

The Random Password Generator is a Python-based application that generates strong and secure passwords according to user-defined requirements.

The project is developed using **Python, Tkinter, Secrets, and Pyperclip**. It provides an easy-to-use graphical interface where users can select password length and character types such as uppercase letters, lowercase letters, numbers, and symbols.

The application also includes password strength checking, automatic clipboard copying, ambiguous character exclusion, and a session-based history of the last five generated passwords.

## ✨ Features

- 🔢 Set password length (minimum 8 characters)
- 🔠 Include uppercase letters
- 🔡 Include lowercase letters
- 🔢 Include numbers
- 🔣 Include symbols
- ✅ Requires at least two character types
- 🔐 Uses Python `secrets` module for secure password generation
- 💪 Password strength indicator
- 📋 Automatically copies generated password to clipboard
- 📋 Manual "Copy to Clipboard" option
- 🚫 Option to exclude ambiguous characters (`0`, `O`, `l`, `1`)
- 🕐 Stores the last 5 generated passwords during the current session
- 🔄 Generate multiple passwords without restarting the application
- ⚠️ Input validation and error messages

## 🛠️ Technologies Used

- Python
- Tkinter
- Secrets
- String
- Pyperclip

## 📂 Project Structure

```text
Python-Task3-RandomPasswordGenerator/
│
├── password_generator.py
├── README.md
│
└── screenshots/
    ├── 01-main.png
    ├── 02-generated-password.png
    ├── 03-validation.png
    ├── 04-copy.png
    └── 05-history.png
```
