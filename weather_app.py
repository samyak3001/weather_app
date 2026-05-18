import streamlit as st
import requests
from datetime import datetime, timedelta

# =========================================================
# 🔑 OPENWEATHER API KEY
# =========================================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# =========================================================
# 🌤 PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌤",
    layout="wide"
)

# =========================================================
# 🎨 SMART WEATHER BACKGROUND
# =========================================================
def get_background(weather, temp, current_hour):

    weather = weather.lower()

    # 🌙 CLEAR NIGHT
    if "clear" in weather and (current_hour >= 18 or current_hour <= 5):
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb"

    # ☀️ SUNNY DAY
    elif "clear" in weather:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"

    # ☁️ CLOUDY
    elif "cloud" in weather:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63"

    # 🌧 RAIN
    elif "rain" in weather or "drizzle" in weather:
        return "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0"

    # ⛈ THUNDERSTORM
    elif "thunder" in weather:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22"

    # 🌫 HAZE / MIST / FOG
    elif (
        "mist" in weather
        or "fog" in weather
        or "haze" in weather
        or "smoke" in weather
    ):
        return "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227"

    # ❄️ SNOW
    elif "snow" in weather:
        return "https://images.unsplash.com/photo-1517299321609-52687d1bc55a"

    # 🌤 DEFAULT
    else:
        return "https://images.unsplash.com/photo-1502082553048-f009c37129b9"


# =========================================================
# 🎨 MODERN UI CSS
# =========================================================
st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: white;
}

/* =========================
   MAIN APP
========================= */

.stApp {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =========================
   HIDE STREAMLIT
========================= */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* =========================
   TITLE
========================= */

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 20px;

    text-shadow:
        0px 4px 20px rgba(0,0,0,0.4);
}

/* =========================
   SEARCH INPUT
========================= */

.stTextInput > div > div > input {

    background: rgba(255,255,255,0.15);

    border: 1px solid rgba(255,255,255,0.2);

    color: white;

    border-radius: 18px;

    padding: 16px;

    font-size: 18px;

    backdrop-filter: blur(10px);
}

/* =========================
   SELECTBOX
========================= */

.stSelectbox > div > div {

    background: rgba(255,255,255,0.15);

    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.2);

    backdrop-filter: blur(10px);
}

/* =========================
   GLASS CARD
========================= */

.glass {

    background: rgba(255,255,255,0.12);

    border: 1px solid rgba(255,255,255,0.18);

    backdrop-filter: blur(16px);

    -webkit-backdrop-filter: blur(16px);

    border-radius: 28px;

    padding: 25px;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.25);
}

/* =========================
   TEMPERATURE
========================= */

.temp {
    font-size: 120px;
    font-weight: 300;
    text-align: center;
}

/* =========================
   WEATHER TEXT
========================= */

.weather-text {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
}

/* =========================
   DETAIL CARDS
========================= */

.detail-card {

    background: rgba(255,255,255,0.12);

    border: 1px solid rgba(255,255,255,0.15);

    backdrop-filter: blur(14px);

    border-radius: 22px;

    padding: 20px;

    text-align: center;

    margin-top: 10px;
}

/* =========================
   BUTTON
========================= */

.stButton > button {

    width: 100%;

    height: 60px;

    border-radius: 18px;

    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.25),
        rgba(255,255,255,0.12)
    );

    color: white;

    font-size: 20px;

    font-weight: bold;

    border: none;

    transition: 0.3s ease;
}

.stButton > button:hover {

    transform: scale(1.02);

    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.35),
        rgba(255,255,255,0.18)
    );
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 🌤 APP TITLE
# =========================================================
st.markdown(
    "<div class='main-title'>🌤 iWeather</div>",
    unsafe_allow_html=True
)

# =========================================================
# 🔍 SEARCH CITY
# =========================================================
search_city = st.text_input(
    "📍 Search City",
    placeholder="Search any city in the world..."
)

lat = None
lon = None
selected_city_name = None

# =========================================================
# 🌍 GEO LOCATION
# =========================================================
if search_city:

    try:

        geo_url = (
            f"https://api.openweathermap.org/geo/1.0/direct?"
            f"q={search_city}&limit=5&appid={API_KEY}"
        )

        geo_response = requests.get(
            geo_url,
            timeout=10
        )

        if geo_response.status_code == 200:

            geo_data = geo_response.json()

            if geo_data:

                options = [
                    f"{c['name']}, {c.get('state','')}, {c['country']}".replace(" ,", "")
                    for c in geo_data
                ]

                # =========================================================
                # SINGLE CITY
                # =========================================================
                if len(options) == 1:

                    selected_city_name = options[0]

                    selected_city = geo_data[0]

                else:

                    selected_city_name = st.selectbox(
                        "🌍 Select Location",
                        options
                    )

                    selected_city = geo_data[
                        options.index(selected_city_name)
                    ]

                lat = selected_city["lat"]
                lon = selected_city["lon"]

            else:
                st.warning("⚠️ City not found")

        else:
            st.error("❌ Failed to fetch location")

    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# =========================================================
