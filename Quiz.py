def Quiz():
    import streamlit as st
    import pandas as pd
    import random
    from datetime import datetime
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    import os
    import time
    import uuid
    import threading

    # ------------------------------
    # --- Quiz Data ---
    # -----------------------------

    quiz_data = {
        "Disaster": {
            "Easy": [
                {"question": "What is an earthquake?", "options": ["Storm", "Ground shaking", "Flood", "Hurricane"], "answer": "Ground shaking"},
                {"question": "What causes floods?", "options": ["Heavy rain", "Sunlight", "Earthquake", "Snowfall"], "answer": "Heavy rain"},
                {"question": "Which natural disaster is caused by tectonic plate movement?", "options": ["Flood", "Cyclone", "Earthquake", "Landslide"], "answer": "Earthquake"},
                {"question": "What is the safe action during an earthquake?", "options": ["Run", "Hide under furniture", "Stand still", "Jump"], "answer": "Hide under furniture"},
                {"question": "Which of the following is a disaster preparedness tip?", "options": ["Ignore news", "Have emergency kit", "Panic", "Stay outside"], "answer": "Have emergency kit"},
                {"question": "Cyclones usually form over?", "options": ["Deserts", "Mountains", "Oceans", "Forests"], "answer": "Oceans"},
                {"question": "Floods are caused due to?", "options": ["Drought", "Fire", "Heavy rainfall", "Cold"], "answer": "Heavy rainfall"},
                {"question": "Which is NOT a natural disaster?", "options": ["Tsunami", "Earthquake", "Terror attack", "Cyclone"], "answer": "Terror attack"},
                {"question": "Which disaster involves lava?", "options": ["Flood", "Hurricane", "Volcanic eruption", "Tornado"], "answer": "Volcanic eruption"},
                {"question": "A tsunami is usually caused by?", "options": ["Forest fire", "Meteor", "Earthquake in ocean", "Snowfall"], "answer": "Earthquake in ocean"}
            ],
            "Medium": [
                {"question": "Which scale measures earthquake intensity?", "options": ["Richter", "Thermometer", "Barometer", "Seismograph"], "answer": "Richter"},
                {"question": "Landslides are most common in?", "options": ["Deserts", "Mountains", "Coasts", "Cities"], "answer": "Mountains"},
                {"question": "Which disaster is predictable?", "options": ["Tornado", "Cyclone", "Earthquake", "Tsunami"], "answer": "Cyclone"},
                {"question": "A major cause of man-made disasters is?", "options": ["Lightning", "Terrorism", "Rain", "Sun"], "answer": "Terrorism"},
                {"question": "Which organization handles disasters in India?", "options": ["NASA", "NDMA", "ISRO", "WHO"], "answer": "NDMA"},
                {"question": "Which event can lead to a tsunami?", "options": ["Volcano", "Typhoon", "Landslide", "All of these"], "answer": "All of these"},
                {"question": "First thing during fire disaster?", "options": ["Sleep", "Call police", "Call fire dept", "Use water"], "answer": "Call fire dept"},
                {"question": "Cyclone alert is given how many hours before?", "options": ["24", "48", "12", "6"], "answer": "48"},
                {"question": "Which is a type of flood?", "options": ["River", "Urban", "Flash", "All of these"], "answer": "All of these"},
                {"question": "What should you carry in disaster kit?", "options": ["Books", "Clothes", "Emergency supplies", "Games"], "answer": "Emergency supplies"}
            ],
            "Difficult": [
                {"question": "Seismograph measures what?", "options": ["Wind", "Tide", "Earthquakes", "Temperature"], "answer": "Earthquakes"},
                {"question": "What is the Fujita scale used for?", "options": ["Cyclones", "Floods", "Tornadoes", "Volcanoes"], "answer": "Tornadoes"},
                {"question": "The epicenter of an earthquake is?", "options": ["Surface above focus", "Deepest point", "Fault line", "None"], "answer": "Surface above focus"},
                {"question": "Which satellite helps monitor weather disasters?", "options": ["INSAT", "Chandrayaan", "Mangalyaan", "Astra"], "answer": "INSAT"},
                {"question": "Which chemical causes industrial disasters?", "options": ["CO2", "Bhopal Gas (MIC)", "Oxygen", "Water"], "answer": "Bhopal Gas (MIC)"},
                {"question": "Disaster Management Act was enacted in?", "options": ["2005", "2010", "1990", "2015"], "answer": "2005"},
                {"question": "Which is a slow onset disaster?", "options": ["Flood", "Drought", "Earthquake", "Tsunami"], "answer": "Drought"},
                {"question": "Which of these is a secondary disaster?", "options": ["Flood", "Fire after quake", "Earthquake", "Cyclone"], "answer": "Fire after quake"},
                {"question": "Disaster risk is measured by?", "options": ["Probability", "Damage", "Vulnerability", "All of these"], "answer": "All of these"},
                {"question": "UN agency for disaster reduction?", "options": ["UNDRR", "UNICEF", "WHO", "UNDP"], "answer": "UNDRR"}
            ]
        },
        "Crime": {
            "Easy": [
                {"question": "What number do you call for police in India?", "options": ["100", "911", "112", "101"], "answer": "100"},
                {"question": "What should you do if you witness a crime?", "options": ["Run", "Report to police", "Record it", "Ignore it"], "answer": "Report to police"},
                {"question": "Which of these is a cybercrime?", "options": ["Theft", "Phishing", "Burglary", "Murder"], "answer": "Phishing"},
                {"question": "Pickpocketing usually happens in?", "options": ["Crowded areas", "Empty roads", "Parks", "Home"], "answer": "Crowded areas"},
                {"question": "Which is a financial crime?", "options": ["Murder", "Forgery", "Assault", "Kidnapping"], "answer": "Forgery"},
                {"question": "Who investigates major crimes?", "options": ["Traffic police", "CBI", "Forest officer", "Farmer"], "answer": "CBI"},
                {"question": "What is IPC in India?", "options": ["Code of conduct", "Penal Code", "Police Code", "None"], "answer": "Penal Code"},
                {"question": "Which is NOT a crime?", "options": ["Helping someone", "Theft", "Hacking", "Fraud"], "answer": "Helping someone"},
                {"question": "To avoid online scams, never share?", "options": ["Your name", "Your food", "Your OTP", "Your email"], "answer": "Your OTP"},
                {"question": "Crime rate is higher in?", "options": ["Cities", "Villages", "Forests", "Mountains"], "answer": "Cities"}
            ],
            "Medium": [
            {"question": "Which crime involves stealing from someone's pocket or bag?", "options": ["Burglary", "Pickpocketing", "Hacking", "Fraud"], "answer": "Pickpocketing"},
            {"question": "Which of the following is a cybercrime?", "options": ["Robbery", "Phishing", "Kidnapping", "Shoplifting"], "answer": "Phishing"},
            {"question": "Which law deals with juvenile crime in India?", "options": ["IPC", "POCSO", "Juvenile Justice Act", "NDPS Act"], "answer": "Juvenile Justice Act"},
            {"question": "Which document is needed to file an FIR?", "options": ["Aadhar card", "Driving License", "None", "Passport"], "answer": "None"},
            {"question": "What is stalking?", "options": ["Following someone without consent", "Helping a stranger", "Reporting a crime", "Sharing food"], "answer": "Following someone without consent"},
            {"question": "What does the term 'IPC' stand for?", "options": ["Indian Personal Code", "Indian Penal Code", "Indian Police Code", "Investigation Procedure Code"], "answer": "Indian Penal Code"},
            {"question": "Who investigates crimes in India?", "options": ["Lawyers", "Judges", "Police", "Citizens"], "answer": "Police"},
            {"question": "Which is a form of online abuse?", "options": ["Phishing", "Spam", "Cyberbullying", "All of these"], "answer": "All of these"},
            {"question": "What does CCTV stand for?", "options": ["Close Circuit Television", "Camera Circuit TV", "Closed Cell Television", "None of these"], "answer": "Close Circuit Television"},
            {"question": "What should you do if you witness a crime?", "options": ["Ignore it", "Call the police", "Run away", "Record for social media"], "answer": "Call the police"},
            ],

            "Difficult": [
                {"question": "Which section of IPC deals with murder?", "options": ["302", "420", "376", "144"], "answer": "302"},
                {"question": "What is the punishment for cyber terrorism under the IT Act?", "options": ["Life imprisonment", "6 months", "2 years", "Fine only"], "answer": "Life imprisonment"},
                {"question": "What does POCSO Act protect?", "options": ["Senior citizens", "Environment", "Children from sexual offenses", "Animals"], "answer": "Children from sexual offenses"},
                {"question": "Which organization investigates economic crimes in India?", "options": ["CBI", "RAW", "ED", "NIA"], "answer": "ED"},
                {"question": "Which IPC section deals with theft?", "options": ["378", "302", "498A", "153A"], "answer": "378"},
                {"question": "What is a bailable offense?", "options": ["Can apply for bail", "Cannot be bailed", "Only judges can decide", "Police must approve"], "answer": "Can apply for bail"},
                {"question": "Which act deals with corruption in India?", "options": ["Prevention of Corruption Act", "RTI Act", "POCSO", "NDPS Act"], "answer": "Prevention of Corruption Act"},
                {"question": "Who can file a PIL in court?", "options": ["Only lawyers", "Any citizen", "Only victims", "Only police"], "answer": "Any citizen"},
                {"question": "What is 'habeas corpus' used for?", "options": ["Release unlawfully detained person", "Punish a criminal", "Enforce traffic laws", "Seize property"], "answer": "Release unlawfully detained person"},
                {"question": "Which article in the Indian Constitution guarantees protection of life and personal liberty?", "options": ["Article 21", "Article 370", "Article 19", "Article 14"], "answer": "Article 21"},

            ]
        },
        "Weather": {
            "Easy": [
                {"question": "What does a thermometer measure?", "options": ["Pressure", "Rain", "Temperature", "Wind"], "answer": "Temperature"},
                {"question": "Which season has the most rainfall?", "options": ["Summer", "Monsoon", "Winter", "Autumn"], "answer": "Monsoon"},
                {"question": "What does a barometer measure?", "options": ["Wind", "Humidity", "Pressure", "Temperature"], "answer": "Pressure"},
                {"question": "Which instrument measures rainfall?", "options": ["Hygrometer", "Anemometer", "Rain gauge", "Thermometer"], "answer": "Rain gauge"},
                {"question": "Which cloud brings rain?", "options": ["Cirrus", "Cumulonimbus", "Stratus", "Altocumulus"], "answer": "Cumulonimbus"},
                {"question": "Snowfall usually happens in?", "options": ["Desert", "Mountains", "Coast", "River"], "answer": "Mountains"},
                {"question": "What is the wind that changes direction with seasons called?", "options": ["Storm", "Monsoon", "Breeze", "Tornado"], "answer": "Monsoon"},
                {"question": "Which color in weather map shows heavy rainfall?", "options": ["Red", "Blue", "Green", "White"], "answer": "Red"},
                {"question": "Which device shows wind speed?", "options": ["Thermometer", "Barometer", "Anemometer", "Hygrometer"], "answer": "Anemometer"},
                {"question": "Humidity means?", "options": ["Dry air", "Moisture in air", "Windy weather", "Rain"], "answer": "Moisture in air"}
            ],
            "Medium": [
                {"question": "What is the main cause of wind?", "options": ["Sunlight", "Clouds", "Temperature difference", "Rain"], "answer": "Temperature difference"},
                {"question": "What do we call a rotating column of air that touches both the cloud base and the Earth?", "options": ["Cyclone", "Hurricane", "Tornado", "Storm"], "answer": "Tornado"},
                {"question": "Which instrument measures air pressure?", "options": ["Thermometer", "Barometer", "Anemometer", "Hygrometer"], "answer": "Barometer"},
                {"question": "What does a hygrometer measure?", "options": ["Temperature", "Humidity", "Wind speed", "Rainfall"], "answer": "Humidity"},
                {"question": "Which cloud type is associated with thunderstorms?", "options": ["Stratus", "Cirrus", "Cumulonimbus", "Nimbostratus"], "answer": "Cumulonimbus"},
                {"question": "What does the ozone layer protect us from?", "options": ["Infrared rays", "Microwaves", "Ultraviolet rays", "Visible light"], "answer": "Ultraviolet rays"},
                {"question": "What is the term for weather patterns lasting 30+ years?", "options": ["Forecast", "Storm", "Climate", "Trend"], "answer": "Climate"},
                {"question": "Which wind blows consistently from the same direction?", "options": ["Trade winds", "Cyclones", "Gusts", "Westerlies"], "answer": "Trade winds"},
                {"question": "What causes lightning?", "options": ["Rain", "Hail", "Static electricity", "Snow"], "answer": "Static electricity"},
                {"question": "El Niño affects which ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"}

            ],
            "Difficult": [
                {"question": "Which scale is used to measure tornado intensity?", "options": ["Saffir-Simpson", "Richter", "Fujita", "Mercalli"], "answer": "Fujita"},
                {"question": "What is the Coriolis effect?", "options": ["Ocean cooling", "Wind direction change due to Earth rotation", "Rain formation", "Cloud pattern shift"], "answer": "Wind direction change due to Earth rotation"},
                {"question": "Which gas is most abundant in Earth’s atmosphere?", "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Nitrogen"},
                {"question": "A sudden violent flood is known as?", "options": ["River flood", "Flash flood", "Storm surge", "Monsoon"], "answer": "Flash flood"},
                {"question": "What are isobars?", "options": ["Temperature lines", "Pressure lines", "Humidity levels", "Wind symbols"], "answer": "Pressure lines"},
                {"question": "Which layer of the atmosphere contains the ozone layer?", "options": ["Mesosphere", "Thermosphere", "Stratosphere", "Troposphere"], "answer": "Stratosphere"},
                {"question": "Which phenomenon warms the Earth’s surface?", "options": ["Albedo", "Greenhouse effect", "Ozone layer", "Reflection"], "answer": "Greenhouse effect"},
                {"question": "What is the Beaufort scale used for?", "options": ["Humidity", "Wind speed", "Air pressure", "Temperature"], "answer": "Wind speed"},
                {"question": "What is the term for a period of abnormally dry weather?", "options": ["Drought", "Famine", "Flood", "Cyclone"], "answer": "Drought"},
                {"question": "What forms dew?", "options": ["Condensation of water vapor on cool surfaces", "Precipitation", "Fog", "Evaporation"], "answer": "Condensation of water vapor on cool surfaces"}

            ]
        },
        "General": {
            "Easy": [
                {"question": "Which of these is a safety app?", "options": ["Awarenow", "Netflix", "Instagram", "Maps"], "answer": "Awarenow"},
                {"question": "Who helps in emergencies?", "options": ["Police", "Doctor", "Firefighter", "All of them"], "answer": "All of them"},
                {"question": "Which item is useful in first aid?", "options": ["Pen", "Bandage", "Phone", "Book"], "answer": "Bandage"},
                {"question": "What should you dial in fire emergency?", "options": ["102", "100", "101", "108"], "answer": "101"},
                {"question": "Which is NOT a safety rule?", "options": ["Run on roads", "Use seatbelt", "Obey traffic", "Stay alert"], "answer": "Run on roads"},
                {"question": "Which of these is a disaster?", "options": ["Earthquake", "Cyclone", "Flood", "All of them"], "answer": "All of them"},
                {"question": "Awareness helps in?", "options": ["More panic", "More damage", "Better response", "More crime"], "answer": "Better response"},
                {"question": "Which is a warning sign?", "options": ["STOP", "GO", "TURN", "U-TURN"], "answer": "STOP"},
                {"question": "What should you carry during travel?", "options": ["Snacks", "Phone", "Water", "All of these"], "answer": "All of these"},
                {"question": "Which is used for navigation?", "options": ["GPS", "Camera", "Calculator", "Scanner"], "answer": "GPS"}
            ],
            "Medium": [
                {"question": "What is the emergency number for ambulance in India?", "options": ["108", "101", "100", "911"], "answer": "108"},
                {"question": "Which government app promotes disaster alerts in India?", "options": ["WeatherNow", "MyGov", "SACHET", "Suraksha"], "answer": "SACHET"},
                {"question": "What does GPS stand for?", "options": ["Global Protection System", "Global Positioning System", "Geo Protocol Standard", "Geo Protected Service"], "answer": "Global Positioning System"},
                {"question": "Which color is usually associated with warning signs?", "options": ["Red", "Blue", "Green", "White"], "answer": "Red"},
                {"question": "What is a fire drill?", "options": ["Real fire event", "Firefighting class", "Emergency evacuation practice", "Gas leak control"], "answer": "Emergency evacuation practice"},
                {"question": "Which of the following is a safe password?", "options": ["123456", "password", "qwerty", "L1on@2024"], "answer": "L1on@2024"},
                {"question": "What does CCTV stand for?", "options": ["Closed Circuit Television", "Camera Controlled TV", "Central Camera Transmission", "Close Camera Tracking"], "answer": "Closed Circuit Television"},
                {"question": "Which app helps track your location in emergency?", "options": ["Instagram", "WhatsApp", "Google Maps", "Awarenow"], "answer": "Awarenow"},
                {"question": "Which of these is a personal safety tip?", "options": ["Ignore surroundings", "Always share passwords", "Stay in well-lit areas", "Never carry ID"], "answer": "Stay in well-lit areas"},
                {"question": "Which body issues weather warnings in India?", "options": ["ISRO", "NASA", "IMD", "NDRF"], "answer": "IMD"}

            ],
            "Difficult": [
                {"question": "What is phishing?", "options": ["Fishing in rivers", "Hacking through physical access", "Fraudulent attempt to obtain sensitive info", "Virus attack"], "answer": "Fraudulent attempt to obtain sensitive info"},
                {"question": "Which agency responds to disasters in India?", "options": ["CRPF", "CISF", "NDRF", "BSF"], "answer": "NDRF"},
                {"question": "What is end-to-end encryption?", "options": ["Basic security", "Encryption during login", "Only sender can encrypt", "Only sender and receiver can read messages"], "answer": "Only sender and receiver can read messages"},
                {"question": "Which Indian app is used for citizen safety alerts?", "options": ["BHIM", "UMANG", "112 India", "RTO Alert"], "answer": "112 India"},
                {"question": "What is the purpose of a panic button in mobile apps?", "options": ["Play music", "Call randomly", "Send emergency alert with location", "Open camera"], "answer": "Send emergency alert with location"},
                {"question": "What does GDPR stand for?", "options": ["General Data Protection Regulation", "Global Disaster Plan Rule", "Government Data Protection Rule", "Geo Data Privacy Regulation"], "answer": "General Data Protection Regulation"},
                {"question": "Which of the following is considered strong cyber hygiene?", "options": ["Click unknown links", "Avoid software updates", "Use same passwords", "Enable 2FA"], "answer": "Enable 2FA"},
                {"question": "Which act governs IT crimes in India?", "options": ["Cyber Law Act", "Information Technology Act", "Data Safety Bill", "Security Regulation Act"], "answer": "Information Technology Act"},
                {"question": "Which is a wearable safety device?", "options": ["Smartwatch with SOS", "Headphones", "Fitness tracker", "Camera lens"], "answer": "Smartwatch with SOS"},
                {"question": "Who can access your location via safety apps?", "options": ["Unknown people", "Friends list only", "Everyone", "People with permission"], "answer": "People with permission"}

            ]
        }
    }


    # ------------------------------
    # --- Certificate Generator ---
    # ------------------------------
    def generate_certificate(name, score, topic, filename=None):
        if filename is None:
            unique_id = uuid.uuid4().hex[:6]
            filename = f"certificate_{name.replace(' ', '_')}_{score}_{unique_id}.pdf"

        c = canvas.Canvas(filename, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Border
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(6)
        c.rect(20, 20, width - 40, height - 40)

        # Title
        c.setFont("Helvetica-Bold", 40)
        c.setFillColor(colors.darkblue)
        c.drawCentredString(width / 2, height - 100, "AWARENOW")

        # Subtitle
        c.setFont("Helvetica-Oblique", 18)
        c.setFillColor(colors.black)
        c.drawCentredString(width / 2, height - 140, "Certificate of Achievement")

        # Name
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(width / 2, height - 190, name)

        # Achievement
        c.setFont("Helvetica", 18)
        c.drawCentredString(width / 2, height - 240,
                            f"has successfully completed the Awarenow Quiz on '{topic}' with distinction.")
        c.drawCentredString(width / 2, height - 270,
                            f"Score Achieved: {score}%")

        # Date
        date_str = datetime.now().strftime("%B %d, %Y")
        c.setFont("Helvetica-Oblique", 14)
        c.drawCentredString(width / 2, height - 300, f"Date: {date_str}")

        # Signatures
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 80, "__________________")
        c.drawString(width - 250, 80, "__________________")
        c.setFont("Helvetica", 14)
        c.drawString(120, 60, "Authorized Signatory")
        c.drawString(width - 230, 60, "Coordinator")

        c.showPage()
        c.save()

        return filename

    # Optional file cleanup
    def remove_file_later(path, delay=60):
        time.sleep(delay)
        if os.path.exists(path):
            os.remove(path)

    # ------------------------------
    # --- Streamlit App UI ---
    # ------------------------------
    st.set_page_config("Quiz App", layout="centered")
    st.title("Awarenow Quiz Challenge")

    # --- Session State Initialization ---
    if "quiz" not in st.session_state:
        st.session_state.quiz = []
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.certificate_generated = False

    # --- Name and Topic Selection ---
    if not st.session_state.quiz:
        st.subheader(" Enter your name to begin")
        name = st.text_input("Your Name:")
        topic = st.selectbox("Choose a topic:", list(quiz_data.keys()))
        difficulty = st.radio("Select difficulty:", ["Easy", "Medium", "Difficult"], horizontal=True)

        if st.button("Start Quiz", type="primary"):
            username = name.strip()
            if username == "":
                st.warning(" Please enter your name to continue.")
            else:
                st.session_state.username = username
                selected_questions = quiz_data[topic][difficulty]
                random.shuffle(selected_questions)
                st.session_state.quiz = selected_questions[:10]
                st.session_state.q_index = 0
                st.session_state.score = 0
                st.session_state.topic = topic
                st.rerun()

    # --- Quiz In Progress ---
    elif st.session_state.q_index < len(st.session_state.quiz):
        q = st.session_state.quiz[st.session_state.q_index]
        st.subheader(f"Q{st.session_state.q_index + 1}: {q['question']}")
        user_answer = st.radio("Choose your answer:", q["options"], key=f"answer_{st.session_state.q_index}")

        if st.button("Submit Answer"):
            if user_answer == q["answer"]:
                st.session_state.score += 1
                st.success(" Correct!")
            else:
                st.error(f" Wrong! Correct answer: {q['answer']}")
            st.session_state.q_index += 1
            time.sleep(1.5)
            st.rerun()

    # --- Quiz Complete ---
    else:
        st.success(" You completed the quiz!")
        score = st.session_state.score
        total = len(st.session_state.quiz)
        percent = (score / total) * 100
        username = st.session_state.get("username", "User")
        st.write(f"**{username}**, your score: **{score} / {total}** (**{percent:.0f}%**)")
        st.balloons()

        if percent >= 60 and not st.session_state.certificate_generated:
            cert_path = generate_certificate(username, int(percent), st.session_state.topic)
            st.success("Congratulations! You've earned a certificate.")

            with open(cert_path, "rb") as f:
                st.download_button(
                    label=" Download Certificate",
                    data=f,
                    file_name=os.path.basename(cert_path),
                    mime="application/pdf"
                )

            st.session_state.certificate_generated = True

            # Optionally clean up file after 1 minute
            threading.Thread(target=remove_file_later, args=(cert_path,), daemon=True).start()

        elif percent < 60:
            st.info(" Score at least 60% to earn a certificate. Try again!")

        if st.button(" Play Again"):
            st.session_state.quiz = []
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.username = ""
            st.session_state.certificate_generated = False
            st.rerun()