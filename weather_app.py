import streamlit as st
import requests
from datetime import datetime, timedelta

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
# CACHE WEATHER
# =====================================================
@st.cache_data(ttl=600)
def get_weather(city):

    current_url = (
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
# WEATHER ICONS
# =====================================================
def get_icon(weather, hour):

    weather = weather.lower()

    if "clear" in weather:
        if hour >= 18 or hour <= 5:
            return "🌙"
        return "☀️"

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
# BACKGROUND
# =====================================================
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

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
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
    font-size: 75px;
    font-weight: bold;
    margin-bottom: 25px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.glass {
    background: rgba(20,20,30,0.45);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 28px;
    padding: 30px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

.card {
    background: rgba(20,20,30,0.45);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 22px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(16px);
    margin-top: 10px;
}

.temp {
    font-size: 120px;
    font-weight: 300;
    text-align: center;
}

.stTextInput input {
    background: rgba(20,20,30,0.45);
    color: white;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.2);
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 16px;
    border: none;
    color: white;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.25),
        rgba(255,255,255,0.1)
    );
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown(
    "<div class='title'>🌦 iWeather Pro</div>",
    unsafe_allow_html=True
)

# =====================================================
# SEARCH
# =====================================================
city = st.text_input(
    "📍 Search City",
    placeholder="Enter city name..."
)

# =====================================================
# WEATHER SECTION
# =====================================================
if city:

    try:

        with st.spinner("Fetching weather..."):

            current, forecast = get_weather(city)

        if current.get("cod") == 200:

            # DATA
            temp = round(current["main"]["temp"])
            feels = round(current["main"]["feels_like"])
            humidity = current["main"]["humidity"]
            pressure = current["main"]["pressure"]
            wind = current["wind"]["speed"]
            visibility = current.get("visibility", 0) / 1000
            weather = current["weather"][0]["description"]

            timezone = current["timezone"]

            local_time = (
                datetime.utcnow()
                + timedelta(seconds=timezone)
            )

            hour = local_time.hour

            date = local_time.strftime(
                "%A, %d %B"
            )

            time_now = local_time.strftime(
                "%I:%M %p"
            )

            icon = get_icon(weather, hour)

            bg = get_background(weather, hour)

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

            # =====================================================
            # MAIN CARD
            # =====================================================
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
                        🕒 {time_now}
                    </h3>

                    <div class="temp">
                        {temp}°
                    </div>

                    <h2 style="text-align:center;">
                        {weather.title()}
                    </h2>

                    <h3 style="text-align:center;">
                        H:{round(current['main']['temp_max'])}°
                        &nbsp;
                        L:{round(current['main']['temp_min'])}°
                    </h3>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # =====================================================
            # DETAILS
            # =====================================================
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

            # =====================================================
            # SUN TIMING
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

            s1.markdown(
                f"""
                <div class="card">
                    <h3>🌅 Sunrise</h3>
                    <h2>{sunrise}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            s2.markdown(
                f"""
                <div class="card">
                    <h3>🌇 Sunset</h3>
                    <h2>{sunset}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # =====================================================
            # HOURLY FORECAST
            # =====================================================
            st.subheader("⏰ Hourly Forecast")

            hourly = forecast["list"][:6]

            forecast_cols = st.columns(6)

            for col, item in zip(forecast_cols, hourly):

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

            st.write("")

            # =====================================================
            # PREDICTION
            # =====================================================
            if st.button("🔮 Predict Tomorrow Weather"):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in weather:
                    prediction = "🌧 Rain Expected Tomorrow"

                elif "cloud" in weather:
                    prediction = "☁️ Cloudy Tomorrow"

                elif "thunder" in weather:
                    prediction = "⛈ Storm Chances Tomorrow"

                elif temp > 35:
                    prediction = "🥵 Very Hot Tomorrow"

                elif temp < 18:
                    prediction = "❄️ Cold Tomorrow"

                st.markdown(
                    f"""
                    <div class="glass">

                        <h1 style="text-align:center;">
                            {prediction}
                        </h1>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.error("City not found")

    except Exception as e:
        st.error(f"Error: {e}")

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div style="
text-align:center;
padding:20px;
font-size:18px;
font-weight:bold;
">
🌟 Designed By
<span style="color:#FFD700;">
Samyak M
</span>
</div>
""", unsafe_allow_html=True)
