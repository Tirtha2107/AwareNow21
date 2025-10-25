

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# -------------------- Load Datasets --------------------
@st.cache_data
def load_data():
    # Read CSVs
    disaster_df = pd.read_csv("disasterIND .csv")
    traffic_df = pd.read_csv("Indian_Traffic_Violations.csv")
    crime_df = pd.read_csv("crime_dataset_india (3).csv")
    
    # Standardize columns
    disaster_df = disaster_df.rename(columns={"Latitude": "lat", "Longitude": "lon", "City": "city"})
    traffic_df = traffic_df.rename(columns={"Latitude": "lat", "Longitude": "lon", "City": "city"})
    crime_df = crime_df.rename(columns={"Latitude": "lat", "Longitude": "lon", "City": "city"})
    
    # Add category
    disaster_df["category"] = "Disaster"
    traffic_df["category"] = "Traffic"
    crime_df["category"] = "Crime"
    
    # Merge
    combined_df = pd.concat([disaster_df, traffic_df, crime_df], ignore_index=True)
    
    # Drop missing coordinates
    combined_df = combined_df.dropna(subset=["lat", "lon"])
    
    # Ensure correct types
    combined_df["lat"] = combined_df["lat"].astype(float)
    combined_df["lon"] = combined_df["lon"].astype(float)
    combined_df["city"] = combined_df["city"].astype(str).str.strip().str.title()
    
    return combined_df

df = load_data()

# -------------------- City Selection --------------------
cities = sorted(df["city"].dropna().unique())
selected_city = st.selectbox("Select a City", options=["All Cities"] + list(cities))

if selected_city != "All Cities":
    city_df = df[df["city"] == selected_city]
else:
    city_df = df

# -------------------- Create Map --------------------
if not city_df.empty:
    map_center = [city_df["lat"].mean(), city_df["lon"].mean()]
    m = folium.Map(location=map_center, zoom_start=6, tiles="CartoDB dark_matter")
    
    # Add HeatMap
    heat_data = city_df[["lat", "lon"]].values.tolist()
    HeatMap(heat_data, radius=10, blur=15, min_opacity=0.4).add_to(m)
    
    # Add click-to-get-coordinates
    folium.LatLngPopup().add_to(m)
    
    # Display map and capture interaction
    map_data = st_folium(m, width=800, height=500)
    
    # If user clicks on the map
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        
        st.success(f"📍 Clicked location: Latitude {lat:.4f}, Longitude {lon:.4f}")
        
        # Ask user to enter city name
        new_city = st.text_input("Enter City Name for this location:")
        if new_city:
            st.write(f"✅ You entered: {new_city}")
            # Example: Append to dataframe
            # df = pd.concat([df, pd.DataFrame([[lat, lon, new_city.title(), "User Input"]], 
            #                                  columns=["lat", "lon", "city", "category"])])
else:
    st.warning("No data found for the selected city.")
