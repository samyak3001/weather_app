import streamlit as st
import requests
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌦",
    layout="wide"
)

# =========================================================
# API KEY
# =========================================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =========================================================
# WEATHER ICONS
# =========================================================
def get_icon(weather, hour):

    weather = weather.lower()

    if "clear" in weather:
        return "🌙" if hour >= 18 or hour <= 5 else "☀️"

    if "few clouds" in weather:
        return "🌤"

    if "scattered clouds" in weather:
        return "⛅"

    if "broken clouds" in weather:
        return "☁️"

    if "cloud" in weather:
        return "☁️"

    if "drizzle" in weather:
        return "🌦"

    if "light rain" in weather:
        return "🌦"

    if "moderate rain" in weather:
        return "🌧"

    if "heavy" in weather:
        return "⛈"

    if "thunder" in weather:
        return "⚡"

    if "snow" in weather:
        return "❄️"

    if (
        "mist" in weather
        or "fog" in weather
        or "haze" in weather
        or "smoke" in weather
    ):
        return "🌫"

    return "🌤"

# =========================================================
# BACKGROUND IMAGES
# =========================================================
def get_background(weather):

    weather = weather.lower()

    if "clear" in weather:
        return (
            "https://images.unsplash.com/"
            "photo-1500530855697-b586d89ba3ee?w=1920"
        )

    elif "cloud" in weather:
        return (
            "https://images.unsplash.com/"
            "photo-1499346030926-9a72daac6c63?w=1920"
        )

    elif "rain" in weather:
        return (
            "https://images.unsplash.com/"
            "photo-1515694346937-94d85e41e6f0?w=1920"
        )

    elif "thunder" in weather:
        return (
            "https://images.unsplash.com/"
            "photo-1500673922987-e212871fec22?w=1920"
        )

    elif "snow" in weather:
        return (
            "https://images.unsplash.com/"
            "photo-1517299321609-52687d1bc55a?w=1920"
        )

    elif (
        "mist" in weather
        or "fog" in weather
        or "haze" in weather
        or "smoke" in weather
    ):
        return (
            "https://images.unsplash.com/"
            "photo-1485236715568-ddc5ee6ca227?w=1920"
        )

    return (
        "https://images.unsplash.com/"
        "photo-1502082553048-f009c37129b9?w=1920"
    )

# =========================================================
# WEATHER API
# =========================================================
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

# =========================================================
# AQI API
# =========================================================
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

