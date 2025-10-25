


import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import openrouteservice
import requests
from geopy.distance import geodesic

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE3NmIzNGUyZWE1ZDQ4ZWM4N2IxZGQ3N2FhNWI1NTUyIiwiaCI6Im11cm11cjY0In0="   # replace with your OpenRouteService key
geolocator = Nominatim(user_agent="india_emergency_locator")

def geocode_place(place):
    try:
        loc = geolocator.geocode(place, timeout=10)
        return (loc.latitude, loc.longitude) if loc else None
    except GeocoderTimedOut:
        return None

def fetch_overpass(lat, lon, radius=5000):
    # query hospitals, police stations, shelters (amenity=hospital, amenity=police, emergency=shelter)
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
    folium.GeoJson(route, style={"color":"blue", "weight":5}).add_to(m)
    folium.Marker(start, tooltip="You are here", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(end, tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)
    return m

st.title("Emergency Services Locator (All India)")
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
            st.warning("No emergency facilities found within 5 km radius.")

        result = st_folium(fmap, width=800, height=500)

        # Show routing controls
        st.markdown("---")
        st.subheader(" Show Route to Facility")
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
