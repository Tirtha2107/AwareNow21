


def Emergency(lang_code):
    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    from geopy.distance import geodesic
    from geopy.geocoders import Nominatim
    import requests
    import folium
    from streamlit_folium import folium_static
    import pandas as pd
    import numpy as np
    from deep_translator import GoogleTranslator

    # Translation helper
    def translate_text(text):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except Exception:
            return text

    # --- Constants ---
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    HOSPITAL_SEARCH_RADIUS_KM = 2
    POLICE_SEARCH_RADIUS_KM = 5

    HOSPITAL_RADIUS_METERS = HOSPITAL_SEARCH_RADIUS_KM * 1000
    POLICE_RADIUS_METERS = POLICE_SEARCH_RADIUS_KM * 1000

    # --- Functions ---
    def get_nearby_places(latitude, longitude, tags, radius_meters):
        query = f"""
        [out:json][timeout:25];
        (
        node{tags}(around:{radius_meters},{latitude},{longitude});
        way{tags}(around:{radius_meters},{latitude},{longitude});
        relation{tags}(around:{radius_meters},{latitude},{longitude});
        );
        out center;
        """
        try:
            response = requests.post(OVERPASS_API_URL, data=query)
            response.raise_for_status()
            data = response.json()
            places = []
            for element in data['elements']:
                lat = element.get('lat', element.get('center', {}).get('lat'))
                lon = element.get('lon', element.get('center', {}).get('lon'))
                if lat is not None and lon is not None:
                    name = element.get('tags', {}).get('name', translate_text("Unknown"))
                    address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', translate_text("N/A")))
                    places.append({'name': name, 'lat': lat, 'lon': lon, 'address': address})
            return places
        except requests.exceptions.RequestException as e:
            st.error(f"{translate_text('Error fetching data from OpenStreetMap')}: {e}")
            return []

    def display_map(user_location, hospitals, police_stations):
        if user_location and user_location['latitude'] and user_location['longitude']:
            m = folium.Map(location=[user_location['latitude'], user_location['longitude']], zoom_start=14)

            # User location marker
            folium.Marker(
                location=[user_location['latitude'], user_location['longitude']],
                popup=translate_text("Your Location"),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

            # Hospitals
            for hospital in hospitals:
                folium.Marker(
                    location=[hospital['lat'], hospital['lon']],
                    popup=f"{translate_text('Hospital')}: {hospital['name']}<br>{translate_text('Address')}: {hospital['address']}",
                    icon=folium.Icon(color="red", icon="medkit")
                ).add_to(m)

            # Police Stations
            for police_station in police_stations:
                folium.Marker(
                    location=[police_station['lat'], police_station['lon']],
                    popup=f"{translate_text('Police Station')}: {police_station['name']}<br>{translate_text('Address')}: {police_station['address']}",
                    icon=folium.Icon(color="darkblue", icon="shield")
                ).add_to(m)

            folium_static(m)
        else:
            st.warning(translate_text("Could not get your location to display the map."))

    # --- Streamlit UI ---
    st.set_page_config(layout="wide")
    st.title(translate_text("Nearby Emergency Services (India)"))

    st.markdown(translate_text("""
        This app detects your current location and shows nearby hospitals and police stations
        within a specified radius in India.
    """))

    location_option = st.radio(
        translate_text("Choose your location input method:"),
        (translate_text("Use Live Location"), translate_text("Enter City Manually"))
    )

    user_lat = None
    user_lon = None
    user_location_display_text = ""

    if location_option == translate_text("Use Live Location"):
        st.info(translate_text("Please allow location access when prompted by your browser."))
        location = streamlit_geolocation()

        if location and location['latitude'] and location['longitude']:
            user_lat = location['latitude']
            user_lon = location['longitude']
            user_location_display_text = translate_text(f"Your current location: Latitude {user_lat:.4f}, Longitude {user_lon:.4f}")
        else:
            st.warning(translate_text("Waiting for location access... Please click 'Allow' in your browser if prompted."))
            st.info(translate_text("If location access is denied or not available, the map and nearby places won't be displayed."))

    elif location_option == translate_text("Enter City Manually"):
        city_name = st.text_input(translate_text("Enter city name (e.g., Mumbai, Delhi):"), "")
        if city_name:
            geolocator = Nominatim(user_agent="emergency_services_app")
            try:
                location_by_city = geolocator.geocode(city_name, country_codes='in')
                if location_by_city:
                    user_lat = location_by_city.latitude
                    user_lon = location_by_city.longitude
                    user_location_display_text = translate_text(f"Location for {city_name}: Latitude {user_lat:.4f}, Longitude {user_lon:.4f}")
                else:
                    st.error(translate_text(f"Could not find coordinates for '{city_name}'. Please try a different city name."))
            except Exception as e:
                st.error(translate_text(f"Error during geocoding: {e}. Please try again."))

    if user_lat is not None and user_lon is not None:
        st.write(user_location_display_text)

        # Hospitals
        st.subheader(translate_text(f"Hospitals within {HOSPITAL_SEARCH_RADIUS_KM} km:"))
        hospital_tags = '["amenity"="hospital"]'
        hospitals = get_nearby_places(user_lat, user_lon, hospital_tags, HOSPITAL_RADIUS_METERS)

        if hospitals:
            hospital_data_raw = []
            for hosp in hospitals:
                distance = geodesic((user_lat, user_lon), (hosp['lat'], hosp['lon'])).km
                hospital_data_raw.append({
                    'Name': hosp['name'],
                    'Address': hosp['address'],
                    'Distance_Raw': distance
                })
            hospital_data_raw.sort(key=lambda x: x['Distance_Raw'])

            df_hospitals = pd.DataFrame([
                {'Name': h['Name'], 'Address': h['Address'], translate_text('Distance (km)'): f"{h['Distance_Raw']:.2f}"}
                for h in hospital_data_raw
            ])
            st.dataframe(df_hospitals, use_container_width=True)
        else:
            st.info(translate_text(f"No hospitals found within {HOSPITAL_SEARCH_RADIUS_KM} km of your location."))

        # Police
        st.subheader(translate_text(f"Police Stations within {POLICE_SEARCH_RADIUS_KM} km:"))
        police_tags = '["amenity"="police"]'
        police_stations = get_nearby_places(user_lat, user_lon, police_tags, POLICE_RADIUS_METERS)

        if police_stations:
            police_data_raw = []
            for police in police_stations:
                distance = geodesic((user_lat, user_lon), (police['lat'], police['lon'])).km
                police_data_raw.append({
                    'Name': police['name'],
                    'Address': police['address'],
                    'Distance_Raw': distance
                })
            police_data_raw.sort(key=lambda x: x['Distance_Raw'])

            df_police = pd.DataFrame([
                {'Name': p['Name'], 'Address': p['Address'], translate_text('Distance (km)'): f"{p['Distance_Raw']:.2f}"}
                for p in police_data_raw
            ])
            st.dataframe(df_police, use_container_width=True)
        else:
            st.info(translate_text(f"No police stations found within {POLICE_SEARCH_RADIUS_KM} km of your location."))

        # Map
        st.subheader(translate_text("Map View:"))
        display_map({'latitude': user_lat, 'longitude': user_lon}, hospitals, police_stations)
    else:
        if location_option == translate_text("Enter City Manually") and not city_name:
            st.info(translate_text("Please enter a city name to find emergency services."))
