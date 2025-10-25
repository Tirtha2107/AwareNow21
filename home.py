

def show_Home(lang_code):
    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    from geopy.geocoders import Nominatim
    import os
    import json
    import pandas as pd
    from streamlit_option_menu import option_menu
    from deep_translator import GoogleTranslator
    from admin import admiin

    # Set wide layout
    st.set_page_config(layout="wide")

    # ----------------------------
    # Helper Functions
    # ----------------------------
    def translate_text(text):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except:
            return text

    feedback_file = "feedback_data.json"

    def load_feedback():
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as f:
                return json.load(f)
        return []

    def save_feedback(data):
        with open(feedback_file, "w") as f:
            json.dump(data, f, indent=2)

    # ----------------------------
    # Dashboard Main
    # ----------------------------
    st.markdown(f"### {translate_text('This is the Main Dashboard.')}")

    selected_dashboard = option_menu(
        menu_title=None,
        options=[
            translate_text("Map"),
            translate_text("Incidents"),
            translate_text("Feedback")
        ],
        icons=["map", "exclamation-triangle", "pen-to-square"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "10px", "background-color": "#EF3131", "justify-content": "center"},
            "icon": {"color": "white", "font-size": "28px"},
            "nav-link": {
                "font-size": "20px", "text-align": "center", "margin": "10px",
                "padding": "20px 0px", "background-color": "#EF3131",
                "color": "white", "border-radius": "10px", "min-width": "150px", "flex": "1"
            },
            "nav-link-selected": {"background-color": "#ff9900"}
        }
    )

    # ----------------------------
    # MAP VIEW TAB
    # ----------------------------
    if selected_dashboard == translate_text("Map"):
        st.subheader(translate_text("Map View"))
        location_method = st.radio(
            translate_text("Select how to provide your location:"),
            [translate_text("Enter Pincode/Place"), translate_text("Pick on Map")]
        )

        latitude, longitude = None, None

        if location_method == translate_text("Enter Pincode/Place"):
            location_input = st.text_input(
                translate_text("Enter a Pincode or Place Name (e.g., Mumbai 400001):"))
            if location_input:
                geolocator = Nominatim(user_agent="safety_map")
                location = geolocator.geocode(location_input)
                if location:
                    latitude, longitude = location.latitude, location.longitude
                else:
                    st.error(translate_text("Location not found. Please enter a valid place or pincode."))
        else:
            st.write(translate_text("Pick your location on the map below:"))
            pick_map = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
            pick_map.add_child(folium.LatLngPopup())
            st_folium(pick_map, width="100%", height=500)
            coords = st.text_input(translate_text("Enter picked coordinates (lat, lon):"))
            if coords:
                try:
                    latitude, longitude = map(float, coords.split(","))
                except:
                    st.error(translate_text("Invalid coordinate format. Use: lat, lon"))

        if latitude and longitude:
            st.success(translate_text(f"Showing map for location: ({latitude:.4f}, {longitude:.4f})"))
            map_view = folium.Map(location=[latitude, longitude], zoom_start=13)
            folium.Marker(
                [latitude, longitude],
                tooltip=translate_text("Your Location"),
                icon=folium.Icon(color="blue", icon="user")
            ).add_to(map_view)

            red_zones = [
                (latitude + 0.01, longitude + 0.01),
                (latitude - 0.01, longitude - 0.01),
                (latitude + 0.015, longitude - 0.015)
            ]
            for lat, lon in red_zones:
                folium.Circle(
                    location=[lat, lon], radius=300, color='red',
                    fill=True, fill_color='red', fill_opacity=0.4,
                    tooltip=translate_text("High Traffic / Incident Zone")
                ).add_to(map_view)

            st_folium(map_view, width="100%", height=550)

    # ----------------------------
    # INCIDENTS TAB
    # ----------------------------
    elif selected_dashboard == translate_text("Incidents"):
        # admiin()
        st.subheader(translate_text("Incident Reports"))
        st.write(translate_text("Below are recent incidents verified by the admin, along with public feedback."))
        CSV_FILE = "reports.csv"

        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            reviewed_df = df[df["status"] == "Reviewed"]

            if not reviewed_df.empty:
                st.markdown(f"### {translate_text('Verified Incidents')}")
                for _, row in reviewed_df.iterrows():
                    with st.expander(f"{translate_text(row['title'])} ({translate_text(row['location'])})"):
                        st.write(f"**{translate_text('Description')}:** {translate_text(row['description'])}")
                        st.write(f"**{translate_text('Date')}:** {row['date']}")
                        if "file" in row and isinstance(row["file"], str) and os.path.exists(row["file"]):
                            file_ext = row["file"].split('.')[-1].lower()
                            st.markdown(f"**📎 {translate_text('Uploaded File')}:**")
                            if file_ext in ["jpg", "jpeg", "png"]:
                                st.image(row["file"], use_column_width=True)
                            elif file_ext in ["mp4", "mov", "avi"]:
                                st.video(row["file"])
                            else:
                                st.write(f" {os.path.basename(row['file'])}")
            else:
                st.info(translate_text("No incidents have been verified yet."))
        else:
            st.warning(translate_text("Report file not found."))

        st.markdown(f"### {translate_text('Public Feedback')}")
        feedback_list = load_feedback()
        if feedback_list:
            for item in feedback_list:
                with st.expander(
                    f"{translate_text(item['name'])}  "
                    f"{translate_text('Upvotes')}: {item.get('upvotes', 0)} | "
                    f"{translate_text('Downvotes')}: {item.get('downvotes', 0)}"
                ):
                    st.write(translate_text(item['comment']))
        else:
            st.info(translate_text("No feedback submitted yet."))

    # ----------------------------
    # FEEDBACK TAB
    # ----------------------------
    elif selected_dashboard == translate_text("Feedback"):
        st.subheader(translate_text("Community Feedback"))
        feedback_list = load_feedback()

        if "voted_feedback" not in st.session_state:
            st.session_state.voted_feedback = set()

        if feedback_list:
            for i, item in enumerate(feedback_list):
                feedback_key = f"{item['name']}_{i}"
                expander_title = (
                    f"{translate_text(item['name'])}  "
                    f"{translate_text('Upvotes')}: {item.get('upvotes', 0)} | "
                    f"{translate_text('Downvotes')}: {item.get('downvotes', 0)}"
                )
                with st.expander(expander_title):
                    st.write(translate_text(item['comment']))
                    col1, col2 = st.columns(2)

                    with col1:
                        if feedback_key not in st.session_state.voted_feedback:
                            if st.button(f"{item.get('upvotes', 0)}", key=f"up_{i}"):
                                feedback_list[i]['upvotes'] = feedback_list[i].get('upvotes', 0) + 1
                                save_feedback(feedback_list)
                                st.session_state.voted_feedback.add(feedback_key)
                                st.rerun()
                        else:
                            st.button(f"{item.get('upvotes', 0)}", key=f"up_disabled_{i}", disabled=True)

                    with col2:
                        if feedback_key not in st.session_state.voted_feedback:
                            if st.button(f"{item.get('downvotes', 0)}", key=f"down_{i}"):
                                feedback_list[i]['downvotes'] = feedback_list[i].get('downvotes', 0) + 1
                                save_feedback(feedback_list)
                                st.session_state.voted_feedback.add(feedback_key)
                                st.rerun()
                        else:
                            st.button(f"{item.get('downvotes', 0)}", key=f"down_disabled_{i}", disabled=True)

        else:
            st.info(translate_text("No feedback submitted yet."))

        st.subheader(translate_text("Submit Feedback"))
        with st.form("feedback_form"):
            name = st.text_input(translate_text("Your Name"))
            comment = st.text_area(translate_text("Your Feedback or Suggestion"))
            if st.form_submit_button(translate_text("Submit")):
                if name and comment:
                    new_feedback = {"name": name, "comment": comment, "upvotes": 0, "downvotes": 0}
                    feedback_list.append(new_feedback)
                    save_feedback(feedback_list)
                    st.success(translate_text("Thank you for your feedback!"))
                else:
                    st.warning(translate_text("Please fill in both fields."))
