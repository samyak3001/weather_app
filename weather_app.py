import streamlit as st
import requests
from datetime import datetime, timedelta

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌦",
    layout="wide"
)

# =====================================
# API KEY
# =====================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =====================================
# WEATHER ICONS
# =====================================
def get_icon(weather, hour):

    weather = weather.lower()

    if "clear" in weather:
        return "🌙" if hour >= 18 or hour <= 5 else "☀️"

    if "cloud" in weather:
        return "☁️"

    if "rain" in weather:
        return "🌧"

    if "drizzle" in weather:
        return "🌦"

    if "thunder" in weather:
        return "⛈"

    if "snow" in weather:
        return "❄️"

    if (
        "mist" in weather
        or "fog" in weather
        or "haze" in weather
    ):
        return "🌫"

    return "🌤"

# =====================================
# GET WEATHER
# =====================================
@st.cache_data(ttl=600)
def get_weather(city):

    current_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    current = requests.get(
        current_url,
        timeout=10
    ).json()

    forecast = requests.get(
        forecast_url,
        timeout=10
    ).json()

    return current, forecast

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
}

h1, h2, h3, p {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.title("🌦 iWeather Pro")

city = st.text_input(
    "📍 Enter City Name"
)

# =====================================
# WEATHER
# =====================================
if city:

    try:

        with st.spinner("Fetching weather..."):

            current, forecast = get_weather(city)

        if str(current.get("cod")) == "200":

            temp = round(
                current["main"]["temp"]
            )

            feels = round(
                current["main"]["feels_like"]
            )

            humidity = current["main"]["humidity"]

            pressure = current["main"]["pressure"]

            wind = current["wind"]["speed"]

            visibility = (
                current.get("visibility", 0)
                / 1000
            )

            condition = current["weather"][0]["description"]

            timezone = current["timezone"]

            local_time = (
                datetime.utcnow()
                + timedelta(seconds=timezone)
            )

            hour = local_time.hour

            icon = get_icon(
                condition,
                hour
            )

            # =====================================
            # MAIN INFO
            # =====================================
            st.markdown("---")

            st.markdown(
                f"# {icon} {city.title()}"
            )

            st.markdown(
                f"### {condition.title()}"
            )

            st.markdown(
                f"# 🌡 {temp}°C"
            )

            st.markdown(
                f"🕒 {local_time.strftime('%I:%M %p')}"
            )

            st.markdown("---")

            # =====================================
            # DETAILS
            # =====================================
            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric(
                "💧 Humidity",
                f"{humidity}%"
            )

            c2.metric(
                "🌬 Wind",
                f"{wind} m/s"
            )

            c3.metric(
                "👀 Visibility",
                f"{visibility} km"
            )

            c4.metric(
                "🤗 Feels Like",
                f"{feels}°"
            )

            c5.metric(
                "📈 Pressure",
                f"{pressure} hPa"
            )

            st.markdown("---")

            # =====================================
            # FORECAST
            # =====================================
            st.subheader(
                "⏰ Hourly Forecast"
            )

            hourly = forecast["list"][:6]

            cols = st.columns(6)

            for col, item in zip(cols, hourly):

                f_time = (
                    datetime.utcfromtimestamp(
                        item["dt"]
                    )
                    + timedelta(seconds=timezone)
                )

                f_hour = f_time.hour

                f_temp = round(
                    item["main"]["temp"]
                )

                f_weather = item[
                    "weather"
                ][0]["description"]

                f_icon = get_icon(
                    f_weather,
                    f_hour
                )

                col.metric(
                    f"{f_time.strftime('%I %p')}",
                    f"{f_temp}°",
                    f"{f_icon}"
                )

                col.caption(
                    f_weather.title()
                )

            st.markdown("---")

            # =====================================
            # PREDICTION
            # =====================================
            if st.button(
                "🔮 Predict Tomorrow"
            ):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in condition:
                    prediction = (
                        "🌧 Rain Expected Tomorrow"
                    )

                elif "cloud" in condition:
                    prediction = (
                        "☁️ Cloudy Tomorrow"
                    )

                elif "thunder" in condition:
                    prediction = (
                        "⛈ Storm Chances Tomorrow"
                    )

                st.success(prediction)

        else:
            st.error("City not found")

    except requests.exceptions.Timeout:
        st.error("Request timed out")

    except Exception as e:
        st.error(f"Error: {e}")
