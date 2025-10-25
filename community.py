
def Feedback(lang):
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    import os
    import time
    from deep_translator import GoogleTranslator

    # Translation function
    def t(text):
        if lang != "English":
            return GoogleTranslator(source="auto", target=lang).translate(text)
        return text

    st.set_page_config(page_title=t("User Feedback Form"), layout="centered")

    st.title("" + t("User Feedback Form"))

    # CSV file path
    file_path = "feedback_responses.csv"

    # Define consistent column headers
    columns = [
        "Timestamp", "Name", "Email", "User Type", "Usage", "Features Used",
        "Overall Rating", "Design Rating", "Speed Rating", "Alert Accuracy",
        "Liked Most", "Issues Faced", "Suggestions",
        "Bug Reported", "Bug Description", "Bug Time"
    ]

    # --- Feedback Form ---
    with st.form("feedback_form", clear_on_submit=True):
        st.header(" " + t("User Info"))
        name = st.text_input(t("Name *"))
        email = st.text_input(t("Email"))

        user_type = st.selectbox(t("You are a:"), [t("Student"), t("Professional"), t("Other")])
        usage = st.radio(t("How often do you use this app?"), [t("Daily"), t("Weekly"), t("Occasionally")])

        st.header(" " + t("Ratings"))
        features = st.multiselect(t("Which features did you use?"), [t("Live Alerts"), t("Maps"), t("Weather"), t("Nearby Services")])
        overall = st.slider(t("Overall Satisfaction"), 1, 5, 3)
        design = st.slider(t("Design & UI"), 1, 5, 3)
        speed = st.slider(t("Speed"), 1, 5, 3)
        accuracy = st.slider(t("Alert Accuracy"), 1, 5, 3)

        st.header(" " + t("Feedback"))
        liked = st.text_area(t("What did you like most?"))
        issues = st.text_area(t("Any issues faced?"))
        suggestions = st.text_area(t("Suggestions for improvement"))

        st.header("" + t("Bug Report (Optional)"))
        bug_reported = st.checkbox(t("Did you face a bug?"))
        bug_desc = ""
        bug_time = ""
        if bug_reported:
            bug_desc = st.text_area(t("Describe the bug"))
            bug_time = st.time_input(t("What time did the bug occur?"))

        submitted = st.form_submit_button(t("Submit Feedback"))

    # --- Submission Logic ---
    if submitted:
        if name.strip() == "":
            st.error(" " + t("Please enter your name before submitting."))
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            feedback_data = {
                "Timestamp": timestamp,
                "Name": name,
                "Email": email,
                "User Type": user_type,
                "Usage": usage,
                "Features Used": ", ".join(features),
                "Overall Rating": overall,
                "Design Rating": design,
                "Speed Rating": speed,
                "Alert Accuracy": accuracy,
                "Liked Most": liked,
                "Issues Faced": issues,
                "Suggestions": suggestions,
                "Bug Reported": bug_reported,
                "Bug Description": bug_desc,
                "Bug Time": str(bug_time) if bug_reported else ""
            }

            # Save to CSV
            df = pd.DataFrame([feedback_data], columns=columns)
            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            st.success(" " + t("Thank you! Your feedback has been submitted."))
            st.toast(t("Refreshing for next response..."), icon="🔄")
            time.sleep(2)
            st.rerun()
