import streamlit as st
import requests
import pandas as pd
import calendar
from datetime import datetime

# Funcție pentru a prelua datele meteo de la WeatherAPI
def get_weather_data(api_key, city, date):
    date_str = date.strftime("%Y-%m-%d")
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&dt={date_str}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        st.error(f"Error fetching data: {data.get('error', {}).get('message', 'Unknown error')}")
        return None

    if 'forecast' not in data or not data['forecast']['forecastday']:
        st.error(f"No weather data found for {city} on {date_str}. Please check the city name and try again.")
        return None

    forecast_day = data['forecast']['forecastday'][0]['day']
    weather_data = {
        'temperature': forecast_day['avgtemp_c'],
        'wind': forecast_day['maxwind_kph'],
        'humidity': forecast_day['avghumidity'],
        'icon': forecast_day['condition']['icon'],
        'description': forecast_day['condition']['text']
    }
    return weather_data

# Funcție pentru a verifica dacă locația este validă
def is_valid_location(api_key, city):
    url = f"http://api.weatherapi.com/v1/search.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()

    return len(data) > 0  # Returnează True dacă locația este validă

# Cheie API
api_key = '8a2b208ea9f9479c94c135753240106 '  # Înlocuiește 'YOUR_WEATHERAPI_KEY' cu cheia ta API de la WeatherAPI

# Introducerea numelui orașului
city = st.text_input('Enter city name:', 'New York')

if city:
    if is_valid_location(api_key, city):
        # Generarea calendarului
        year = datetime.now().year
        month = datetime.now().month
        cal = calendar.monthcalendar(year, month)

        # Afișarea calendarului în Streamlit
        st.title(f"Weather Calendar for {city} - {calendar.month_name[month]} {year}")

        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day != 0:
                    date = datetime(year, month, day).date()
                    weather = get_weather_data(api_key, city, date)
                    
                    if weather:
                        with cols[i]:
                            st.write(f"{day}")
                            st.image(f"http:{weather['icon']}")
                            st.write(f"Temp: {weather['temperature']} °C")
                            st.write(f"Wind: {weather['wind']} kph")
                            st.write(f"Humidity: {weather['humidity']}%")
                            st.write(f"{weather['description']}")
                    else:
                        with cols[i]:
                            st.write(f"{day}")
                            st.write("No data")
    else:
        st.error(f"Invalid city name: {city}. Please check the city name and try again.")
