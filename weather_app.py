import streamlit as st
import requests
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="iWeather Pro",
    page_icon="🌦",
    layout="wide"
)

# =====================================================
# API KEY
# =====================================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =====================================================
# WEATHER ICONS
# =====================================================
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

# =====================================================
# BACKGROUND IMAGES
# =====================================================
def get_background(weather):

    weather = weather.lower()

    if "clear" in weather:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920"

    if "cloud" in weather:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?w=1920"

    if "rain" in weather:
        return "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1920"

    if "thunder" in weather:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22?w=1920"

    if "snow" in weather:
        return "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=1920"

    return "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"

# =====================================================
# GET WEATHER
# =====================================================
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

# =====================================================
# GET AQI
# =====================================================
@st.cache_data(ttl=600)
def get_aqi(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution?"
        f"lat={lat}&lon={lon}&appid={API_KEY}"
    )

    return requests.get(
        url,
        timeout=10
    ).json()

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

h1, h2, h3, h4, p, label {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: white;
}

.stTextInput input {
    background-color: rgba(255,255,255,0.1);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.title("🌦 iWeather Pro")

st.caption("Real-Time Smart Weather Dashboard")

# =====================================================
# SEARCH
# =====================================================
city = st.text_input(
    "📍 Enter City Name",
    placeholder="Search city..."
)

# =====================================================
# WEATHER SECTION
# =====================================================
if city:

    try:

        with st.spinner("Fetching weather..."):

            current, forecast = get_weather(city)

        if str(current.get("cod")) == "200":

            # =====================================================
            # DATA
            # =====================================================
            temp = round(current["main"]["temp"])

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

            weather = current["weather"][0]["description"]

            timezone = current["timezone"]

            country = current["sys"]["country"]

            lat = current["coord"]["lat"]

            lon = current["coord"]["lon"]

            local_time = (
                datetime.utcnow()
                + timedelta(seconds=timezone)
            )

            hour = local_time.hour

            icon = get_icon(
                weather,
                hour
            )

            # =====================================================
            # BACKGROUND
            # =====================================================
            bg = get_background(weather)

            st.markdown(
                f"""
                <style>

                .stApp {{
                    background:
                        linear-gradient(
                            rgba(0,0,0,0.5),
                            rgba(0,0,0,0.5)
                        ),
                        url("{bg}");

                    background-size: cover;
                }}

                </style>
                """,
                unsafe_allow_html=True
            )

            # =====================================================
            # MAIN INFO
            # =====================================================
            st.markdown("---")

            st.markdown(
                f"# {icon} {city.title()}, {country}"
            )

            st.markdown(
                f"### {weather.title()}"
            )

            st.markdown(
                f"# 🌡 {temp}°C"
            )

            st.markdown(
                f"🕒 {local_time.strftime('%I:%M %p')}"
            )

            st.markdown("---")

            # =====================================================
            # WEATHER DETAILS
            # =====================================================
            st.subheader("📊 Weather Details")

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

            # =====================================================
            # SUNRISE / SUNSET
            # =====================================================
            sunrise = (
                datetime.utcfromtimestamp(
                    current["sys"]["sunrise"]
                )
                + timedelta(seconds=timezone)
            ).strftime("%I:%M %p")

            sunset = (
                datetime.utcfromtimestamp(
                    current["sys"]["sunset"]
                )
                + timedelta(seconds=timezone)
            ).strftime("%I:%M %p")

            st.subheader("🌅 Sun Timing")

            s1, s2 = st.columns(2)

            s1.metric(
                "🌅 Sunrise",
                sunrise
            )

            s2.metric(
                "🌇 Sunset",
                sunset
            )

            st.markdown("---")

            # =====================================================
            # AQI
            # =====================================================
            aqi_data = get_aqi(lat, lon)

            aqi = aqi_data["list"][0]["main"]["aqi"]

            aqi_text = {
                1: "Good 😊",
                2: "Fair 🙂",
                3: "Moderate 😐",
                4: "Poor 😷",
                5: "Very Poor ☠️"
            }

            st.subheader("🌫 Air Quality")

            st.metric(
                "AQI",
                aqi_text[aqi]
            )

            st.markdown("---")

            # =====================================================
            # HOURLY FORECAST
            # =====================================================
            st.subheader("⏰ Hourly Forecast")

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
                    f_time.strftime("%I %p"),
                    f"{f_temp}°",
                    f_icon
                )

                col.caption(
                    f_weather.title()
                )

            st.markdown("---")

            # =====================================================
            # 5 DAY FORECAST
            # =====================================================
            st.subheader("📅 5-Day Forecast")

            daily_data = forecast["list"][::8][:5]

            cols = st.columns(5)

            for col, item in zip(cols, daily_data):

                day = datetime.utcfromtimestamp(
                    item["dt"]
                ).strftime("%a")

                d_temp = round(
                    item["main"]["temp"]
                )

                d_weather = item[
                    "weather"
                ][0]["description"]

                d_icon = get_icon(
                    d_weather,
                    12
                )

                col.metric(
                    day,
                    f"{d_temp}°",
                    d_icon
                )

                col.caption(
                    d_weather.title()
                )

            st.markdown("---")

            # =====================================================
            # TEMPERATURE CHART
            # =====================================================
            st.subheader("🌡 Temperature Trend")

            temps = [
                item["main"]["temp"]
                for item in forecast["list"][:8]
            ]

            times = [
                (
                    datetime.utcfromtimestamp(
                        item["dt"]
                    )
                    + timedelta(seconds=timezone)
                ).strftime("%I %p")
                for item in forecast["list"][:8]
            ]

            df = pd.DataFrame({
                "Time": times,
                "Temperature": temps
            })

            fig = px.line(
                df,
                x="Time",
                y="Temperature",
                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("---")

            # =====================================================
            # PREDICTION
            # =====================================================
            if st.button(
                "🔮 Predict Tomorrow"
            ):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in weather:
                    prediction = (
                        "🌧 Rain Expected Tomorrow"
                    )

                elif "cloud" in weather:
                    prediction = (
                        "☁️ Cloudy Tomorrow"
                    )

                elif "thunder" in weather:
                    prediction = (
                        "⛈ Storm Chances Tomorrow"
                    )

                elif temp > 35:
                    prediction = (
                        "🥵 Very Hot Tomorrow"
                    )

                elif temp < 18:
                    prediction = (
                        "❄️ Cold Tomorrow"
                    )

                st.success(prediction)

            st.caption(
                "🔄 Auto refresh every 10 minutes"
            )

        else:
            st.error("City not found")

    except requests.exceptions.Timeout:
        st.error("Request timed out")

    except Exception as e:
        st.error(f"Error: {e}")
