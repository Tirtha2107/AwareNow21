
       

from streamlit_option_menu import option_menu
from deep_translator import GoogleTranslator
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from folium.plugins import HeatMap, MarkerCluster
import json
import os
import pandas as pd
import plotly.express as px
from datetime import datetime
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import requests
import openrouteservice
from openrouteservice import convert
import random
from geopy.distance import geodesic

# Import local modules
from home import show_Home
from chartsAnalytics import charts
from predict import prediction
from chatbot import chat
from News import news
from community import Feedback
from emergency import Emergency
from livealert import Live_Alerts
from safety import safety
from Quiz import Quiz
from heatmap import heatmap



def show_dashboard():
    # -------------------
    # Configure Google Gemini
    # -------------------
    api_key = "AIzaSyBBWBIahoh1TrweQuDVfmhnpEtKs5AoJ1E"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    st.set_page_config(page_title="AwareNow", layout="wide")

   
    st.markdown("""
        <style>
        /* Entire Background Gradient */
        html, body, .stApp {
            height: 100%;
            background: linear-gradient(to right, #0f1025 30%, #502b76 100%);
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0f1025;
            padding: 1rem 1rem 1rem 1rem;
            min-width: 300px;
            width: 300px;
        }

        /* Sidebar Header */
        .css-hyum1k {
            color: #f8c94c;
            font-size: 18px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 10px;
        }
        
        /* Menu links */
        .nav-link {
            font-size: 16px !important;
            font-weight: 500 !important;
            color: white !important;
            border-radius: 10px;
            margin: 5px 0;
        }
        .nav-link:hover {
            background-color: #ff7f2a !important;
            color: white !important;
        }
        .nav-link.active {
            background-color: #ff6600 !important;
            color: white !important;
        }

        /* Title */
        h1#awarenow-title {
            text-align: center;
            color: #ffffff;
            font-size: 48px;
            font-weight: 800;
            margin-top: 1.5rem;
            margin-bottom: 0.2rem;
        }

        /* Subtitle */
        .subtitle {
            text-align: center;
            color: #e0e0e0;
            font-size: 20px;
            font-weight: 500;
            margin-bottom: 0.1rem;
        }

        /* Small welcome */
        .small {
            text-align: center;
            font-size: 16px;
            color: #e3e3e3;
            margin-bottom: 2rem;
        }

        /* Dropdown styling */
        label {
            color: white !important;
            font-size: 16px;
        }

        div[data-baseweb="select"] {
            background-color: #1c1c1c !important;
            color: white !important;
            border: 2px solid #6a5acd !important;
            border-radius: 10px !important;
            width: 300px !important;
            margin: 0 auto !important;
        }

        /* Center dropdown */
        .stSelectbox {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 1.5rem;
        }
        
        .stExpander {
            background-color: #333333;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    def translate_text(text, lang_code):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except Exception:
            return text


    lang = st.selectbox("Select Language", ["English", "हिन्दी", "मराठी"])
    lang_code = 'en' if lang == "English" else 'hi' if lang == "हिन्दी" else 'mr'

    T = {
        "title": "AwareNow",
        "subtitle": "Real-Time Local Alert and Safety Information System",
        "welcome": "Welcome to the Home Page!",
        "choose_option": "CHOOSE YOUR OPTION",
        "home": "Home",
        "maps": "Interactive Maps",
        "emergency": "Emergency",
        "safety_info": "Safety Information",
        "charts": "Charts & Analytics",
        "incident": "User Incident Report",
        "prediction": "Prediction",
        "news": "Daily News",
        "chatbot": "ChatBot",
        "quiz": "Quiz",
        "feedback": "Community Feedback",
        "interactive_map": "Interactive Safety Map",
        "heatmap": "Heatmap",
        "markers": "Markers",
        "live_alerts": "Live Alerts",
        "live_travel": "Live Travel",
        "emergency_markers": "Emergency Markers (All India)",
        "enter_area": "Enter Area Name or PIN Code (India)",
        "you_are_here": "You are here",
        "route_facility": "Show Route to Facility",
        "dest_coords": "Enter facility latitude,longitude (from map popup):",
        "route_planner": "AwareNow - Smart Route Planner with Live Alerts",
        "start_loc": "Start Location",
        "dest_loc": "Destination",
        "alert_filters": "Alert Filters",
        "crime_alerts": "Crime Alerts",
        "disaster_alerts": "Disaster Alerts",
        "traffic_alerts": "Traffic Violations",
        "flood_warnings": "Flood Warnings (Simulated)",
        "weather_warnings": "Weather Warnings (Simulated)",
        "plan_route": "Plan Route",
        "route_ready": "Route & Alerts Ready",
        "distance": "Distance",
        "travel_time": "Estimated Travel Time",
        "no_route": "No route found.",
        "invalid_loc": "Invalid start or destination.",
        "emergency_fac": "Emergency Facilities",
        "safety_guidelines": "Safety Guidelines & Precautionary Measures",
        "report_incident": "Report an Incident",
        "category": "Select Incident Category",
        "title_label": "Incident Title",
        "desc_label": "Description of the Incident",
        "location_label": "Location (e.g., Street, City, Pincode)",
        "upload_file": "Upload Image or Video (Optional)",
        "submit_report": "Submit Report",
        "report_success": "Your report has been submitted successfully!",
        "fill_fields": "Please fill in all the fields.",
        "daily_news": "Daily Safety & Local News",
        "ai_assistant": "AI Assistant",
        "quiz_label": "Quiz",
        "feedback_label": "Community Feedback & Suggestions"
    }

    # -------------------
    # Title and Subtitle
    # -------------------
    st.markdown(f"<h1 style='text-align: center; color: #EF3131; font-size: 60px; font-weight: bold;'>{translate_text(T['title'], lang_code)}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{translate_text(T['subtitle'], lang_code)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small'>{translate_text(T['welcome'], lang_code)}</div>", unsafe_allow_html=True)

    # -------------------
    # Sidebar Menu
    # -------------------
    with st.sidebar:
        st.markdown(f"### {translate_text(T['choose_option'], lang_code)}")
        menu_options = [
            translate_text(T['home'], lang_code),
            translate_text(T['maps'], lang_code),
            translate_text(T['emergency'], lang_code),
            translate_text(T['safety_info'], lang_code),
            translate_text(T['charts'], lang_code),
            translate_text(T['incident'], lang_code),
            translate_text(T['prediction'], lang_code),
            translate_text(T['news'], lang_code),
            translate_text(T['chatbot'], lang_code),
            translate_text(T['quiz'], lang_code),
            translate_text(T['feedback'], lang_code)
        ]
        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=[
                "house-fill", "geo-alt-fill", "exclamation-circle-fill",
                "info-circle", "graph-up-arrow", "file-earmark-text-fill",
                "robot", "newspaper", "chat-left-text-fill",
                "question-circle-fill", "people-fill"
            ],
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#25043B"},
                "icon": {"color": "#ff9900", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px 0"},
                "nav-link-selected": {"background-color": "#EF3131", "color": "white"},
            }
        )

    # -------------------
    # Main Navigation
    # -------------------
    if selected == translate_text(T['home'], lang_code):
        show_Home(lang_code)

    elif selected == translate_text("Interactive Maps", lang_code):
        st.text(translate_text("Here is the Interactive Map.", lang_code))
        st.subheader(translate_text("Interactive Safety Map", lang_code))

        ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE3NmIzNGUyZWE1ZDQ4ZWM4N2IxZGQ3N2FhNWI1NTUyIiwiaCI6Im11cm11cjY0In0="   # replace with your OpenRouteService key
        geolocator = Nominatim(user_agent="india_emergency_locator")

        st.set_page_config(layout="wide", page_title="AwareNow")

        ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE3NmIzNGUyZWE1ZDQ4ZWM4N2IxZGQ3N2FhNWI1NTUyIiwiaCI6Im11cm11cjY0In0="

        @st.cache_data
        def get_coordinates(address):
            geolocator = Nominatim(user_agent="route_app")
            try:
                location = geolocator.geocode(f"{address}, India", timeout=10)
                if location:
                    return (location.latitude, location.longitude)
            except:
                return None
            return None

        @st.cache_data
        def get_route(start_coords, end_coords):
            url = "https://api.openrouteservice.org/v2/directions/driving-car"
            headers = {'Authorization': ORS_API_KEY, 'Content-Type': 'application/json'}
            body = {"coordinates": [[start_coords[1], start_coords[0]], [end_coords[1], end_coords[0]]]}
            try:
                response = requests.post(url, headers=headers, data=json.dumps(body))
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                return None

        # Load datasets
        crime_df = pd.read_csv("crime_dataset_india (3).csv")
        disaster_df = pd.read_csv("disasterIND .csv")
        traffic_df = pd.read_csv("Indian_Traffic_Violations.csv")

        # Initialize session state
        for key in ["heatmap", "markers", "alert", "travel"]:
            if key not in st.session_state:
                st.session_state[key] = False

        # Map controls
        with st.expander("Map Controls", expanded=True):
            if st.button("Heatmap"):
                st.session_state.heatmap = not st.session_state.heatmap
            if st.button("Markers"):
                st.session_state.markers = not st.session_state.markers
            if st.button("Live Alerts"):
                st.session_state.alert = not st.session_state.alert
            if st.button("Live Travel"):
                st.session_state.travel = not st.session_state.travel

        # Heatmap feature
        if st.session_state.heatmap:
            st.subheader("Heatmap")
            heatmap()

        # Markers feature
        if st.session_state.markers:
            st.subheader("Markers Feature (Coming Soon)")

            def geocode_place(place):
                try:
                    loc = geolocator.geocode(place, timeout=10)
                    return (loc.latitude, loc.longitude) if loc else None
                except GeocoderTimedOut:
                    return None

            def fetch_overpass(lat, lon, radius=5000):
                query = f"""
                [out:json][timeout:25];
                (
                node["amenity"="hospital"](around:{radius},{lat},{lon});
                node["amenity"="police"](around:{radius},{lat},{lon});
                node["amenity"="shelter"](around:{radius},{lat},{lon});
                node["emergency"="shelter"](around:{radius},{lat},{lon});
                );
                out center;
                """
                r = requests.post("https://overpass-api.de/api/interpreter", data={"data": query})
                return r.json().get("elements", [])

            def plot_facilities(fmap, facilities):
                for el in facilities:
                    lat, lon = el.get("lat"), el.get("lon")
                    tags = el.get("tags", {})
                    typ = "other"
                    if tags.get("amenity") == "hospital":
                        typ = "hospital"
                        color = "red"
                    elif tags.get("amenity") == "police":
                        typ = "police"
                        color = "blue"
                    elif tags.get("emergency") == "shelter" or tags.get("amenity") == "shelter":
                        typ = "shelter"
                        color = "green"
                    else:
                        color = "gray"
                    name = tags.get("name", typ.title())
                    popup = folium.Popup(f"{name} ({typ.title()})<br>Lat: {lat:.5f}, Lon: {lon:.5f}", max_width=250)
                    folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color=color)).add_to(fmap)

            def route_map(start, end):
                client = openrouteservice.Client(key=ORS_API_KEY)
                coords = [start[::-1], end[::-1]]
                route = client.directions(coordinates=coords, profile='driving-car', format='geojson')
                m = folium.Map(location=start, zoom_start=14)
                folium.GeoJson(route, style={"color": "blue", "weight": 5}).add_to(m)
                folium.Marker(start, tooltip="You are here", icon=folium.Icon(color="blue")).add_to(m)
                folium.Marker(end, tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)
                return m

            st.title("Emergency Markers (All India)")
            place = st.text_input("Enter Area Name or PIN Code (India)", placeholder="e.g., Mumbai, 110001")

            if place:
                loc = geocode_place(place)
                if loc:
                    st.success(f"Location found: {loc}")
                    lat, lon = loc
                    fmap = folium.Map(location=loc, zoom_start=14)
                    folium.Marker(loc, tooltip="You are here", icon=folium.Icon(color="blue")).add_to(fmap)

                    facilities = fetch_overpass(lat, lon)
                    if facilities:
                        plot_facilities(fmap, facilities)
                    else:
                        st.warning("No emergency facilities found within 5 km radius.")

                    result = st_folium(fmap, width=800, height=500)

                    # Show routing controls
                    st.markdown("---")
                    st.subheader("Show Route to Facility")
                    dest = st.text_input("Enter facility latitude,longitude (from map popup):")
                    if dest:
                        try:
                            dlat, dlon = map(float, dest.split(","))
                            m2 = route_map(loc, (dlat, dlon))
                            st_folium(m2, width=800, height=500)
                        except:
                            st.error("Invalid format. Use latitude,longitude")
                else:
                    st.error("Could not geocode the location. Try again with a valid place or PIN code.")

        # Live alerts feature
        if st.session_state.alert:
            st.subheader("Live Alerts Feature (Coming Soon)")
            Live_Alerts()

        # Travel planner
        if st.session_state.travel:
            st.title("AwareNow - Smart Route Planner with Live Alerts")

            col1, col2 = st.columns(2)
            start_address = col1.text_input("Start Location", "Pune")
            destination_address = col2.text_input("Destination", "Gateway of India, Mumbai")

            st.header("Alert Filters")
            show_crime = st.checkbox("Crime Alerts", True)
            show_disaster = st.checkbox("Disaster Alerts", True)
            show_traffic = st.checkbox("Traffic Violations", True)
            show_flood = st.checkbox("Flood Warnings (Simulated)", True)
            show_weather = st.checkbox("Weather Warnings (Simulated)", True)

            if st.button("Plan Route"):
                if start_address and destination_address:
                    with st.spinner("Fetching route and alerts..."):
                        start_coords = get_coordinates(start_address)
                        end_coords = get_coordinates(destination_address)

                        if start_coords and end_coords:
                            route_data = get_route(start_coords, end_coords)
                            if route_data and 'routes' in route_data:
                                route = route_data['routes'][0]
                                geometry = convert.decode_polyline(route['geometry'])
                                route_line = [[coord[1], coord[0]] for coord in geometry['coordinates']]

                                # Init map
                                m = folium.Map(location=start_coords, zoom_start=6, tiles="CartoDB positron")
                                folium.Marker(start_coords, icon=folium.Icon(color='green'),
                                            tooltip=f"Start: {start_address}").add_to(m)
                                folium.Marker(end_coords, icon=folium.Icon(color='blue'),
                                            tooltip=f"End: {destination_address}").add_to(m)
                                folium.PolyLine(route_line, color="cyan", weight=5).add_to(m)

                                # Filter zone
                                min_lat = min(start_coords[0], end_coords[0])
                                max_lat = max(start_coords[0], end_coords[0])
                                min_lon = min(start_coords[1], end_coords[1])
                                max_lon = max(start_coords[1], end_coords[1])

                                cluster = MarkerCluster().add_to(m)
                                alert_data = []

                                # Crime alerts
                                if show_crime:
                                    for _, row in crime_df.head(200).iterrows():
                                        city = row.get("City", "")
                                        desc = row.get("Crime Description", "")
                                        coords = get_coordinates(city)
                                        if coords:
                                            lat, lon = coords
                                            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                                                folium.Marker([lat, lon], icon=folium.Icon(color='red'),
                                                            tooltip=f"{desc} in {city}").add_to(cluster)
                                                alert_data.append(["Crime", city, desc])

                                # Disaster alerts
                                if show_disaster:
                                    disaster_df.dropna(subset=["Latitude", "Longitude"], inplace=True)
                                    for _, row in disaster_df.iterrows():
                                        lat, lon = row["Latitude"], row["Longitude"]
                                        dtype = row.get("Disaster Type", "")
                                        loc = row.get("Location", "")
                                        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                                            folium.Marker([lat, lon], icon=folium.Icon(color='orange'),
                                                        tooltip=f"{dtype} at {loc}").add_to(cluster)
                                            alert_data.append(["Disaster", loc, dtype])

                                # Traffic alerts
                                if show_traffic:
                                    traffic_df.dropna(subset=["Location"], inplace=True)
                                    for _, row in traffic_df.iterrows():
                                        location = row["Location"]
                                        coords = get_coordinates(location)
                                        if coords:
                                            lat, lon = coords
                                            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                                                vtype = row.get("Violation_Type", "")
                                                folium.Marker([lat, lon], icon=folium.Icon(color='purple'),
                                                            tooltip=f"{vtype} at {location}").add_to(cluster)
                                                alert_data.append(["Traffic", location, vtype])

                                # Flood alerts (simulated)
                                if show_flood:
                                    for _ in range(10):
                                        lat = random.uniform(min_lat, max_lat)
                                        lon = random.uniform(min_lon, max_lon)
                                        folium.Marker([lat, lon], icon=folium.Icon(color='blue'),
                                                    tooltip="Flood Alert (Simulated)").add_to(cluster)

                                # Weather alerts (simulated)
                                if show_weather:
                                    for _ in range(5):
                                        lat = random.uniform(min_lat, max_lat)
                                        lon = random.uniform(min_lon, max_lon)
                                        weather = random.choice(["Heavy Rain", "Thunderstorm", "Fog", "Heatwave"])
                                        folium.Marker([lat, lon], icon=folium.Icon(color='lightgray'),
                                                    tooltip=f"Weather Alert: {weather}").add_to(cluster)

                                # Route info
                                dist_km = route['summary']['distance'] / 1000
                                duration_min = int(route['summary']['duration'] // 60)
                                hours = duration_min // 60
                                minutes = duration_min % 60
                                duration_str = f"{hours} hr {minutes} min" if hours else f"{minutes} min"

                                st.success("Route & Alerts Ready")
                                st.write(f"Distance: {dist_km:.2f} km")
                                st.write(f"Estimated Travel Time: {duration_str}")
                                folium_static(m)
                            else:
                                st.warning("No route found.")
                        else:
                            st.warning("Invalid start or destination.")


    elif selected == translate_text(T['emergency'], lang_code):
        st.title(translate_text(T['emergency_fac'], lang_code))
        Emergency(lang_code)

    elif selected == translate_text(T['safety_info'], lang_code):
        st.header(translate_text(T['safety_guidelines'], lang_code))
        safety(lang_code)

    elif selected == translate_text(T['charts'], lang_code):
        charts()

    elif selected == translate_text(T['incident'], lang_code):
        st.title(""+ translate_text(T['report_incident'], lang_code))
        CSV_FILE = "reports.csv"
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with st.form("incident_report_form"):
            category = st.selectbox(translate_text(T['category'], lang_code), ["Crime", "Disaster", "Traffic", "Weather"])
            report_title = st.text_input(translate_text(T['title_label'], lang_code))
            report_description = st.text_area(translate_text(T['desc_label'], lang_code))
            report_location = st.text_input(translate_text(T['location_label'], lang_code))
            uploaded_file = st.file_uploader(translate_text(T['upload_file'], lang_code),
                                             type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])
            submitted = st.form_submit_button(translate_text(T['submit_report'], lang_code))
            if submitted:
                if report_title and report_description and report_location:
                    file_path = ""
                    if uploaded_file is not None:
                        file_extension = uploaded_file.name.split(".")[-1]
                        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                        file_path = os.path.join(UPLOAD_DIR, unique_filename)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.read())
                    report_data = {
                        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                        "category": category,
                        "title": report_title,
                        "description": report_description,
                        "location": report_location,
                        "file": file_path,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "Pending"
                    }
                    if os.path.exists(CSV_FILE):
                        df = pd.read_csv(CSV_FILE)
                        df = pd.concat([df, pd.DataFrame([report_data])], ignore_index=True)
                    else:
                        df = pd.DataFrame([report_data])
                    df.to_csv(CSV_FILE, index=False)
                    st.success(translate_text(T['report_success'], lang_code))
                else:
                    st.error(translate_text(T['fill_fields'], lang_code))

    elif selected == translate_text(T['prediction'], lang_code):
        prediction(lang_code)

    elif selected == translate_text(T['news'], lang_code):
        st.header(translate_text(T['daily_news'], lang_code))
        news(lang_code)

    elif selected == translate_text(T['chatbot'], lang_code):
        st.header(translate_text(T['ai_assistant'], lang_code))
        chat(lang_code)

    elif selected == translate_text(T['quiz'], lang_code):
        st.header(translate_text(T['quiz_label'], lang_code))
        Quiz()

    elif selected == translate_text(T['feedback'], lang_code):
        st.header(translate_text(T['feedback_label'], lang_code))
        Feedback(lang_code)
