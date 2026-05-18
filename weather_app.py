import streamlit as st
import requests
from datetime import datetime, timedelta

# =========================
# 🔑 API KEY
# =========================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌤",
    layout="centered"
)

# =========================
# 🎨 BACKGROUND FUNCTION
# =========================
def get_bg(weather, temp):

    weather = weather.lower()

    if "thunder" in weather:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22"

    elif "rain" in weather:
        return "https://images.unsplash.com/photo-1501696461415-6bd6660c6742"

    elif "cloud" in weather:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63"

    elif "clear" in weather and temp > 25:
        return "https://images.unsplash.com/photo-1501973801540-537f08ccae7b"

    elif "clear" in weather:
        return "https://images.unsplash.com/photo-1502082553048-f009c37129b9"

    else:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"


# =========================
# 🎨 CSS
# =========================
st.markdown("""
<style>

.stApp {
    color: white;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    margin-bottom: 25px;
}

.temp {
    font-size: 95px;
    text-align: center;
    font-weight: 300;
    margin-top: -10px;
}

.center {
    text-align: center;
}

.card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    padding: 18px;
    border-radius: 20px;
    text-align: center;
    margin: 5px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

.prediction-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(14px);
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.35);
}

.stButton > button {
    width: 100%;
    border-radius: 15px;
    height: 55px;
    font-size: 20px;
    font-weight: bold;
    background: rgba(255,255,255,0.2);
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.35);
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🌤 TITLE
# =========================
st.markdown(
    "<div class='title'>🌤 iWeather</div>",
    unsafe_allow_html=True
)

# =========================
# 🔍 SEARCH CITY
# =========================
search = st.text_input("🔍 Search City")

lat = None
lon = None
selected = None

# =========================
# 🌍 GEO API
# =========================
if search:

    try:

        geo_url = (
            f"https://api.openweathermap.org/geo/1.0/direct?"
            f"q={search}&limit=5&appid={API_KEY}"
        )

        geo_response = requests.get(geo_url)

        if geo_response.status_code == 200:

            geo_data = geo_response.json()

            if geo_data:

                options = [
                    f"{c['name']}, {c.get('state','')}, {c['country']}".replace(" ,", "")
                    for c in geo_data
                ]

                selected = st.selectbox(
                    "Select City",
                    options
                )

                selected_city = geo_data[options.index(selected)]

                lat = selected_city["lat"]
                lon = selected_city["lon"]

            else:
                st.error("❌ City not found")

        else:
            st.error("❌ API Error")

    except Exception as e:
        st.error(f"Error: {e}")

# =========================
# 🌦 WEATHER DATA
# =========================
if lat is not None and lon is not None:

    try:

        # Current Weather
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        # Forecast
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        data = requests.get(weather_url).json()
        forecast_data = requests.get(forecast_url).json()

        if data.get("cod") == 200:

            # =========================
            # WEATHER DETAILS
            # =========================
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            feels_like = data["main"]["feels_like"]
            pressure = data["main"]["pressure"]

            weather = data["weather"][0]["description"]
            weather_main = data["weather"][0]["main"]

            wind_speed = data["wind"]["speed"]

            visibility = data.get("visibility", 0) / 1000

            timezone_offset = data["timezone"]

            # =========================
            # 🎨 BACKGROUND
            # =========================
            bg = get_bg(weather, temp)

            st.markdown(f"""
            <style>

            .stApp {{
                background-image: url("{bg}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.45);
                backdrop-filter: blur(5px);
                z-index: -1;
            }}

            </style>
            """, unsafe_allow_html=True)

            # =========================
            # 🕒 LOCAL TIME
            # =========================
            utc_time = datetime.utcnow()

            local_time = utc_time + timedelta(
                seconds=timezone_offset
            )

            current_time = local_time.strftime("%I:%M %p")
            current_date = local_time.strftime("%A, %d %B")

            # =========================
            # 📍 MAIN DISPLAY
            # =========================
            st.markdown(
                f"<h2 class='center'>{selected}</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='center'>{current_date}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='center' style='font-size:20px;'>🕒 {current_time}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='temp'>{round(temp)}°</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='center' style='font-size:24px;'>"
                f"{weather.title()}"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='center'>"
                f"H:{round(data['main']['temp_max'])}° "
                f"L:{round(data['main']['temp_min'])}°"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown("---")

            # =========================
            # 🌅 SUNRISE / SUNSET
            # =========================
            sunrise = (
                datetime.utcfromtimestamp(data["sys"]["sunrise"])
                + timedelta(seconds=timezone_offset)
            ).strftime("%I:%M %p")

            sunset = (
                datetime.utcfromtimestamp(data["sys"]["sunset"])
                + timedelta(seconds=timezone_offset)
            ).strftime("%I:%M %p")

            col1, col2 = st.columns(2)

            col1.markdown(
                f"<div class='card'>🌅 Sunrise<br><br><b>{sunrise}</b></div>",
                unsafe_allow_html=True
            )

            col2.markdown(
                f"<div class='card'>🌇 Sunset<br><br><b>{sunset}</b></div>",
                unsafe_allow_html=True
            )

            st.markdown("---")

            # =========================
            # 📊 WEATHER DETAILS
            # =========================
            st.markdown("### 📊 Weather Details")

            c1, c2, c3 = st.columns(3)

            c1.markdown(
                f"<div class='card'>💧 Humidity<br><br><b>{humidity}%</b></div>",
                unsafe_allow_html=True
            )

            c2.markdown(
                f"<div class='card'>🌬 Wind<br><br><b>{wind_speed} m/s</b></div>",
                unsafe_allow_html=True
            )

            c3.markdown(
                f"<div class='card'>👀 Visibility<br><br><b>{visibility} km</b></div>",
                unsafe_allow_html=True
            )

            c4, c5 = st.columns(2)

            c4.markdown(
                f"<div class='card'>🤗 Feels Like<br><br><b>{round(feels_like)}°</b></div>",
                unsafe_allow_html=True
            )

            c5.markdown(
                f"<div class='card'>📈 Pressure<br><br><b>{pressure} hPa</b></div>",
                unsafe_allow_html=True
            )

            st.markdown("---")

            # =========================
            # ⏰ HOURLY FORECAST
            # =========================
            st.markdown("### ⏰ Hourly Forecast")

            cols = st.columns(6)

            for i, item in enumerate(forecast_data["list"][:6]):

                time = (
                    datetime.utcfromtimestamp(item["dt"])
                    + timedelta(seconds=timezone_offset)
                ).strftime("%I %p")

                t = round(item["main"]["temp"])

                w = item["weather"][0]["main"]

                icon = "☀️"

                if "cloud" in w.lower():
                    icon = "☁️"

                elif "rain" in w.lower():
                    icon = "🌧"

                elif "thunder" in w.lower():
                    icon = "⛈"

                cols[i].markdown(f"""
                <div class='card'>
                    <b>{time}</b>
                    <br><br>
                    {icon}
                    <br>
                    <b>{t}°</b>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # =========================
            # 🔮 WEATHER PREDICTION
            # =========================
            if st.button("🔮 Predict Tomorrow Weather"):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in weather.lower():
                    prediction = "🌧 Rain Expected Tomorrow"

                elif "thunder" in weather.lower():
                    prediction = "⛈ Thunderstorm Chances Tomorrow"

                elif humidity > 85 and wind_speed > 7:
                    prediction = "⛈ Storm Chances Tomorrow"

                elif humidity > 70:
                    prediction = "☁️ Cloudy Weather Tomorrow"

                elif temp > 35:
                    prediction = "🥵 Very Hot Weather Tomorrow"

                elif temp < 18:
                    prediction = "❄️ Cold Weather Tomorrow"

                elif "clear" in weather.lower():
                    prediction = "☀️ Clear & Pleasant Tomorrow"

                st.markdown(f"""
                <div class='prediction-card'>
                    🔮 Tomorrow Prediction
                    <br><br>
                    {prediction}
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ Weather data not found")

    except Exception as e:
        st.error(f"❌ Error fetching weather: {e}")

# =========================
# 🌟 FOOTER
# =========================
st.markdown("""
<hr>

<div style='text-align:center;font-size:18px;'>
🌟 By <b style='color:#FFD700;'>Samyak M</b>
</div>
""", unsafe_allow_html=True)
