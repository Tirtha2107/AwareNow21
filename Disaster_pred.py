def Disaster_Prediction(lang):
    import streamlit as st
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from geopy.geocoders import Nominatim
    import folium
    from streamlit_folium import st_folium

    st.title("Disaster Type Prediction ")

    # ------------------ SYNTHETIC TRAINING DATA ------------------
    data = [
        [6, "Mumbai", "Flood"], [7, "Mumbai", "Flood"], [8, "Kolkata", "Flood"],
        [3, "Delhi", "Heatwave"], [4, "Jaipur", "Heatwave"], [5, "Nagpur", "Heatwave"],
        [10, "Chennai", "Cyclone"], [11, "Visakhapatnam", "Cyclone"], [12, "Puri", "Cyclone"],
        [1, "Delhi", "Cold Wave"], [2, "Bikaner", "Drought"], [5, "Jodhpur", "Drought"],
        [7, "Guwahati", "Flood"], [9, "Kochi", "Flood"], [8, "Manali", "Landslide"],
        [6, "Shimla", "Landslide"], [11, "Bhubaneswar", "Cyclone"], [3, "Ahmedabad", "Heatwave"]
    ]
    df = pd.DataFrame(data, columns=["Month", "City", "Disaster"])

    # ------------------ ENCODING ------------------
    le_city = LabelEncoder()
    le_disaster = LabelEncoder()

    df["City_enc"] = le_city.fit_transform(df["City"])
    df["Disaster_enc"] = le_disaster.fit_transform(df["Disaster"])

    # ------------------ MODEL TRAINING ------------------
    X = df[["Month", "City_enc"]]
    y = df["Disaster_enc"]

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)

    # ------------------ MARKER COLOR FUNCTION ------------------
    def get_marker_color(disaster_type):
        colors = {
            "Flood": "blue",
            "Heatwave": "red",
            "Cyclone": "purple",
            "Storm": "orange",
            "Cold Wave": "lightblue",
            "Drought": "beige",
            "Landslide": "green"
        }
        return colors.get(disaster_type, "gray")

    # ------------------ SESSION STATE ------------------
    if "predicted_type" not in st.session_state:
        st.session_state.predicted_type = None
    if "predicted_prob" not in st.session_state:
        st.session_state.predicted_prob = None
    if "map_coords" not in st.session_state:
        st.session_state.map_coords = None
    if "last_city" not in st.session_state:
        st.session_state.last_city = None

    # ------------------ USER INPUT ------------------
    city_input = st.text_input("Enter City Name", placeholder="e.g. Mumbai, Delhi")
    selected_date = st.date_input("Enter Date of Occurrence", value=None, format="YYYY/MM/DD")

    # ------------------ PREDICT BUTTON ------------------
    if st.button("Predict Disaster Type"):
        if city_input.strip() and selected_date:
            month = selected_date.month

            # If the city was never in training data, add it temporarily
            if city_input not in le_city.classes_:
                new_classes = list(le_city.classes_) + [city_input]
                le_city.classes_ = np.array(new_classes)

            city_enc = le_city.transform([city_input])[0]
            pred_enc = model.predict([[month, city_enc]])[0]
            pred_proba = max(model.predict_proba([[month, city_enc]])[0]) * 100

            disaster_pred = le_disaster.inverse_transform([pred_enc])[0]

            st.session_state.predicted_type = disaster_pred
            st.session_state.predicted_prob = round(pred_proba, 2)
            st.session_state.last_city = city_input

            # Get coordinates for map
            geolocator = Nominatim(user_agent="disaster-map")
            location = geolocator.geocode(f"{city_input}, India")
            if location:
                st.session_state.map_coords = (location.latitude, location.longitude)
            else:
                st.session_state.map_coords = None
        else:
            st.warning("Please enter a city name and select a date.")

    # ------------------ DISPLAY RESULT ------------------
    if st.session_state.predicted_type and st.session_state.last_city:
        st.success(
            f" Predicted Disaster Type in **{st.session_state.last_city}** "
            f"on **{selected_date.year}/{selected_date.month:02}/{selected_date.day:02}**: "
            f"**{st.session_state.predicted_type}** "
            f"(Likelihood: {st.session_state.predicted_prob}%)"
        )

    # ------------------ MAP ------------------
    if st.session_state.map_coords:
        lat, lon = st.session_state.map_coords
        m = folium.Map(location=[lat, lon], zoom_start=12)

        folium.Marker(
            [lat, lon],
            tooltip=f"{st.session_state.last_city} - {st.session_state.predicted_type}",
            icon=folium.Icon(color=get_marker_color(st.session_state.predicted_type))
        ).add_to(m)

        st_folium(m, width=700, height=500)

    elif st.session_state.last_city and not st.session_state.map_coords:
        st.warning("Could not locate city on map.")