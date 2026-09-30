import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
from dotenv import load_dotenv
import os


# ---------------- LOAD API KEY ----------------

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


# ---------------- SETTINGS ----------------

current_unit = "C"


# ---------------- GET WEATHER ----------------

def get_weather():

    city = city_entry.get().strip()

    # Empty city validation
    if city == "":
        show_error("Please enter a city name.")
        return

    if not API_KEY:
        show_error("API key is missing.")
        return

    try:

        # Current weather API
        current_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        current_response = requests.get(
            current_url,
            timeout=10
        )

        current_data = current_response.json()

        # Check API error
        if current_response.status_code != 200:

            if current_response.status_code == 404:
                show_error("City not found. Please check the city name.")

            elif current_response.status_code == 401:
                show_error("Invalid API key.")

            else:
                show_error(
                    current_data.get(
                        "message",
                        "Unable to get weather."
                    )
                )

            return

        # Current weather information
        temperature = current_data["main"]["temp"]
        humidity = current_data["main"]["humidity"]
        weather = current_data["weather"][0]["description"]
        wind = current_data["wind"]["speed"]
        icon = current_data["weather"][0]["icon"]

        # Display current weather
        city_label.config(
            text=current_data["name"]
        )

        temperature_label.config(
            text=f"{temperature:.1f} °C"
        )

        fahrenheit = (temperature * 9 / 5) + 32

        temp_f_label.config(
            text=f"{fahrenheit:.1f} °F"
        )

        condition_label.config(
            text=weather.title()
        )

        humidity_label.config(
            text=f"Humidity: {humidity}%"
        )

        wind_label.config(
            text=f"Wind Speed: {wind} m/s"
        )

        # Load weather icon
        load_icon(icon)

        # Get forecast
        get_forecast(city)

        show_error("")

    except requests.exceptions.Timeout:

        show_error(
            "Request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        show_error(
            "Network error. Check your internet connection."
        )

    except requests.exceptions.RequestException:

        show_error(
            "Unable to connect to weather service."
        )

    except Exception as e:

        show_error(
            "Something went wrong."
        )


# ---------------- WEATHER ICON ----------------

def load_icon(icon_code):

    try:

        icon_url = (
            f"https://openweathermap.org/img/wn/"
            f"{icon_code}@2x.png"
        )

        response = requests.get(
            icon_url,
            timeout=10
        )

        image = Image.open(
            BytesIO(response.content)
        )

        image = image.resize((100, 100))

        weather_image = ImageTk.PhotoImage(image)

        icon_label.config(
            image=weather_image
        )

        # Keep reference
        icon_label.image = weather_image

    except Exception:

        icon_label.config(
            image=""
        )


# ---------------- FORECAST ----------------

