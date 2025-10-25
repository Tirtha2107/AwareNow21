def Live_Alerts():
    import streamlit as st
    from streamlit_geolocation import streamlit_geolocation
    import folium
    from streamlit_folium import st_folium
    import pandas as pd
    import random

    st.set_page_config(page_title="Live Alerts & Location", layout="wide")
    st.title("📍 Live Emergency & Crime Alerts")

    # --- Dummy alerts generator (replace with real API) ---
    def get_real_alerts(center_lat, center_lon, n=15):
        alert_types = ['Fire', 'Crime', 'Flood', 'Traffic', 'Medical Emergency']
        alerts = []
        for _ in range(n):
            alert_type = random.choice(alert_types)
            lat = center_lat + random.uniform(-0.02, 0.02)
            lon = center_lon + random.uniform(-0.02, 0.02)
            alerts.append({
                "type": alert_type,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "details": f"[{alert_type}] Reported at {lat:.4f}, {lon:.4f}."
            })
        return alerts

    # --- Session state defaults ---
    if "user_location" not in st.session_state:
        st.session_state.user_location = None   # [lat, lon] or None
        st.session_state.alerts = []
        st.session_state.loc_clicked = False

    # --- Locate Me button (user must click to request browser geolocation) ---
    st.markdown("Click the button below to let the browser share your location.")
    if st.button("📍 Locate Me"):
        st.session_state.loc_clicked = True

    # If user clicked, request browser location (streamlit_geolocation shows the browser prompt)
    if st.session_state.loc_clicked:
        location = streamlit_geolocation()
        if location and location.get("latitude") is not None and location.get("longitude") is not None:
            lat = location["latitude"]
            lon = location["longitude"]
            # Save and fetch alerts
            changed = (st.session_state.user_location is None) or (abs(lat - st.session_state.user_location[0]) > 1e-3 or abs(lon - st.session_state.user_location[1]) > 1e-3)
            st.session_state.user_location = [lat, lon]
            if changed or not st.session_state.alerts:
                st.session_state.alerts = get_real_alerts(lat, lon)
            st.success(f"Location received: {lat:.6f}, {lon:.6f}")
        else:
            st.warning("Waiting for browser to provide location. Make sure you click 'Allow' in the prompt.")

    # Show map & controls only if we have a location
    if st.session_state.user_location:
        current_user_lat, current_user_lon = st.session_state.user_location

        # Simple refresh button to re-fetch alerts (avoids full page rerun)
        if st.button("🔄 Refresh Alerts"):
            st.session_state.alerts = get_real_alerts(current_user_lat, current_user_lon)

        # Filters (main page)
        all_alert_types = ['Fire', 'Crime', 'Flood', 'Traffic', 'Medical Emergency']
        selected_alert_types = st.multiselect(
            "Select alert types to display:",
            options=all_alert_types,
            default=all_alert_types
        )

        filtered_alerts = [a for a in st.session_state.alerts if a["type"] in selected_alert_types]

        # Build map
        m = folium.Map(location=[current_user_lat, current_user_lon], zoom_start=14)
        folium.Marker(
            [current_user_lat, current_user_lon],
            tooltip="Your Current Location",
            icon=folium.Icon(color="green", icon="user", prefix='fa')
        ).add_to(m)

        color_map = {"Fire": "red", "Crime": "blue", "Flood": "orange", "Traffic": "purple", "Medical Emergency": "darkred"}
        icon_map = {"Fire": "fire", "Crime": "exclamation-triangle", "Flood": "tint", "Traffic": "car", "Medical Emergency": "heartbeat"}

        for alert in filtered_alerts:
            folium.Marker(
                [alert["latitude"], alert["longitude"]],
                tooltip=f"{alert['type']} Alert",
                popup=folium.Popup(alert["details"], max_width=300),
                icon=folium.Icon(
                    color=color_map.get(alert["type"], "gray"),
                    icon=icon_map.get(alert["type"], "info"),
                    prefix='fa'
                )
            ).add_to(m)

        st.subheader("🗺 Map of Live Alerts")
        st_folium(m, width=1000, height=500)

        st.subheader("🧾 Recent Alerts Nearby")
        with st.expander(f"View details for {len(filtered_alerts)} alerts"):
            if filtered_alerts:
                df = pd.DataFrame(filtered_alerts)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No alerts of the selected types found in this area.")
    else:
        st.info("Map will appear after you click '📍 Locate Me' and allow location access.")