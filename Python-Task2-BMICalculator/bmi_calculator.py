import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt


# ---------------- DATABASE ----------------

conn = sqlite3.connect("bmi.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT
)
""")

conn.commit()


# ---------------- CALCULATE BMI ----------------

def calculate():

    name = name_entry.get()
    weight = weight_entry.get()
    height = height_entry.get()

    # Check empty fields
    if name == "" or weight == "" or height == "":
        messagebox.showerror("Error", "Please fill all fields.")
        return

    # Convert weight and height to numbers
    try:
        weight = float(weight)
        height = float(height)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Weight and Height must be numbers."
        )
        return

    # Check positive values
    if weight <= 0 or height <= 0:
        messagebox.showerror(
            "Error",
            "Weight and Height must be greater than 0."
        )
        return

    # Calculate BMI
    bmi = weight / (height * height)

    # BMI category
    if bmi < 18.5:
        category = "Underweight"
        color = "orange"

    elif bmi < 25:
        category = "Normal"
        color = "green"

    elif bmi < 30:
        category = "Overweight"
        color = "orange"

    else:
        category = "Obese"
        color = "red"

    # Show result
    result.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        fg=color
    )

    # Save record in database
    cursor.execute(
        """
        INSERT INTO records
        (name, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, weight, height, bmi, category)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "BMI record saved successfully."
    )


# ---------------- VIEW HISTORY ----------------

def view_history():

    name = name_entry.get()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter your name."
        )
        return

    cursor.execute(
        "SELECT * FROM records WHERE name = ?",
        (name,)
    )

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "History",
            "No records found."
        )
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("600x400")

    title = tk.Label(
        history_window,
        text=f"BMI History - {name}",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=10)

    history_text = tk.Text(
        history_window,
        width=70,
        height=18
    )

    history_text.pack(padx=10, pady=10)

    for record in records:

        record_id = record[0]
        record_name = record[1]
        weight = record[2]
        height = record[3]
        bmi = record[4]
        category = record[5]

        history_text.insert(
            tk.END,
            f"ID: {record_id}\n"
            f"Name: {record_name}\n"
            f"Weight: {weight} kg\n"
            f"Height: {height} m\n"
            f"BMI: {bmi:.2f}\n"
            f"Category: {category}\n"
            f"{'-' * 40}\n"
        )

    history_text.config(state="disabled")


# ---------------- BMI TREND GRAPH ----------------

def show_graph():

    name = name_entry.get()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter your name."
        )
        return

    cursor.execute(
        "SELECT bmi FROM records WHERE name = ?",
        (name,)
    )

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "Graph",
            "No BMI records found."
        )
        return

    bmi_values = [record[0] for record in records]

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(1, len(bmi_values) + 1),
        bmi_values,
        marker="o"
    )

    plt.title(f"BMI Trend - {name}")
    plt.xlabel("Record")
    plt.ylabel("BMI")

    plt.axhline(
        y=18.5,
        linestyle="--",
        label="Underweight Limit"
    )

    plt.axhline(
        y=25,
        linestyle="--",
        label="Normal Limit"
    )

    plt.axhline(
        y=30,
        linestyle="--",
        label="Overweight Limit"
    )

    plt.legend()
    plt.grid(True)

    plt.show()


# ---------------- CLEAR FIELDS ----------------

def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result.config(
        text="BMI: --\nCategory: --",
        fg="black"
    )


# ---------------- GUI ----------------

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("500x600")

title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 25, "bold")
)

title.pack(pady=20)


# Name
name_label = tk.Label(
    root,
    text="Name",
    font=("Arial", 14)
)

name_label.pack()

name_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30
)

name_entry.pack(pady=5)


# Weight
weight_label = tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial", 14)
)

weight_label.pack()

weight_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30
)

weight_entry.pack(pady=5)


# Height
height_label = tk.Label(
    root,
    text="Height (meters)",
    font=("Arial", 14)
)

height_label.pack()

height_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30
)

height_entry.pack(pady=5)


# Calculate button
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 13, "bold"),
    command=calculate
)

calculate_button.pack(pady=15)


# Result
result = tk.Label(
    root,
    text="BMI: --\nCategory: --",
    font=("Arial", 18, "bold")
)

result.pack(pady=10)


# History button
history_button = tk.Button(
    root,
    text="View History",
    font=("Arial", 12),
    command=view_history
)

history_button.pack(pady=5)


# Graph button
graph_button = tk.Button(
    root,
    text="Show BMI Trend",
    font=("Arial", 12),
    command=show_graph
)

graph_button.pack(pady=5)


# Clear button
clear_button = tk.Button(
    root,
    text="Clear",
    font=("Arial", 12),
    command=clear_fields
)

clear_button.pack(pady=5)


# ---------------- START GUI ----------------

root.mainloop()


# ---------------- CLOSE DATABASE ----------------

conn.close()