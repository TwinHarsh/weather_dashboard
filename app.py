import streamlit as st
import requests
import plotly.graph_objects as go
import datetime
from background import set_background
from recommendation import get_detailed_recommendation


#weather fetch func
def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return {"error": f"City not found or API error ({response.status_code})"}

    data = response.json()

    # 5-day / 3-hour forecast
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    forecast_params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    forecast_response = requests.get(forecast_url, params=forecast_params)
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        data["forecast"] = forecast_data["list"]
    return data

#fetching air-quality
def get_air_quality(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        aqi = data["list"][0]["main"]["aqi"]
        return aqi
    else:
        return None
    
aqi_levels = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor"
}

    


# Streamlit UI
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="centered")
st.title("🌤️ Weather Dashboard")
st.sidebar.title("Weather Dashboard")
st.sidebar.markdown("Choose a city or check history")
set_background()
api_key = st.secrets["API_KEY"]


from history_favorites import save_search, get_search_history, add_favorite, remove_favorite, get_favorites

# Set default state if not exists
if "selected_city" not in st.session_state:
    st.session_state.selected_city = ""

# Sidebar
with st.sidebar:
    st.subheader("📌 Favorites & History")

    favorites = list(get_favorites())
    history = get_search_history()

    if favorites:
        st.markdown("### ⭐ Favorites")
        for fav in favorites:
            if st.button(fav, key=f"fav_{fav}"):
                st.session_state.selected_city = fav

    if history:
        st.markdown("### 🔁 Recent Searches")
        for hist in history:
            if st.button(hist, key=f"hist_{hist}"):
                st.session_state.selected_city = hist


city = st.text_input("Enter City Name", value=st.session_state.selected_city, key="city_input")


if city:
    save_search(city)

col1, col2, _ = st.columns([2, 2, 6])

with col1:
    if st.button("➕ Add"):
        add_favorite(city)
        st.success(f"{city} added to favorites.")

with col2:
    if st.button("❌ Remove"):
        remove_favorite(city)
        st.warning(f"{city} removed from favorites.")



if city:
    data = get_weather(city, api_key)

    if "error" in data:
        st.error(data["error"])
    else:
        
        st.subheader(f"Weather in {city.title()}")

        # Get weather details
        weather_main = data['weather'][0]['main']
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        recommendations = get_detailed_recommendation(data)
        if recommendations:
          st.markdown("### 🧠 Smart Weather Tips")
          for tip in recommendations:
             st.write("- " + tip)

        # Display icon + weather info
        st.image(icon_url, caption=weather_desc.title())
        st.metric("🌡️ Temperature", f"{temp} °C")
        st.metric("💧 Humidity", f"{humidity}%")
        st.metric("🌬️ Wind Speed", f"{wind} m/s")

        # Display the air quality index 
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        aqi = get_air_quality(lat, lon, api_key)

        if aqi:
            aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            st.metric("🌫️ Air Quality Index", f"{aqi} - {aqi_levels[aqi]}")
        else:
            st.warning("Air Quality Index unavailable.")


        if "forecast" in data:
            from collections import defaultdict

            st.subheader("5-Day Temperature Forecast (Averaged)")

            # Group forecast by date
            daily_temps = defaultdict(list)
            for entry in data["forecast"]:
                dt = datetime.datetime.fromtimestamp(entry["dt"])
                date = dt.date()
                temp = entry["main"]["temp"]
                daily_temps[date].append(temp)

            # Prepare for plotting
            dates = []
            avg_temps = []
            max_temps = []

            for date, temps in daily_temps.items():
                dates.append(date.strftime("%a %d"))
                avg_temps.append(sum(temps) / len(temps))
                max_temps.append(max(temps))

            # Plot with Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(x=dates, y=avg_temps, name="Avg Temp (°C)", marker_color="skyblue"))
            fig.add_trace(go.Bar(x=dates, y=max_temps, name="Max Temp (°C)", marker_color="orangered"))

            fig.update_layout(
                title="Daily Avg and Max Temperatures (Next 5 Days)",
                xaxis_title="Day",
                yaxis_title="Temperature (°C)",
                barmode="group",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(
                   color="white",     
                   size=14            
                )
            )
            fig.update_xaxes(tickfont=dict(color='white'))
            fig.update_yaxes(tickfont=dict(color='white'))


            st.plotly_chart(fig, use_container_width=True)

from multi_city import compare_cities_weather

st.header("🏙️ Compare Weather Across Multiple Cities")
multi_input = st.text_input("Enter city names separated by commas (e.g., Delhi, London, New York)")
if multi_input:
    compare_cities_weather(multi_input.split(","), api_key)
