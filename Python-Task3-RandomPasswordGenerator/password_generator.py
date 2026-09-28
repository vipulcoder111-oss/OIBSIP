import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip


# ---------------- PASSWORD GENERATOR ----------------

def generate_password():

    try:
        length = int(length_spinbox.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid length.")
        return

    # Minimum length
    if length < 8:
        messagebox.showerror(
            "Error",
            "Password length must be at least 8 characters."
        )
        return

    # Selected character types
    selected_types = []

    if uppercase_var.get():
        selected_types.append(string.ascii_uppercase)

    if lowercase_var.get():
        selected_types.append(string.ascii_lowercase)

    if numbers_var.get():
        selected_types.append(string.digits)

    if symbols_var.get():
        selected_types.append(string.punctuation)

    # At least 2 types
    if len(selected_types) < 2:
        messagebox.showerror(
            "Error",
            "Please select at least 2 character types."
        )
        return

    # Ambiguous characters
    ambiguous = "0Ol1"

    if exclude_var.get():
        selected_types = [
            characters.replace("0", "")
                       .replace("O", "")
                       .replace("l", "")
                       .replace("1", "")
            for characters in selected_types
        ]

    # Make sure every selected type has characters
    selected_types = [
        characters for characters in selected_types
        if characters
    ]

    # Security rule:
    # At least one character from every selected type
    password_characters = []

    for characters in selected_types:
        password_characters.append(
            secrets.choice(characters)
        )

    # Create combined character set
    all_characters = "".join(selected_types)

    # Fill remaining characters
    remaining = length - len(password_characters)

    for i in range(remaining):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Secure shuffle
    secrets.SystemRandom().shuffle(password_characters)

    password = "".join(password_characters)

    # Display password
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    # Copy automatically
    pyperclip.copy(password)

    # Strength
    strength = calculate_strength(
        length,
        len(selected_types)
    )

    strength_label.config(
        text=f"Strength: {strength}"
    )

    # Add to history
    history.insert(0, password)

    # Keep only last 5
    if len(history) > 5:
        history.pop()

    update_history()


# ---------------- PASSWORD STRENGTH ----------------

def calculate_strength(length, types):

    if length >= 16 and types >= 3:
        return "Strong"

    elif length >= 12 and types >= 2:
        return "Medium"

    else:
        return "Weak"


# ---------------- COPY PASSWORD ----------------

def copy_password():

    password = password_entry.get()

    if password == "":
        messagebox.showerror(
            "Error",
            "Generate a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# ---------------- HISTORY ----------------

def update_history():

    history_text.delete(
        "1.0",
        tk.END
    )

    for number, password in enumerate(history, start=1):

        history_text.insert(
            tk.END,
            f"{number}. {password}\n"
        )


# ---------------- CLEAR ----------------

def clear_password():

    password_entry.delete(
        0,
        tk.END
    )

    strength_label.config(
        text="Strength: --"
    )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Random Password Generator")
root.geometry("550x700")


# ---------------- TITLE ----------------

title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=20)


# ---------------- LENGTH ----------------

length_label = tk.Label(
    root,
    text="Password Length",
    font=("Arial", 14)
)

length_label.pack()

length_spinbox = tk.Spinbox(
    root,
    from_=8,
    to=50,
    width=10,
    font=("Arial", 14)
)

length_spinbox.pack(pady=8)


# ---------------- CHARACTER TYPES ----------------

type_label = tk.Label(
    root,
    text="Select Character Types",
    font=("Arial", 14, "bold")
)

type_label.pack(pady=10)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)


uppercase_check = tk.Checkbutton(
    root,
    text="Uppercase Letters (A-Z)",
    variable=uppercase_var,
    font=("Arial", 12)
)

uppercase_check.pack()


lowercase_check = tk.Checkbutton(
    root,
    text="Lowercase Letters (a-z)",
    variable=lowercase_var,
    font=("Arial", 12)
)

lowercase_check.pack()


numbers_check = tk.Checkbutton(
    root,
    text="Numbers (0-9)",
    variable=numbers_var,
    font=("Arial", 12)
)

numbers_check.pack()


symbols_check = tk.Checkbutton(
    root,
    text="Symbols (!@#$...)",
    variable=symbols_var,
    font=("Arial", 12)
)

symbols_check.pack()


# ---------------- EXCLUDE AMBIGUOUS ----------------

exclude_var = tk.BooleanVar(value=False)

exclude_check = tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=exclude_var,
    font=("Arial", 12)
)

exclude_check.pack(pady=10)


# ---------------- PASSWORD ----------------

password_label = tk.Label(
    root,
    text="Generated Password",
    font=("Arial", 14, "bold")
)

password_label.pack(pady=10)


password_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=40
)

password_entry.pack(pady=5)


# ---------------- STRENGTH ----------------

strength_label = tk.Label(
    root,
    text="Strength: --",
    font=("Arial", 15, "bold")
)

strength_label.pack(pady=10)


# ---------------- BUTTONS ----------------

generate_button = tk.Button(
    root,
    text="Generate Password",
    font=("Arial", 13, "bold"),
    command=generate_password
)

generate_button.pack(pady=8)


copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    font=("Arial", 12),
    command=copy_password
)

copy_button.pack(pady=5)


clear_button = tk.Button(
    root,
    text="Clear",
    font=("Arial", 12),
    command=clear_password
)

clear_button.pack(pady=5)


# ---------------- HISTORY ----------------

history_label = tk.Label(
    root,
    text="Last 5 Generated Passwords",
    font=("Arial", 14, "bold")
)

history_label.pack(pady=10)


history_text = tk.Text(
    root,
    width=55,
    height=8
)

history_text.pack()


# ---------------- HISTORY LIST ----------------

history = []


# ---------------- START PROGRAM ----------------

root.mainloop()