import streamlit as st
import requests

# ======================================
# CONFIG
# ======================================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌤",
    layout="centered"
)

API_KEY = "96c73ea634856d67ace6716d27c2662e"

# ======================================
# TITLE
# ======================================
st.title("🌤 iWeather")

city = st.text_input(
    "Enter City Name"
)

# ======================================
# WEATHER FUNCTION
# ======================================
def get_weather(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    return response.json()

# ======================================
# BUTTON
# ======================================
if st.button("Get Weather"):

    if city:

        data = get_weather(city)

        if data.get("cod") == 200:

            temp = data["main"]["temp"]

            feels = data["main"]["feels_like"]

            humidity = data["main"]["humidity"]

            weather = data["weather"][0]["description"]

            wind = data["wind"]["speed"]

            st.success(f"Weather in {city}")

            st.metric("🌡 Temperature", f"{temp} °C")

            st.metric("🤗 Feels Like", f"{feels} °C")

            st.metric("💧 Humidity", f"{humidity}%")

            st.metric("🌬 Wind Speed", f"{wind} m/s")

            st.write(
                f"### 🌤 Condition: {weather.title()}"
            )

        else:
            st.error("City not found")

    else:
        st.warning("Enter city name") 
