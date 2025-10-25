def chat(lang):
    import streamlit as st
    import pandas as pd
    import google.generativeai as genai
    import datetime
    from deep_translator import GoogleTranslator

    # ----------------- LANGUAGE HANDLING -----------------
     # Translation function
    def t(text):
        if lang != "English":
            return GoogleTranslator(source="auto", target=lang).translate(text)
        return text

    # ================== LOAD DATA ==================
    @st.cache_data
    def load_data():
        crime_df = pd.read_csv("crime_dataset_india (3).csv")
        disaster_df = pd.read_csv("disasterIND .csv")
        traffic_df = pd.read_csv("Indian_Traffic_Violations.csv")
        weather_df = pd.read_excel("weather.xlsx")
        return crime_df, disaster_df, traffic_df, weather_df

    crime_df, disaster_df, traffic_df, weather_df = load_data()

    # ================== GEMINI CONFIG ==================
    api_key = "AIzaSyBBWBIahoh1TrweQuDVfmhnpEtKs5AoJ1E"  # replace with your valid key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    # ================== STREAMLIT UI ==================
    st.title(t("AwareNow AI Assistant"))

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input(t("You:"), key="input")

    # ================== FUNCTION TO DETECT QUERY ==================
    def detect_and_answer(query):
        query_lower = query.lower()

        # ---------- Crime ----------
        if "crime" in query_lower or "theft" in query_lower or "murder" in query_lower:
            latest = crime_df.head(5)
            return t("Here are recent crime records:"), latest

        # ---------- Disaster ----------
        elif "disaster" in query_lower or "flood" in query_lower or "earthquake" in query_lower:
            latest = disaster_df.head(5)
            return t("Here are recent disaster records:"), latest

        # ---------- Traffic ----------
        elif "traffic" in query_lower or "violation" in query_lower:
            latest = traffic_df.head(5)
            return t("Here are recent traffic violation records:"), latest

        # ---------- Weather ----------
        elif "weather" in query_lower or "temperature" in query_lower or "rain" in query_lower:
            latest = weather_df.head(5)
            return t("Here is the latest weather data:"), latest

        # ---------- Default (AI) ----------
        else:
            response = model.generate_content(query)
            return t(response.text), None

    # ================== CHAT HANDLING ==================
    if st.button(t("Send")) and user_input:
        st.session_state.chat_history.append((t("You"), user_input))
        answer, table_data = detect_and_answer(user_input)
        st.session_state.chat_history.append((t("Gemini"), answer))
        if table_data is not None:
            st.session_state.chat_history.append(("TABLE", table_data))

    # ================== DISPLAY CHAT ==================
    for sender, msg in st.session_state.chat_history:
        if sender == "TABLE":
            st.dataframe(msg, use_container_width=True)
        else:
            st.markdown(f"**{sender}:** {msg}")
