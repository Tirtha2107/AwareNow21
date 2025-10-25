def inter_maps(lang_code):
    import streamlit as st
    import pandas as pd
    import folium
    import json
    import random
    import requests
    import openrouteservice
    from folium.plugins import MarkerCluster
    from streamlit_folium import st_folium, folium_static
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    from openrouteservice import convert
    from datetime import datetime
    from deep_translator import GoogleTranslator
    from livealert import Live_Alerts


    # Translation helper
    def translate_text(text, lang_code):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except Exception:
            return text

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

    crime_df = pd.read_csv("crime_dataset_india (3).csv")
    disaster_df = pd.read_csv("disasterIND .csv")
    traffic_df = pd.read_csv("Indian_Traffic_Violations.csv")

    for key in ["heatmap", "markers", "alert", "travel"]:
        if key not in st.session_state:
            st.session_state[key] = False

    

    with st.expander(translate_text("Map Controls", lang_code), expanded=True):
        if st.button(translate_text("Heatmap", lang_code)):
            st.session_state.heatmap = not st.session_state.heatmap
        if st.button(translate_text("Markers", lang_code)):
            st.session_state.markers = not st.session_state.markers
        if st.button(translate_text("Live Alerts", lang_code)):
            st.session_state.alert = not st.session_state.alert
        if st.button(translate_text("Live Travel", lang_code)):
            st.session_state.travel = not st.session_state.travel

    if st.session_state.heatmap:
        st.subheader(translate_text("Heatmap Feature (Coming Soon)", lang_code))

    if st.session_state.markers:
        st.subheader(translate_text("Markers Feature (Coming Soon)", lang_code))

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
                popup = folium.Popup(
                    f"{name} ({typ.title()})<br>Lat: {lat:.5f}, Lon: {lon:.5f}",
                    max_width=250
                )
                folium.Marker([lat, lon], popup=popup, icon=folium.Icon(color=color)).add_to(fmap)

        def route_map(start, end):
            client = openrouteservice.Client(key=ORS_API_KEY)
            coords = [start[::-1], end[::-1]]
            route = client.directions(coordinates=coords, profile='driving-car', format='geojson')
            m = folium.Map(location=start, zoom_start=14)
            folium.GeoJson(route, style={"color": "blue", "weight": 5}).add_to(m)
            folium.Marker(start, tooltip=translate_text("You are here", lang_code), icon=folium.Icon(color="blue")).add_to(m)
            folium.Marker(end, tooltip=translate_text("Destination", lang_code), icon=folium.Icon(color="red")).add_to(m)
            return m

        st.title(translate_text("Emergency Markers (All India)", lang_code))
        place = st.text_input(translate_text("Enter Area Name or PIN Code (India)", lang_code),
                              placeholder=translate_text("e.g., Mumbai, 110001", lang_code))

        if place:
            loc = geocode_place(place)
            if loc:
                st.success(f"{translate_text('Location found', lang_code)}: {loc}")
                lat, lon = loc
                fmap = folium.Map(location=loc, zoom_start=14)
                folium.Marker(loc, tooltip=translate_text("You are here", lang_code),
                              icon=folium.Icon(color="blue")).add_to(fmap)

                facilities = fetch_overpass(lat, lon)
                if facilities:
                    plot_facilities(fmap, facilities)
                else:
                    st.warning(translate_text("No emergency facilities found within 5 km radius.", lang_code))

                st_folium(fmap, width=800, height=500)

                st.markdown("---")
                st.subheader(translate_text("Show Route to Facility", lang_code))
                dest = st.text_input(translate_text("Enter facility latitude,longitude (from map popup):", lang_code))
                if dest:
                    try:
                        dlat, dlon = map(float, dest.split(","))
                        m2 = route_map(loc, (dlat, dlon))
                        st_folium(m2, width=800, height=500)
                    except:
                        st.error(translate_text("Invalid format. Use latitude,longitude", lang_code))

            else:
                st.error(translate_text("Could not geocode the location. Try again with a valid place or PIN code.", lang_code))

    if st.session_state.alert:
        st.subheader(translate_text("Live Alerts Feature (Coming Soon)", lang_code))
        Live_Alerts()

    if st.session_state.travel:
        st.title(translate_text("AwareNow - Smart Route Planner with Live Alerts", lang_code))

        col1, col2 = st.columns(2)
        start_address = col1.text_input(translate_text("Start Location", lang_code), "Pune")
        destination_address = col2.text_input(translate_text("Destination", lang_code), "Gateway of India, Mumbai")

        st.header(translate_text("Alert Filters", lang_code))
        show_crime = st.checkbox(translate_text("Crime Alerts", lang_code), True)
        show_disaster = st.checkbox(translate_text("Disaster Alerts", lang_code), True)
        show_traffic = st.checkbox(translate_text("Traffic Violations", lang_code), True)
        show_flood = st.checkbox(translate_text("Flood Warnings (Simulated)", lang_code), True)
        show_weather = st.checkbox(translate_text("Weather Warnings (Simulated)", lang_code), True)

        if st.button(translate_text("Plan Route", lang_code)):
            if start_address and destination_address:
                with st.spinner(translate_text("Fetching route and alerts...", lang_code)):
                    start_coords = get_coordinates(start_address)
                    end_coords = get_coordinates(destination_address)

                    if start_coords and end_coords:
                        route_data = get_route(start_coords, end_coords)
                        if route_data and 'routes' in route_data:
                            route = route_data['routes'][0]
                            geometry = convert.decode_polyline(route['geometry'])
                            route_line = [[coord[1], coord[0]] for coord in geometry['coordinates']]

                            m = folium.Map(location=start_coords, zoom_start=6, tiles="CartoDB positron")
                            folium.Marker(start_coords, icon=folium.Icon(color='green'),
                                          tooltip=f"{translate_text('Start', lang_code)}: {start_address}").add_to(m)
                            folium.Marker(end_coords, icon=folium.Icon(color='blue'),
                                          tooltip=f"{translate_text('End', lang_code)}: {destination_address}").add_to(m)
                            folium.PolyLine(route_line, color="cyan", weight=5).add_to(m)

                            # Filtering and plotting alerts
                            min_lat = min(start_coords[0], end_coords[0])
                            max_lat = max(start_coords[0], end_coords[0])
                            min_lon = min(start_coords[1], end_coords[1])
                            max_lon = max(start_coords[1], end_coords[1])

                            cluster = MarkerCluster().add_to(m)

                            if show_crime:
                                for _, row in crime_df.head(200).iterrows():
                                    city = row.get("City", "")
                                    desc = row.get("Crime Description", "")
                                    coords = get_coordinates(city)
                                    if coords:
                                        lat, lon = coords
                                        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                                            folium.Marker([lat, lon], icon=folium.Icon(color='red'),
                                                          tooltip=f"{desc} {translate_text('in', lang_code)} {city}").add_to(cluster)

                            if show_disaster:
                                disaster_df.dropna(subset=["Latitude", "Longitude"], inplace=True)
                                for _, row in disaster_df.iterrows():
                                    lat, lon = row["Latitude"], row["Longitude"]
                                    dtype = row.get("Disaster Type", "")
                                    loc = row.get("Location", "")
                                    if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                                        folium.Marker([lat, lon], icon=folium.Icon(color='orange'),
                                                      tooltip=f"{dtype} {translate_text('at', lang_code)} {loc}").add_to(cluster)

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
                                                          tooltip=f"{vtype} {translate_text('at', lang_code)} {location}").add_to(cluster)

                            if show_flood:
                                for _ in range(10):
                                    lat = random.uniform(min_lat, max_lat)
                                    lon = random.uniform(min_lon, max_lon)
                                    folium.Marker([lat, lon], icon=folium.Icon(color='blue'),
                                                  tooltip=translate_text("Flood Alert (Simulated)", lang_code)).add_to(cluster)

                            if show_weather:
                                for _ in range(5):
                                    lat = random.uniform(min_lat, max_lat)
                                    lon = random.uniform(min_lon, max_lon)
                                    weather = random.choice(["Heavy Rain", "Thunderstorm", "Fog", "Heatwave"])
                                    folium.Marker([lat, lon], icon=folium.Icon(color='lightgray'),
                                                  tooltip=f"{translate_text('Weather Alert', lang_code)}: {translate_text(weather, lang_code)}").add_to(cluster)

                            dist_km = route['summary']['distance'] / 1000
                            duration_min = int(route['summary']['duration'] // 60)
                            hours = duration_min // 60
                            minutes = duration_min % 60
                            duration_str = f"{hours} hr {minutes} min" if hours else f"{minutes} min"

                            st.success(translate_text("Route & Alerts Ready", lang_code))
                            st.write(f"{translate_text('Distance', lang_code)}: {dist_km:.2f} km")
                            st.write(f"{translate_text('Estimated Travel Time', lang_code)}: {duration_str}")
                            folium_static(m)
                        else:
                            st.warning(translate_text("No route found.", lang_code))
                    else:
                        st.warning(translate_text("Invalid start or destination.", lang_code))
                     
