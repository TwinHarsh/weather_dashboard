def get_detailed_recommendation(data):
    recommendations = []

    weather_main = data["weather"][0]["main"]
    weather_desc = data["weather"][0]["description"].lower()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    wind_speed = data["wind"]["speed"]

    # Weather-based suggestions
    if weather_main == "Clear":
        if "sky" in weather_desc:
            recommendations.append("🌞 Clear sky — great time for outdoor activities. Don't forget sunglasses!")
    elif weather_main == "Clouds":
        if "scattered" in weather_desc:
            recommendations.append("⛅ Scattered clouds — a pleasant day with some sun.")
        elif "broken" in weather_desc:
            recommendations.append("🌥️ Broken clouds — mild sunlight, enjoy your walk.")
        elif "overcast" in weather_desc:
            recommendations.append("☁️ Overcast sky — might feel gloomy, consider indoor plans.")
        else:
            recommendations.append("🌤️ Partly cloudy — good time for light outdoor activities.")
    elif weather_main == "Rain":
        if "light" in weather_desc:
            recommendations.append("🌦️ Light rain — carry an umbrella just in case.")
        elif "moderate" in weather_desc:
            recommendations.append("🌧️ Moderate rain — wear a raincoat or stay sheltered.")
        elif "heavy" in weather_desc or "shower" in weather_desc:
            recommendations.append("🌧️ Heavy rain — avoid traveling unless necessary.")
        else:
            recommendations.append("🌦️ Rainy conditions — stay dry and alert.")
    elif weather_main == "Drizzle":
        recommendations.append("🌦️ Drizzling — keep an umbrella handy.")
    elif weather_main == "Thunderstorm":
        recommendations.append("⛈️ Thunderstorm — stay indoors, avoid using electronics.")
    elif weather_main == "Snow":
        recommendations.append("❄️ Snowy weather — dress warmly and drive carefully.")
    elif weather_main in ["Mist", "Fog", "Haze"]:
        recommendations.append("🌫️ Low visibility due to mist/fog — be cautious while driving.")
    elif weather_main == "Smoke":
        recommendations.append("🚭 Smoky air — avoid outdoor exercises.")
    elif weather_main == "Dust":
        recommendations.append("🌪️ Dusty — wear a mask if you go outside.")
    elif weather_main == "Sand":
        recommendations.append("🌬️ Sand in the air — avoid long outdoor exposure.")

    # Temperature-based suggestions
    if temp >= 35:
        recommendations.append("🥵 It's extremely hot — stay hydrated, wear light clothes.")
    elif 30 <= temp < 35:
        recommendations.append("🌡️ Quite warm — apply sunscreen and drink water.")
    elif 20 <= temp < 30:
        recommendations.append("😌 Pleasant temperature — enjoy the outdoors!")
    elif 10 <= temp < 20:
        recommendations.append("🧥 Mildly cold — consider a light jacket.")
    elif 0 <= temp < 10:
        recommendations.append("🧊 Cold — wear warm clothing.")
    else:
        recommendations.append("❄️ Freezing temperatures — bundle up heavily!")

    # Feels-like temperature gap
    if abs(temp - feels_like) > 3:
        if feels_like > temp:
            recommendations.append("📈 Feels hotter than it is — dress lighter.")
        else:
            recommendations.append("📉 Feels colder than it is — add a layer.")

    # Wind conditions
    if wind_speed >= 10:
        recommendations.append("💨 It's windy — avoid loose clothing outdoors.")
    elif wind_speed >= 20:
        recommendations.append("🌬️ Very strong winds — avoid staying under trees or signboards.")

    return recommendations
