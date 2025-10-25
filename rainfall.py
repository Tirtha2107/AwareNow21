# import streamlit as st
# import requests
# import folium
# from streamlit_folium import folium_static

# st.set_page_config(page_title="Weather Map", layout="wide")

# API_KEY = "c24f70a890c583d233cbd498262f6294"
# CITY = "Mumbai"

# def fetch_coords(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}"
#     data = requests.get(url).json()
#     return data['coord']['lat'], data['coord']['lon'] if data.get("cod") == 200 else (None, None)

# def add_layers(map_obj):
#     layers = {
#         "Clouds": "clouds_new",
#         "Rain": "precipitation_new",
#         "Wind": "wind_new"
#     }
#     for name, layer in layers.items():
#         folium.raster_layers.TileLayer(
#             tiles=f"https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
#             attr="OpenWeatherMap", name=name, overlay=True
#         ).add_to(map_obj)

# st.title(" Weather Overlays")

# if st.button("Show Map"):
#     lat, lon = fetch_coords(CITY)
#     if lat and lon:
#         m = folium.Map(location=[lat, lon], zoom_start=6)
#         folium.Marker([lat, lon], popup=CITY).add_to(m)
#         add_layers(m)
#         folium.LayerControl().add_to(m)
#         folium_static(m, width=700, height=500)
#     else:
#         st.error("Unable to fetch location.")

import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# App config
st.set_page_config(page_title="Weather Map", layout="wide")
API_KEY = "c24f70a890c583d233cbd498262f6294"

# Function to fetch coordinates and weather info
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    if data.get("cod") == 200:
        coords = data['coord']['lat'], data['coord']['lon']
        weather_info = {
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description'].title(),
            "icon": data['weather'][0]['icon']
        }
        return coords, weather_info
    else:
        return (None, None), None

# Function to add weather layers
def add_layers(map_obj):
    layers = {
        "Clouds": "clouds_new",
        "Rain": "precipitation_new",
        "Wind": "wind_new",
        "Temperature": "temp_new",
        "Pressure": "pressure_new",
        "Snow": "snow_new"
    }
    for name, layer in layers.items():
        folium.raster_layers.TileLayer(
            tiles=f"https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={API_KEY}",
            attr="OpenWeatherMap", name=name, overlay=True
        ).add_to(map_obj)

# UI
st.title("🌦 Interactive Weather Map")

city = st.text_input("Enter city name:", "Mumbai")
zoom_level = st.slider("Zoom Level", 4, 12, 6)
map_style = st.selectbox("Map Style", ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"])

if st.button("Show Weather Map"):
    with st.spinner("Fetching weather data..."):
        (lat, lon), weather_info = fetch_weather(city)
        
        if lat and lon:
            m = folium.Map(location=[lat, lon], zoom_start=zoom_level, tiles=map_style)
            
            # Add weather layers
            add_layers(m)
            
            # Add marker with weather info
            icon_url = f"http://openweathermap.org/img/wn/{weather_info['icon']}@2x.png"
            popup_html = f"""
            <b>{city}</b><br>
            🌡 Temperature: {weather_info['temperature']}°C<br>
            💧 Humidity: {weather_info['humidity']}%<br>
            🌥 Condition: {weather_info['description']}<br>
            <img src="{icon_url}" width="50">
            """
            folium.Marker(
                [lat, lon],
                popup=popup_html,
                icon=folium.CustomIcon(icon_url, icon_size=(50, 50))
            ).add_to(m)
            
            folium.LayerControl().add_to(m)
            folium_static(m, width=900, height=600)
        else:
            st.error("❌ Unable to fetch location. Check city name.")
