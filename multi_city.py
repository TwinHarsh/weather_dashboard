import requests
import plotly.graph_objects as go
import streamlit as st

def fetch_city_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city.title(),
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        }
    return None

def compare_cities_weather(city_list, api_key):
    weather_data = []
    for city in city_list:
        result = fetch_city_weather(city.strip(), api_key)
        if result:
            weather_data.append(result)

    if not weather_data:
        st.warning("No valid city data found.")
        return

    # Plotting comparison chart
    cities = [d["city"] for d in weather_data]
    temps = [d["temp"] for d in weather_data]
    humidities = [d["humidity"] for d in weather_data]
    winds = [d["wind"] for d in weather_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=cities, y=temps, name="Temperature (°C)", marker_color="orange",
        text=[f"{t:.1f}°C" for t in temps], textposition='outside'))
    fig.add_trace(go.Bar(
        x=cities, y=humidities, name="Humidity (%)", marker_color="blue",
        text=[f"{h}%" for h in humidities], textposition='outside'))
    fig.add_trace(go.Bar(
        x=cities, y=winds, name="Wind Speed (m/s)", marker_color="green",
        text=[f"{w:.1f} m/s" for w in winds], textposition='outside'))

    fig.update_layout(
        barmode='group',
        title="Multi-City Weather Comparison",
        xaxis_title="City",
        yaxis_title="Value",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)
