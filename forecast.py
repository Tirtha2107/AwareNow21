
def forcast(lang):
    import streamlit as st
    import requests
    import pandas as pd
    import random
    from datetime import datetime
    from fpdf import FPDF
    import plotly.express as px
    from deep_translator import GoogleTranslator

    API_KEY = "c24f70a890c583d233cbd498262f6294"

    # -------------------- TRANSLATION FUNCTION --------------------
    def t(text):
        try:
            return GoogleTranslator(source='auto', target=lang).translate(text)
        except:
            return text

    # -------------------- API FUNCTIONS --------------------
    def get_weather(city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        return res.json()

    def get_forecast(city):
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url)
        return res.json()

    # -------------------- HELPER FUNCTIONS --------------------
    def create_forecast_df(forecast_data):
        forecast_list = forecast_data["list"]
        records = []
        for f in forecast_list:
            dt = datetime.fromtimestamp(f["dt"])
            temp = f["main"]["temp"]
            rain = f.get("rain", {}).get("3h", 0)
            records.append({"Datetime": dt, t("Temperature (°C)"): temp, t("Rainfall (mm)"): rain})
        return pd.DataFrame(records)

    def generate_alerts(weather_data):
        alerts = []
        main = weather_data.get("main", {})
        temp = main.get("temp")
        humidity = main.get("humidity")
        rain_data = weather_data.get("rain", {})
        rain_1h = rain_data.get("1h", 0) if rain_data else 0

        if temp and temp > 40:
            alerts.append(t("Heatwave Warning: Temperature exceeds 40°C."))
        if rain_1h and rain_1h > 10:
            alerts.append(t(f"Heavy Rain Alert: {rain_1h} mm rainfall expected in 1 hour."))
        if humidity and humidity > 85:
            alerts.append(t("High Humidity Alert: May feel more uncomfortable."))
        if not alerts:
            alerts.append(t("No significant weather alerts."))
        return alerts

    # -------------------- FALLBACK PREDICTION --------------------
    def predict_weather(city):
        averages = {
            "temp": 28,
            "humidity": 70,
            "wind_speed": 10,
            "description": "partly cloudy"
        }
        return {
            "main": {
                "temp": round(averages["temp"] + random.uniform(-3, 3), 1),
                "humidity": round(averages["humidity"] + random.uniform(-10, 10)),
            },
            "wind": {"speed": round(averages["wind_speed"] + random.uniform(-2, 2), 1)},
            "weather": [{"description": averages["description"], "icon": "02d"}],
            "rain": {}
        }

    # -------------------- STREAMLIT APP --------------------
    st.set_page_config(page_title=t("India Weather Forecast"), layout="wide")
    st.title(t("India Weather Forecast with Rainfall Info"))

    city1 = st.text_input(t("Enter City Name"), "Mumbai")

    if st.button(t("Get Weather Forecast")):
        weather1 = get_weather(city1)

        if "main" not in weather1:
            st.warning(t(f"No live data found for '{city1}'. Using predicted weather data."))
            weather1 = predict_weather(city1)
            forecast1 = None
        else:
            forecast1 = get_forecast(city1)

        col1, col2 = st.columns(2)

        with col1:
            st.header(f"{city1}")
            st.metric(t("Temperature"), f"{weather1['main']['temp']} °C")
            st.image(f"http://openweathermap.org/img/wn/{weather1['weather'][0]['icon']}@2x.png")
            st.write(f"*{t('Description')}:*", weather1["weather"][0]["description"].capitalize())
            st.write(f"*{t('Humidity')}:*", f"{weather1['main']['humidity']} %")
            st.write(f"*{t('Wind Speed')}:*", f"{weather1['wind']['speed']} km/h")

            alerts1 = generate_alerts(weather1)
            if alerts1:
                st.warning(t("Alerts:") + "\n" + "\n".join(alerts1))

        if forecast1:
            with col2:
                st.subheader(t("5-Day Forecast"))
                df_forecast = create_forecast_df(forecast1)
                fig = px.line(df_forecast, x="Datetime", y=t("Temperature (°C)"), title=t("Temperature Forecast"))
                st.plotly_chart(fig)

                
