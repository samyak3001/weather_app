import streamlit as st
import requests
from datetime import datetime, timedelta

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="iWeather",
    page_icon="🌦",
    layout="wide"
)

# ============================================
# API KEY
# ============================================
API_KEY = "96c73ea634856d67ace6716d27c2662e"

# ============================================
# WEATHER ICONS
# ============================================
def get_icon(condition, hour):

    condition = condition.lower()

    if "clear" in condition:
        return "🌙" if hour >= 18 or hour <= 5 else "☀️"

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


# ============================================
# BACKGROUND
# ============================================
def get_bg(condition, hour):

    condition = condition.lower()

    if "clear" in condition and (hour >= 18 or hour <= 5):
        return "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920"

    if "clear" in condition:
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920"

    if "cloud" in condition:
        return "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?w=1920"

    if "rain" in condition:
        return "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=1920"

    if "thunder" in condition:
        return "https://images.unsplash.com/photo-1500673922987-e212871fec22?w=1920"

    if (
        "mist" in condition
        or "fog" in condition
        or "haze" in condition
    ):
        return "https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?w=1920"

    return "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=1920"


# ============================================
# API FUNCTIONS
# ============================================
@st.cache_data(ttl=600)
def get_city(city):

    url = (
        f"https://api.openweathermap.org/geo/1.0/direct?"
        f"q={city}&limit=5&appid={API_KEY}"
    )

    return requests.get(url).json()


@st.cache_data(ttl=600)
def get_weather(lat, lon):

    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}"
        f"&appid={API_KEY}&units=metric"
    )

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}"
        f"&appid={API_KEY}&units=metric"
    )

    weather = requests.get(weather_url).json()
    forecast = requests.get(forecast_url).json()

    return weather, forecast


# ============================================
# CSS
# ============================================
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
    font-size: 70px;
    font-weight: bold;
    margin-bottom: 25px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.glass, .card {
    background: rgba(20,20,30,0.45);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 25px;
    backdrop-filter: blur(16px);
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

.card {
    text-align: center;
    margin-top: 10px;
}

.temp {
    font-size: 120px;
    font-weight: 300;
    text-align: center;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background: rgba(20,20,30,0.45);
    color: white;
    border-radius: 18px;
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

# ============================================
# TITLE
# ============================================
st.markdown(
    "<div class='title'>🌦 iWeather</div>",
    unsafe_allow_html=True
)

# ============================================
# SEARCH
# ============================================
city_name = st.text_input(
    "📍 Search City",
    placeholder="Enter city..."
)

lat, lon = None, None

# ============================================
# CITY SEARCH
# ============================================
if city_name:

    cities = get_city(city_name)

    if cities:

        options = [
            f"{c['name']}, {c.get('state','')}, {c['country']}".replace(" ,", "")
            for c in cities
        ]

        selected = st.selectbox(
            "🌍 Select Location",
            options
        )

        city = cities[options.index(selected)]

        lat = city["lat"]
        lon = city["lon"]

    else:
        st.error("City not found")

# ============================================
# WEATHER
# ============================================
if lat and lon:

    try:

        data, forecast = get_weather(lat, lon)

        if data.get("cod") == 200:

            temp = round(data["main"]["temp"])

            feels = round(
                data["main"]["feels_like"]
            )

            humidity = data["main"]["humidity"]

            pressure = data["main"]["pressure"]

            wind = data["wind"]["speed"]

            visibility = (
                data.get("visibility", 0) / 1000
            )

            condition = data["weather"][0]["description"]

            timezone = data["timezone"]

            local = datetime.utcnow() + timedelta(
                seconds=timezone
            )

            hour = local.hour

            date = local.strftime(
                "%A, %d %B"
            )

            time_now = local.strftime(
                "%I:%M %p"
            )

            icon = get_icon(
                condition,
                hour
            )

            bg = get_bg(
                condition,
                hour
            )

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
                        {icon} {selected}
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
                        &nbsp;
                        L:{round(data['main']['temp_min'])}°
                    </h3>

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

            for col, (title, value) in zip(
                cols,
                details
            ):

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

            # SUNRISE SUNSET
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

            # FORECAST
            st.subheader("⏰ Hourly Forecast")

            forecast_items = forecast["list"][:6]

            cols = st.columns(6)

            for col, item in zip(cols, forecast_items):

                f_time = (
                    datetime.utcfromtimestamp(
                        item["dt"]
                    )
                    + timedelta(seconds=timezone)
                )

                f_hour = f_time.hour

                display_time = f_time.strftime(
                    "%I %p"
                )

                f_temp = round(
                    item["main"]["temp"]
                )

                f_condition = item[
                    "weather"
                ][0]["description"]

                f_icon = get_icon(
                    f_condition,
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

                        <p>{f_condition.title()}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            # PREDICTION
            if st.button(
                "🔮 Predict Tomorrow Weather"
            ):

                prediction = "☀️ Sunny Tomorrow"

                if "rain" in condition:
                    prediction = "🌧 Rain Expected Tomorrow"

                elif "cloud" in condition:
                    prediction = "☁️ Cloudy Tomorrow"

                elif "thunder" in condition:
                    prediction = "⛈ Storm Chances Tomorrow"

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

# ============================================
# FOOTER
# ============================================
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
