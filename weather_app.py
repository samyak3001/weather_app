import streamlit as st
import requests
from datetime import datetime, timedelta

API_KEY = "96c73ea634856d67ace6716d27c2662e"

st.set_page_config(page_title="iWeather", layout="centered")

# 🎨 Dynamic Background Function
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

# 🎨 UI Styling
st.markdown("""
<style>
.stApp { color: white; }

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.temp {
    font-size: 85px;
    text-align: center;
    font-weight: 300;
}

.center { text-align: center; }

.card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌤 iWeather</div>", unsafe_allow_html=True)

# 🔍 SEARCH
search = st.text_input("🔍 Search City")

city = None
lat = lon = None

if search:
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=5&appid={API_KEY}"
    geo_data = requests.get(geo_url).json()

    if geo_data:
        options = [
            f"{c['name']}, {c.get('state','')}, {c['country']}".replace(" ,","")
            for c in geo_data
        ]

        selected = st.selectbox("Select City", options)

        selected_city = geo_data[options.index(selected)]
        city = selected_city["name"]
        lat = selected_city["lat"]
        lon = selected_city["lon"]

# 🚀 WEATHER
if lat and lon:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    forecast_data = requests.get(forecast_url).json()

    if data.get("cod") == 200:
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        # 🎨 Background
        bg = get_bg(weather, temp)

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{bg}");
            background-size: cover;
            background-position: center;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.45);
            backdrop-filter: blur(6px);
        }}
        </style>
        """, unsafe_allow_html=True)

        # 🕒 CURRENT LOCAL TIME (FIXED)
        timezone_offset = data["timezone"]
        utc_time = datetime.utcnow()
        local_time = utc_time + timedelta(seconds=timezone_offset)

        current_time = local_time.strftime("%I:%M %p")
        current_date = local_time.strftime("%A, %d %B")

        # 📍 DISPLAY
        st.markdown(f"<h2 class='center'>{selected}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='center'>{current_date}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='center' style='font-size:20px;'>🕒 {current_time}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='temp'>{temp}°</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='center'>{weather}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='center'>H:{data['main']['temp_max']}°  L:{data['main']['temp_min']}°</div>", unsafe_allow_html=True)

        st.markdown("---")

        # 🌅 Sunrise & Sunset (FIXED TIMEZONE)
        sunrise = (datetime.utcfromtimestamp(data["sys"]["sunrise"]) + timedelta(seconds=timezone_offset)).strftime("%I:%M %p")
        sunset = (datetime.utcfromtimestamp(data["sys"]["sunset"]) + timedelta(seconds=timezone_offset)).strftime("%I:%M %p")

        col1, col2 = st.columns(2)

        col1.markdown(f"<div class='card'>🌅 Sunrise<br><b>{sunrise}</b></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'>🌇 Sunset<br><b>{sunset}</b></div>", unsafe_allow_html=True)

        st.markdown("---")

        # ⏰ Hourly
        st.markdown("### ⏰ Hourly Forecast")

        cols = st.columns(6)

        for i, item in enumerate(forecast_data["list"][:6]):
            time = (datetime.utcfromtimestamp(item["dt"]) + timedelta(seconds=timezone_offset)).strftime("%I %p")
            t = item["main"]["temp"]
            w = item["weather"][0]["main"]

            icon = "☀️"
            if "cloud" in w.lower():
                icon = "☁️"
            elif "rain" in w.lower():
                icon = "🌧"

            cols[i].markdown(f"""
            <div class='card'>
                <b>{time}</b><br><br>
                {icon}<br>
                {t}°
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("City not found")

# 🌟 Footer
st.markdown("""
<hr>
<div style='text-align:center'>
🌟 By <b style='color:#FFD700;'>Samyak M</b>
</div>
""", unsafe_allow_html=True)