def get_forecast(city):

    try:

        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(
            forecast_url,
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            return

        # Clear old forecast
        hourly_text.delete(
            "1.0",
            tk.END
        )

        daily_text.delete(
            "1.0",
            tk.END
        )

        # ---------------- NEXT 6 HOURS ----------------

        hourly_text.insert(
            tk.END,
            "NEXT 6 HOURS\n\n"
        )

        # Forecast API gives data every 3 hours
        for item in data["list"][:2]:

            time = datetime.fromtimestamp(
                item["dt"]
            ).strftime("%I:%M %p")

            temp = item["main"]["temp"]

            condition = item["weather"][0]["description"]

            hourly_text.insert(
                tk.END,
                f"{time}  |  "
                f"{temp:.1f} °C  |  "
                f"{condition.title()}\n"
            )

        # ---------------- NEXT 5 DAYS ----------------

        daily_text.insert(
            tk.END,
            "NEXT 5 DAYS\n\n"
        )

        days = {}

        for item in data["list"]:

            date = datetime.fromtimestamp(
                item["dt"]
            ).strftime("%Y-%m-%d")

            if date not in days:

                days[date] = item

        count = 0

        for date, item in days.items():

            if count >= 5:
                break

            day = datetime.strptime(
                date,
                "%Y-%m-%d"
            ).strftime("%A")

            temp = item["main"]["temp"]

            condition = item["weather"][0]["description"]

            daily_text.insert(
                tk.END,
                f"{day}  |  "
                f"{temp:.1f} °C  |  "
                f"{condition.title()}\n"
            )

            count += 1

    except Exception:

        show_error(
            "Forecast could not be loaded."
        )


# ---------------- CELSIUS / FAHRENHEIT ----------------

def toggle_unit():

    global current_unit

    if current_unit == "C":

        current_unit = "F"

        temperature = temperature_label.cget(
            "text"
        ).replace(" °C", "")

        try:

            celsius = float(temperature)

            fahrenheit = (
                celsius * 9 / 5
            ) + 32

            temperature_label.config(
                text=f"{fahrenheit:.1f} °F"
            )

            unit_button.config(
                text="Switch to °C"
            )

        except ValueError:
            pass

    else:

        current_unit = "C"

        temperature = temperature_label.cget(
            "text"
        ).replace(" °F", "")

        try:

            fahrenheit = float(temperature)

            celsius = (
                fahrenheit - 32
            ) * 5 / 9

            temperature_label.config(
                text=f"{celsius:.1f} °C"
            )

            unit_button.config(
                text="Switch to °F"
            )

        except ValueError:
            pass


# ---------------- ERROR MESSAGE ----------------

def show_error(message):

    error_label.config(
        text=message
    )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Weather App")

root.geometry("700x750")


# ---------------- TITLE ----------------

title_label = tk.Label(
    root,
    text="🌤️ Weather App",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=15
)


# ---------------- CITY INPUT ----------------

city_label_input = tk.Label(
    root,
    text="Enter City Name",
    font=("Arial", 13)
)

city_label_input.pack()


city_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=30
)

city_entry.pack(
    pady=8
)


# ---------------- GET WEATHER BUTTON ----------------

get_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12, "bold"),
    command=get_weather
)

get_button.pack(
    pady=5
)


# ---------------- ERROR LABEL ----------------

error_label = tk.Label(
    root,
    text="",
    font=("Arial", 11)
)

error_label.pack(
    pady=5
)


# ---------------- CITY ----------------

city_label = tk.Label(
    root,
    text="Weather",
    font=("Arial", 20, "bold")
)

city_label.pack(
    pady=5
)


# ---------------- ICON ----------------

icon_label = tk.Label(
    root
)

icon_label.pack()


# ---------------- TEMPERATURE ----------------

temperature_label = tk.Label(
    root,
    text="-- °C",
    font=("Arial", 25, "bold")
)

temperature_label.pack()


temp_f_label = tk.Label(
    root,
    text="-- °F",
    font=("Arial", 15)
)

temp_f_label.pack()


# ---------------- CONDITION ----------------

condition_label = tk.Label(
    root,
    text="Condition: --",
    font=("Arial", 15)
)

condition_label.pack(
    pady=5
)


# ---------------- HUMIDITY ----------------

humidity_label = tk.Label(
    root,
    text="Humidity: --",
    font=("Arial", 13)
)

humidity_label.pack()


# ---------------- WIND ----------------

wind_label = tk.Label(
    root,
    text="Wind Speed: --",
    font=("Arial", 13)
)

wind_label.pack(
    pady=5
)


# ---------------- UNIT BUTTON ----------------

unit_button = tk.Button(
    root,
    text="Switch to °F",
    command=toggle_unit
)

unit_button.pack(
    pady=5
)


# ---------------- HOURLY FORECAST ----------------

hourly_label = tk.Label(
    root,
    text="Hourly Forecast",
    font=("Arial", 14, "bold")
)

hourly_label.pack(
    pady=8
)


hourly_text = tk.Text(
    root,
    width=65,
    height=4
)

hourly_text.pack()


# ---------------- DAILY FORECAST ----------------

daily_label = tk.Label(
    root,
    text="Daily Forecast",
    font=("Arial", 14, "bold")
)

daily_label.pack(
    pady=8
)


daily_text = tk.Text(
    root,
    width=65,
    height=7
)

daily_text.pack()


# ---------------- START PROGRAM ----------------

root.mainloop()