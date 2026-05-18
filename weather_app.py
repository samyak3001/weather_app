import streamlit as st
import requests
from datetime import datetime, timedelta

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="iWeather",
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
def weather_icon(condition, hour=None):

    condition = condition.lower()

    if "clear" in condition:
        if hour and (hour >= 18 or hour <= 5):
            return "🌙"
        return "☀️"

    if "cloud" in condition:
        return "☁️"

    if "drizzle" in condition:
        return "🌦"

    if "rain" in condition:
        return "🌧"

    if "thunder" in condition:
        return "⛈"

    if "snow" in condition:
        return "❄️"

    if (
        "mist" in condition
        or "fog" in condition
        or "haze" in condition
    ):
        return "🌫"

    return "☀️"


# =====================================================
# BACKGROUND
# =====================================================
def get_background(condition, hour):

    condition = condition.lower()

    if "clear" in condition and (hour >= 18 or hour <= 5):
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920"

    elif "clear" in condition:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920"

    elif "cloud" in condition:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?w=1920"

    elif "rain" in condition:
        return "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1920"

    elif "thunder" in condition:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22?w=1920"

    elif "snow" in condition:
        return "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=1920"

    elif (
        "mist" in condition
        or "fog" in condition
        or "haze" in condition
    ):
        return "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?w=1920"

    return "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"


# =====================================================
# CACHE
# =====================================================
@st.cache_data(ttl=600)
def fetch_city(city):

    url = (
        f"https://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=5&appid={API_KEY}"
    )

    return requests.get(url).json()


@st.cache_data(ttl=600)
def fetch_weather(lat, lon):

    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    weather = requests.get(weather_url).json()
    forecast = requests.get(forecast_url).json()

    return weather, forecast


# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>

/* GLOBAL */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: white;
}

/* HIDE */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* APP */

