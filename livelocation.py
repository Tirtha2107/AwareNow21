###
import streamlit as st
import time
import requests
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
import openrouteservice

# === Config ===
REFRESH_INTERVAL = 10  # seconds
GOOGLE_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE3NmIzNGUyZWE1ZDQ4ZWM4N2IxZGQ3N2FhNWI1NTUyIiwiaCI6Im11cm11cjY0In0="

st.set_page_config(page_title="Live Location Tracker", layout="centered")
st.title("📍 Live Location Tracker")
st.write(f"This page will refresh every {REFRESH_INTERVAL} seconds.")

# === Get live location ===
location = streamlit_geolocation()

# === Function to get nearby places ===
def get_nearby_places(api_key, lat, lon, place_type):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "location": f"{lat},{lon}",
        "radius": 5000,
        "type": place_type,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    results = response.json().get("results", [])
    
    places = []
    for place in results[:5]:  # Limit to 5 results for speed
        place_id = place.get("place_id")
        name = place.get("name", "N/A")
        address = place.get("vicinity", "N/A")

        # Get detailed info including phone number
        details_params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number",
            "key": api_key
        }
        detail_response = requests.get(details_url, params=details_params)
        detail_data = detail_response.json().get("result", {})

        phone = detail_data.get("formatted_phone_number", "Not available")

        places.append({
            "name": name,
            "address": address,
            "phone": phone
        })
    return places

# === Main logic ===
if location and location["latitude"] and location["longitude"]:
    lat = location["latitude"]
    lon = location["longitude"]

    st.success(f"Current Location: {lat:.6f}, {lon:.6f}")

    # Show on map
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker(
        [lat, lon],
        popup="📍 You are here",
        icon=folium.Icon(color="red", icon="glyphicon-map-marker")
    ).add_to(m)
    st_folium(m, width=700, height=500)

    # === Nearby Hospitals ===
    st.subheader("🏥 Nearby Hospitals")
    hospitals = get_nearby_places(GOOGLE_API_KEY, lat, lon, "hospital")
    if hospitals:
        for h in hospitals:
            st.markdown(f"**{h['name']}**")
            st.write(f"📍 {h['address']}")
            st.write(f"📞 {h['phone']}")
            st.markdown("---")
    else:
        st.write("No hospitals found nearby.")

    # === Nearby Police Stations ===
    st.subheader("👮 Nearby Police Stations")
    police = get_nearby_places(GOOGLE_API_KEY, lat, lon, "police")
    if police:
        for p in police:
            st.markdown(f"**{p['name']}**")
            st.write(f"📍 {p['address']}")
            st.write(f"📞 {p['phone']}")
            st.markdown("---")
    else:
        st.write("No police stations found nearby.")
else:
    st.info("Waiting for location... Please allow location access in your browser.")

# Auto-refresh
time.sleep(REFRESH_INTERVAL)
st.rerun()