import streamlit as st
import requests
from datetime import datetime, timedelta

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="iWeather Pro",
    page_icon="🌦",
    layout="wide"
)

# =========================================
# API KEY
# =========================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =========================================
# WEATHER ICONS
# =========================================
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

# =========================================
# BACKGROUND
# =========================================
def get_background(weather, hour):

    weather = weather.lower()

    if "clear" in weather and (hour >= 18 or hour <= 5):
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920"

    if "clear" in weather:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920"

    if "cloud" in weather:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?w=1920"

    if "rain" in weather:
        return "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1920"

    if "thunder" in weather:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22?w=1920"

    if (
        "mist" in weather
        or "fog" in weather
        or "haze" in weather
    ):
        return "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?w=1920"

    return "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"

# =========================================
# API CALL
# =========================================
@st.cache_data(ttl=600)
def get_weather(city):

    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        "&units=metric"
    )

    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}"
        f"&appid={API_KEY}"
        "&units=metric"
    )

    weather = requests.get(
        weather_url,
        timeout=10
    ).json()

    forecast = requests.get(
        forecast_url,
        timeout=10
    ).json()

    return weather, forecast

# =========================================
# CSS
# =========================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: sans-serif;
    color: white;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.title {
    text-align: center;
    font-size: 70px;
    font-weight: bold;
    margin-bottom: 20px;
}

.glass {
    background: rgba(20,20,30,0.45);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 25px;
    padding: 25px;
    backdrop-filter: blur(16px);
}

.card {
    background: rgba(20,20,30,0.45);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-top: 10px;
}

.temp {
    font-size: 120px;
    text-align: center;
    font-weight: 300;
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================
st.markdown(
    "<div class='title'>🌦 iWeather Pro</div>",
    unsafe_allow_html=True
)

# =========================================
# SEARCH
# =========================================
city = st.text_input(
    "📍 Search City",
    placeholder="Enter city name..."
)

# =========================================
# WEATHER
# =========================================
if city.strip():

    try:

        with st.spinner("Fetching weather..."):

            data, forecast = get_weather(city)

        if str(data.get("cod")) == "200":

            temp = round(data["main"]["temp"])
            feels = round(data["main"]["feels_like"])
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            visibility = data.get("visibility", 0) / 1000

            condition = data["weather"][0]["description"]

            timezone = data["timezone"]

            local_time = (
                datetime.utcnow()
                + timedelta(seconds=timezone)
            )

            hour = local_time.hour

            date = local_time.strftime(
                "%A, %d %B"
            )

            current_time = local_time.strftime(
                "%I:%M %p"
            )

            icon = get_icon(condition, hour)

            bg = get_background(condition, hour)

            # BACKGROUND
            st.markdown(
                f"""
                <style>

                .stApp {{
                    background:
                        linear-gradient(
                            rgba(0,0,0,0.45),
                            rgba(0,0,0,0.45)
                        ),
                        url("{bg}");
                }}

                </style>
                """,
                unsafe_allow_html=True
            )

            # MAIN CARD
            st.markdown(
                f"""
                <div class="glass">

                    <h1 style="text-align:center;">
                        {icon} {city.title()}
                    </h1>

                    <h3 style="text-align:center;">
                        {date}
                    </h3>

                    <h3 style="text-align:center;">
                        🕒 {current_time}
                    </h3>

                    <div class="temp">
                        {temp}°
                    </div>

                    <h2 style="text-align:center;">
                        {condition.title()}
                    </h2>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # DETAILS
            st.subheader("📊 Weather Details")

            details = [
                ("💧 Humidity", f"{humidity}%"),
                ("🌬 Wind", f"{wind} m/s"),
                ("👀 Visibility", f"{visibility} km"),
                ("🤗 Feels Like", f"{feels}°"),
                ("📈 Pressure", f"{pressure} hPa")
            ]

            cols = st.columns(5)

            for col, (title, value) in zip(cols, details):

                col.markdown(
                    f"""
                    <div class="card">
                        <h3>{title}</h3>
                        <h2>{value}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            # FORECAST
            st.subheader("⏰ Hourly Forecast")

            forecast_items = forecast["list"][:6]

            cols = st.columns(6)

            for col, item in zip(cols, forecast_items):

                f_time = (
                    datetime.utcfromtimestamp(item["dt"])
                    + timedelta(seconds=timezone)
                )

                f_hour = f_time.hour

                display_time = f_time.strftime("%I %p")

                f_temp = round(item["main"]["temp"])

                f_weather = item["weather"][0]["description"]

                f_icon = get_icon(
                    f_weather,
                    f_hour
                )

                col.markdown(
                    f"""
                    <div class="card">

                        <h3>{display_time}</h3>

                        <div style="font-size:50px;">
                            {f_icon}
                        </div>

                        <h2>{f_temp}°</h2>

                        <p>{f_weather.title()}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.error("City not found")

    except requests.exceptions.Timeout:
        st.error("Request timed out")

    except Exception as e:
        st.error(f"Error: {e}")