.stApp {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* TITLE */

.title {
    text-align:center;
    font-size:70px;
    font-weight:700;
    margin-bottom:30px;
    text-shadow:0px 4px 20px rgba(0,0,0,0.5);
}

/* INPUT */

.stTextInput input {

    background: rgba(20,20,30,0.45);

    border: 1px solid rgba(255,255,255,0.2);

    border-radius:18px;

    color:white;

    padding:16px;

    font-size:18px;

    backdrop-filter: blur(15px);
}

/* SELECT */

.stSelectbox div[data-baseweb="select"] {

    background: rgba(20,20,30,0.45);

    border-radius:18px;

    backdrop-filter: blur(15px);
}

/* GLASS */

.glass {

    background: rgba(20,20,30,0.45);

    border: 1px solid rgba(255,255,255,0.18);

    border-radius:30px;

    padding:30px;

    backdrop-filter: blur(18px);

    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* CARDS */

.card {

    background: rgba(20,20,30,0.45);

    border: 1px solid rgba(255,255,255,0.15);

    border-radius:24px;

    padding:20px;

    text-align:center;

    backdrop-filter: blur(15px);

    margin-top:10px;
}

/* TEMP */

.temp {
    font-size:130px;
    font-weight:300;
    text-align:center;
}

/* BUTTON */

.stButton button {

    width:100%;

    height:60px;

    border:none;

    border-radius:18px;

    font-size:20px;

    font-weight:bold;

    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.25),
        rgba(255,255,255,0.12)
    );

    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown(
    "<div class='title'>🌦 iWeather</div>",
    unsafe_allow_html=True
)

# =====================================================
# SEARCH
# =====================================================
city_input = st.text_input(
    "📍 Search City",
    placeholder="Enter city name..."
)

lat = None
lon = None
selected_name = None

# =====================================================
# CITY SEARCH
# =====================================================
if city_input:

    try:

        cities = fetch_city(city_input)

        if cities:

            names = [
                f"{c['name']}, {c.get('state','')}, {c['country']}".replace(" ,", "")
                for c in cities
            ]

            if len(names) == 1:

                selected_name = names[0]
                selected_city = cities[0]

            else:

                selected_name = st.selectbox(
                    "🌍 Select Location",
                    names
                )

                selected_city = cities[
                    names.index(selected_name)
                ]

            lat = selected_city["lat"]
            lon = selected_city["lon"]

        else:
            st.warning("City not found")

    except:
        st.error("Failed to search city")

# =====================================================
# WEATHER
# =====================================================
if lat and lon:

    try:

        with st.spinner("Fetching weather..."):

            data, forecast = fetch_weather(
                lat,
                lon
            )

        if data.get("cod") == 200:

            # WEATHER VALUES
            temp = round(data["main"]["temp"])

            feels = round(data["main"]["feels_like"])

            humidity = data["main"]["humidity"]

            pressure = data["main"]["pressure"]

            wind = data["wind"]["speed"]

            visibility = data.get("visibility", 0) / 1000

            condition = data["weather"][0]["description"]

            timezone = data["timezone"]

            # TIME
            utc = datetime.utcnow()

            local = utc + timedelta(
                seconds=timezone
            )

            hour = local.hour

            date = local.strftime(
                "%A, %d %B"
            )

            time_now = local.strftime(
                "%I:%M %p"
            )

            # BACKGROUND
            bg = get_background(
                condition,
                hour
            )

            st.markdown(f"""
            <style>

            .stApp {{
                background:
                    linear-gradient(
                        rgba(0,0,0,0.45),
                        rgba(0,0,0,0.45)
                    ),
                    url("{bg}");

                background-size:cover;
                background-position:center;
            }}

            </style>
            """, unsafe_allow_html=True)

            icon = weather_icon(
                condition,
                hour
            )

            # =====================================================
            # MAIN CARD
            # =====================================================
            st.markdown(
                f"""
                <div class="glass">

                    <h1 style="text-align:center;">
                        {icon} {selected_name}
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
                        {condition.title()}
                    </h2>

                    <h3 style="text-align:center;">
                        H:{round(data['main']['temp_max'])}°
                        L:{round(data['main']['temp_min'])}°
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

            c1, c2, c3 = st.columns(3)

            c1.markdown(
                f"""
                <div class="card">
                    <h3>💧 Humidity</h3>
                    <h2>{humidity}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            c2.markdown(
                f"""
                <div class="card">
                    <h3>🌬 Wind</h3>
                    <h2>{wind} m/s</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            c3.markdown(
                f"""
                <div class="card">
                    <h3>👀 Visibility</h3>
                    <h2>{visibility} km</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            c4, c5 = st.columns(2)

            c4.markdown(
                f"""
                <div class="card">
                    <h3>🤗 Feels Like</h3>
                    <h2>{feels}°</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            c5.markdown(
                f"""
                <div class="card">
                    <h3>📈 Pressure</h3>
                    <h2>{pressure} hPa</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # =====================================================
            # SUNRISE SUNSET
            # =====================================================
            sunrise = (
                datetime.utcfromtimestamp(
                    data["sys"]["sunrise"]
                )
                + timedelta(seconds=timezone)
            ).strftime("%I:%M %p")

            sunset = (
                datetime.utcfromtimestamp(
                    data["sys"]["sunset"]
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

            cols = st.columns(6)

            for col, item in zip(cols, hourly):

                forecast_time = (
                    datetime.utcfromtimestamp(item["dt"])
                    + timedelta(seconds=timezone)
                )

                forecast_hour = forecast_time.hour

                display_time = forecast_time.strftime(
                    "%I %p"
                )

                forecast_temp = round(
                    item["main"]["temp"]
                )

                forecast_condition = item[
                    "weather"
                ][0]["main"]

                forecast_desc = item[
                    "weather"
                ][0]["description"]

                forecast_icon = weather_icon(
                    forecast_condition,
                    forecast_hour
                )

                card_html = f"""
                <div class="card">

                    <h3>{display_time}</h3>

                    <div style="font-size:50px;">
                        {forecast_icon}
                    </div>

                    <h2>{forecast_temp}°</h2>

                    <p style="
                        font-size:14px;
                        opacity:0.8;
                    ">
                        {forecast_desc.title()}
                    </p>

                </div>
                """

                col.markdown(
                    card_html,
                    unsafe_allow_html=True
                )

            st.write("")

            # =====================================================
            # PREDICTION
            # =====================================================
            if st.button(
                "🔮 Predict Tomorrow Weather"
            ):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in condition.lower():
                    prediction = "🌧 Rain Expected Tomorrow"

                elif "cloud" in condition.lower():
                    prediction = "☁️ Cloudy Tomorrow"

                elif "thunder" in condition.lower():
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

    except:
        st.error("Unable to fetch weather")

# =====================================================
# FOOTER
# =====================================================
st.write("")

st.markdown("""
<div style="
text-align:center;
padding:20px;
font-size:18px;
font-weight:600;
">
🌟 Designed By
<span style="color:#FFD700;">
Samyak M
</span>
</div>
""", unsafe_allow_html=True)
