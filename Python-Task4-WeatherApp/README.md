# 🌤️ Basic Weather App

A Python-based Weather Application that fetches real-time weather information for a user-selected city using the OpenWeatherMap API.

The application provides a simple graphical interface built with Tkinter and displays current weather information along with forecast details.

---

## 🎯 Project Objective

The objective of this project is to build a weather application that can:

- Accept a city name from the user
- Fetch real-time weather data using an API
- Display temperature and weather conditions
- Show humidity and wind speed
- Display weather icons
- Provide short-term and daily forecast information
- Handle invalid input and API errors gracefully

---

## ✨ Features

### 🌡️ Current Weather

The application displays:

- Temperature
- Temperature in Celsius and Fahrenheit
- Humidity
- Weather condition
- Wind speed
- Weather icon

### 🔮 Forecast

The application provides:

- Next few hours forecast
- 5-day forecast information

### 🌍 Unit Conversion

Users can switch between:

- Celsius (°C)
- Fahrenheit (°F)

### ⚠️ Error Handling

The application handles:

- Empty city input
- Invalid city name
- Invalid API key
- Network errors
- Request timeout

### 🖥️ Graphical User Interface

The application uses **Tkinter** to provide an easy-to-use GUI.

---

## 🛠️ Technologies Used

- Python
- Tkinter
- Requests
- JSON
- Pillow
- python-dotenv
- OpenWeatherMap API

---

## 📁 Project Structure

```text
Python-Task4-WeatherApp/
│
├── weather_app.py
├── README.md
├── .env
│
└── screenshots/
    ├── 01-main.png
    ├── 02-weather-result.png
    ├── 03-fahrenheit.png
    ├── 04-invalid-city.png
    └── 05-empty-input.png
```
