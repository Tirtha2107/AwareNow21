

    
        
       
def prediction(lang):
    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
    import os
    import json

    from streamlit_option_menu import option_menu
    from deep_translator import GoogleTranslator
    from ML_prediction_crime import mlcrime
    from forecast import forcast
    from Disaster_pred import Disaster_Prediction

    # Set wide layout
    st.set_page_config(layout="wide")

    def t(text):
        if lang != "en":
            try:
                return GoogleTranslator(source="en", target=lang).translate(text)
            except:
                return text
        return text

    st.markdown(f"### {t('This is the Main Dashboard.')}")

    selected_dashboard = option_menu(
        menu_title=None,
        options=[
            t("Crime"),
            t("Disaster"),
            t("Weather")
        ],
        icons=[
            "user-secret",           # Crime
            "exclamation-triangle",  # Disaster
            "cloud"                  # Weather
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

    if selected_dashboard == t("Crime"):
        st.subheader(t("Crime Prediction"))
        mlcrime(lang)  

    elif selected_dashboard == t("Disaster"):
        st.subheader(t("Disaster Prediction"))
        Disaster_Prediction(lang)

    elif selected_dashboard == t("Weather"):
        st.subheader(t("Weather Prediction"))
        forcast(lang)


