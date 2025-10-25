def heatmap():
    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
    import os
    import json

    from streamlit_option_menu import option_menu
    from deep_translator import GoogleTranslator
    from weather_heat import weather_heat
    from disaster_heat import disaster_heat
    from crime_heat import crime_heat

    # Set wide layout to avoid side black space
    st.set_page_config(layout="wide")


    # ----------------------------
    # Language Translator Function
    # ----------------------------
    def translate_text(text, lang_code):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except:
            return text  # fallback to original if error


    # ----------------------------
    # Dashboard Main Function
    # ----------------------------
    lang_code = st.session_state.get("lang_code", "en")

    st.markdown(f"### {translate_text('This is the Main Dashboard.', lang_code)}")

    selected_dashboard = option_menu(
        menu_title=None,
        options=[
            translate_text("Crime", lang_code),
            translate_text("Disaster", lang_code),
            translate_text("Weather", lang_code)
        ],
        icons = [
            "user-secret",           # Crime
            "exclamation-triangle", # Disaster
            "cloud"                 # Weather
        ],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "10px",
                "background-color": "#EF3131",
                "justify-content": "center"
            },
            "icon": {
                "color": "white",
                "font-size": "28px"
            },
            "nav-link": {
                "font-size": "20px",
                "text-align": "center",
                "margin": "10px",
                "padding": "20px 0px",
                "background-color": "#EF3131",
                "color": "white",
                "border-radius": "10px",
                "min-width": "150px",
                "flex": "1"
            },
            "nav-link-selected": {
                "background-color": "#ff9900"
            }
        }
    )

    # ----------------------------
    # MAP VIEW TAB
    # ----------------------------
    if selected_dashboard == translate_text("Crime", lang_code):
        st.subheader(translate_text("Crime Prediction", lang_code))
        crime_heat()
        
    
    elif selected_dashboard == translate_text("Disaster", lang_code):
        st.subheader(translate_text("Disaster Prediction", lang_code))
        disaster_heat()

    elif selected_dashboard == translate_text("Weather", lang_code):
        st.subheader(translate_text("Weather Prediction", lang_code))    
        weather_heat()

heatmap()