# =========================================================
# CSS
# =========================================================
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
    background-color: rgba(255,255,255,0.12);
    color: white;
    border-radius: 12px;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="column"] {
    width: 100% !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.title("🌦 iWeather Pro")

st.caption("Real-Time Smart Weather Dashboard")

# =========================================================
# SEARCH
# =========================================================
city = st.text_input(
    "📍 Enter City Name",
    placeholder="Search city..."
)

# =========================================================
# WEATHER SECTION
# =========================================================
if city.strip():

    try:

        with st.spinner(
            "🌍 Loading live weather data..."
        ):

            current, forecast = get_weather(city)

        if str(current.get("cod")) == "200":

            # =================================================
            # MAIN DATA
            # =================================================
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

            country = current["sys"]["country"]

            city_name = current["name"]

            lat = current["coord"]["lat"]

            lon = current["coord"]["lon"]

            timezone = current["timezone"]

            # =================================================
            # LOCAL TIME
            # =================================================
            local_time = (
                datetime.utcnow()
                + timedelta(seconds=timezone)
            )

            hour = local_time.hour

            formatted_time = local_time.strftime(
                "%I:%M %p"
            )

            formatted_date = local_time.strftime(
                "%A, %d %B %Y"
            )

            # =================================================
            # ICON + BACKGROUND
            # =================================================
            icon = get_icon(weather, hour)

            bg = get_background(weather)

            # =================================================
            # APPLY BACKGROUND
            # =================================================
            st.markdown(
                f"""
                <style>

                .stApp {{
                    background:
                        linear-gradient(
                            rgba(0,0,0,0.45),
                            rgba(0,0,0,0.55)
                        ),
                        url("{bg}");

                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}

                </style>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # MAIN DISPLAY
            # =================================================
            st.markdown("---")

            st.markdown(
                f"# {icon} {city_name}, {country}"
            )

            st.markdown(
                f"### {weather.title()}"
            )

            st.markdown(
                f"# 🌡 {temp}°C"
            )

            st.markdown(
                f"🕒 {formatted_time}"
            )

            st.markdown(
                formatted_date
            )

            st.markdown("---")

            # =================================================
            # WEATHER DETAILS
            # =================================================
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
                f"{feels}°C"
            )

            c5.metric(
                "📈 Pressure",
                f"{pressure} hPa"
            )

            st.markdown("---")

            # =================================================
            # SUN TIMING
            # =================================================
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

            # =================================================
            # AIR QUALITY
            # =================================================
            aqi_data = get_aqi(lat, lon)

            aqi = aqi_data.get(
                "list",
                [{}]
            )[0].get(
                "main",
                {}
            ).get(
                "aqi",
                1
            )

            aqi_map = {
                1: "Good 😊",
                2: "Fair 🙂",
                3: "Moderate 😐",
                4: "Poor 😷",
                5: "Very Poor ☠️"
            }

            st.subheader("🌫 Air Quality")

            st.metric(
                "AQI",
                aqi_map[aqi]
            )

            st.markdown("---")

            # =================================================
            # HOURLY FORECAST
            # =================================================
            st.subheader("⏰ Hourly Forecast")

            hourly = forecast["list"][:6]

            cols = st.columns(6)

            for col, item in zip(cols, hourly):

                forecast_time = (
                    datetime.utcfromtimestamp(
                        item["dt"]
                    )
                    + timedelta(seconds=timezone)
                )

                f_hour = forecast_time.hour

                display_time = forecast_time.strftime(
                    "%I %p"
                )

                forecast_temp = round(
                    item["main"]["temp"]
                )

                forecast_weather = item[
                    "weather"
                ][0]["description"]

                forecast_icon = get_icon(
                    forecast_weather,
                    f_hour
                )

                rain = item.get(
                    "pop",
                    0
                ) * 100

                col.metric(
                    display_time,
                    f"{forecast_temp}°",
                    forecast_icon
                )

                col.caption(
                    forecast_weather.title()
                )

                col.caption(
                    f"🌧 {rain:.0f}% chance"
                )

            st.markdown("---")

            # =================================================
            # 5 DAY FORECAST
            # =================================================
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

            # =================================================
            # TEMPERATURE CHART
            # =================================================
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
                markers=True,
                title="Next Hours Temperature"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            fig.update_traces(
                line_width=4
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("---")

            # =================================================
            # AI WEATHER PREDICTION
            # =================================================
            st.subheader("🔮 AI Weather Prediction")

            if "rain" in weather:
                prediction = (
                    "🌧 Rain may continue tomorrow."
                )

            elif "cloud" in weather:
                prediction = (
                    "☁️ Cloudy weather expected tomorrow."
                )

            elif "thunder" in weather:
                prediction = (
                    "⚡ Thunderstorm chances tomorrow."
                )

            elif temp > 35:
                prediction = (
                    "🥵 Very hot weather tomorrow."
                )

            elif temp < 18:
                prediction = (
                    "❄️ Cold weather tomorrow."
                )

            else:
                prediction = (
                    "☀️ Pleasant weather tomorrow."
                )

            st.success(prediction)

            st.caption(
                "🔄 Auto refresh every 10 minutes"
            )

            # =================================================
            # FOOTER
            # =================================================
            st.markdown(
                """
                ---
                ### 🌦 iWeather Pro
                Made by Samyak M
                """
            )

        else:
            st.error("City not found")

    except requests.exceptions.Timeout:
        st.error("Request timed out")

    except requests.exceptions.ConnectionError:
        st.error("Internet connection issue")

    except Exception as e:
        st.error(f"Error: {e}")