# 🌦 WEATHER SECTION
# =========================================================
if lat is not None and lon is not None:

    try:

        # WEATHER API
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        # FORECAST API
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast?"
            f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        weather_response = requests.get(
            weather_url,
            timeout=10
        )

        forecast_response = requests.get(
            forecast_url,
            timeout=10
        )

        data = weather_response.json()
        forecast_data = forecast_response.json()

        if data.get("cod") == 200:

            # =========================================================
            # WEATHER VALUES
            # =========================================================
            temp = round(data["main"]["temp"])

            humidity = data["main"]["humidity"]

            feels_like = round(data["main"]["feels_like"])

            pressure = data["main"]["pressure"]

            weather = data["weather"][0]["description"]

            wind_speed = data["wind"]["speed"]

            visibility = data.get("visibility", 0) / 1000

            timezone_offset = data["timezone"]

            # =========================================================
            # 🕒 LOCAL TIME
            # =========================================================
            utc_time = datetime.utcnow()

            local_time = utc_time + timedelta(
                seconds=timezone_offset
            )

            current_time = local_time.strftime(
                "%I:%M %p"
            )

            current_date = local_time.strftime(
                "%A, %d %B"
            )

            current_hour = local_time.hour

            # =========================================================
            # 🎨 DYNAMIC BACKGROUND
            # =========================================================
            bg = get_background(
                weather,
                temp,
                current_hour
            )

            st.markdown(f"""
            <style>

            .stApp {{
                background:
                    linear-gradient(
                        rgba(0,0,0,0.35),
                        rgba(0,0,0,0.35)
                    ),
                    url("{bg}");

                background-size: cover;

                background-position: center;

                background-repeat: no-repeat;

                background-attachment: fixed;
            }}

            </style>
            """, unsafe_allow_html=True)

            # =========================================================
            # 🌤 MAIN WEATHER CARD
            # =========================================================
            st.markdown("<div class='glass'>", unsafe_allow_html=True)

            st.markdown(
                f"<h1 style='text-align:center;'>📍 {selected_city_name}</h1>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align:center;font-size:22px;'>"
                f"{current_date}"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align:center;font-size:22px;'>"
                f"🕒 {current_time}"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='temp'>{temp}°</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='weather-text'>"
                f"{weather.title()}"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div style='text-align:center;font-size:22px;'>"
                f"H:{round(data['main']['temp_max'])}° "
                f"L:{round(data['main']['temp_min'])}°"
                f"</div>",
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.write("")

            # =========================================================
            # 📊 WEATHER DETAILS
            # =========================================================
            st.subheader("📊 Weather Details")

            c1, c2, c3, c4, c5 = st.columns(5)

            cards = [
                ("💧 Humidity", f"{humidity}%"),
                ("🌬 Wind", f"{wind_speed} m/s"),
                ("👀 Visibility", f"{visibility} km"),
                ("🤗 Feels Like", f"{feels_like}°"),
                ("📈 Pressure", f"{pressure} hPa")
            ]

            for col, (title, value) in zip(
                [c1, c2, c3, c4, c5],
                cards
            ):

                col.markdown(f"""
                <div class='detail-card'>
                    <h3>{title}</h3>
                    <h2>{value}</h2>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # =========================================================
            # 🌅 SUNRISE & SUNSET
            # =========================================================
            sunrise = (
                datetime.utcfromtimestamp(
                    data["sys"]["sunrise"]
                )
                + timedelta(seconds=timezone_offset)
            ).strftime("%I:%M %p")

            sunset = (
                datetime.utcfromtimestamp(
                    data["sys"]["sunset"]
                )
                + timedelta(seconds=timezone_offset)
            ).strftime("%I:%M %p")

            st.subheader("🌅 Sun Timing")

            s1, s2 = st.columns(2)

            s1.markdown(f"""
            <div class='detail-card'>
                <h3>🌅 Sunrise</h3>
                <h2>{sunrise}</h2>
            </div>
            """, unsafe_allow_html=True)

            s2.markdown(f"""
            <div class='detail-card'>
                <h3>🌇 Sunset</h3>
                <h2>{sunset}</h2>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            # =========================================================
            # ⏰ HOURLY FORECAST
            # =========================================================
            st.subheader("⏰ Hourly Forecast")

            cols = st.columns(6)

            for i, item in enumerate(
                forecast_data["list"][:6]
            ):

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

                elif "snow" in w.lower():
                    icon = "❄️"

                cols[i].markdown(f"""
                <div class='detail-card'>
                    <h4>{time}</h4>
                    <h1>{icon}</h1>
                    <h3>{t}°</h3>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # =========================================================
            # 🔮 WEATHER PREDICTION
            # =========================================================
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

                st.markdown(f"""
                <div class='glass'>
                    <h1 style='text-align:center;'>
                    🔮 {prediction}
                    </h1>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ Weather data unavailable")

    except requests.exceptions.Timeout:
        st.error("⏳ Weather request timed out")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# =========================================================
# 🌟 FOOTER
# =========================================================
st.write("")

st.markdown("""
<div style='
text-align:center;
padding:20px;
font-size:18px;
font-weight:600;
'>
🌟 Designed By <span style='color:#FFD700;'>Samyak M</span>
</div>
""", unsafe_allow_html=True)
