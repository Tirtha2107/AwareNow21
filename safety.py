# def safety():
#     import streamlit as st
#     import requests

#     st.set_page_config(page_title="Safety Information", layout="wide")
#     st.title("Safety Information Center")

#     # Define categories and incidents
#     categories = {
#         "Crime": [
#             "Theft / Pickpocketing",
#             "Robbery (Armed/Unarmed)",
#             "Assault",
#             "Burglary (Home Invasion)",
#             "Fraud / Scam",
#             "Cybercrime (Hacking, Identity Theft)",
#             "Kidnapping / Abduction",
#             "Harassment / Stalking",
#             "Vandalism",
#             "Human Trafficking"
#         ],
#         "Disaster": [
#             "Earthquake",
#             "Flood",
#             "Tsunami",
#             "Landslide",
#             "Volcanic Eruption",
#             "Wildfire",
#             "Hurricane / Cyclone / Typhoon",
#             "Tornado",
#             "Avalanche",
#             "Drought"
#         ],
#         "Weather": [
#             "Thunderstorm / Lightning",
#             "Extreme Heat / Heatwave",
#             "Extreme Cold / Blizzard",
#             "Heavy Rain / Monsoon Flooding",
#             "Dense Fog",
#             "Hailstorm",
#             "Dust Storm / Sandstorm",
#             "Ice Storm",
#             "Strong Winds / Gusts",
#             "Severe Snowstorm"
#         ]
#     }

#     # Tips dictionary
#     incident_tips = {
#         # Crime tips
#         "Theft / Pickpocketing": [
#             "Keep valuables out of sight and secure.",
#             "Use anti-theft bags or money belts.",
#             "Be alert in crowded areas.",
#             "Avoid displaying expensive items in public.",
#             "Report theft to local authorities immediately."
#         ],
#         "Robbery (Armed/Unarmed)": [
#             "Stay calm and do not resist.",
#             "Observe details about the suspect.",
#             "Comply with demands to avoid escalation.",
#             "Call police as soon as it is safe.",
#             "Seek medical and emotional support."
#         ],
#         "Assault": [
#             "Get to a safe location immediately.",
#             "Call emergency services.",
#             "Avoid confronting the attacker again.",
#             "Preserve evidence if reporting to police.",
#             "Seek medical attention even for minor injuries."
#         ],
    #     "Burglary (Home Invasion)": [
    #         "Leave the premises if possible.",
    #         "Call police from a safe location.",
    #         "Do not attempt to confront burglars.",
    #         "Secure doors and windows in the future.",
    #         "Consider installing a security system."
    #     ],
    #     "Fraud / Scam": [
    #         "Do not share personal or financial info.",
    #         "Verify the identity of callers or senders.",
    #         "Avoid clicking suspicious links.",
    #         "Report scams to authorities.",
    #         "Monitor accounts for suspicious activity."
    #     ],
    #     "Cybercrime (Hacking, Identity Theft)": [
    #         "Change compromised passwords immediately.",
    #         "Enable two-factor authentication.",
    #         "Scan devices for malware.",
    #         "Report to cybercrime authorities.",
    #         "Monitor financial accounts closely."
    #     ],
    #     "Kidnapping / Abduction": [
    #         "Try to signal for help discreetly.",
    #         "Remember details of surroundings.",
    #         "Look for escape opportunities safely.",
    #         "Comply with captor instructions to stay safe.",
    #         "Contact authorities immediately upon release."
    #     ],
    #     "Harassment / Stalking": [
    #         "Document all incidents.",
    #         "Block and avoid contact.",
    #         "Inform trusted friends/family.",
    #         "Report to authorities if it escalates.",
    #         "Increase personal security measures."
    #     ],
    #     "Vandalism": [
    #         "Do not confront vandals directly.",
    #         "Document damage with photos.",
    #         "Report to police or local authorities.",
    #         "Secure property to prevent future incidents.",
    #         "Consider security cameras."
    #     ],
    #     "Human Trafficking": [
    #         "Be cautious of suspicious job offers.",
    #         "Avoid traveling with strangers.",
    #         "Report suspicious activities immediately.",
    #         "Know local helplines.",
    #         "Trust your instincts."
    #     ],

    #     # Disaster tips
    #     "Earthquake": [
    #         "Drop, cover, and hold on during shaking.",
    #         "Stay away from windows and heavy objects.",
    #         "If outdoors, move to an open area.",
    #         "After shaking stops, evacuate if unsafe.",
    #         "Check for injuries and hazards."
    #     ],
    #     "Flood": [
    #         "Move to higher ground immediately.",
    #         "Avoid walking or driving through floodwaters.",
    #         "Listen to local alerts and instructions.",
    #         "Turn off electricity if safe to do so.",
    #         "Stay away from fast-moving water."
    #     ],
    #     "Tsunami": [
    #         "Move to higher ground without delay.",
    #         "Follow evacuation orders.",
    #         "Stay away from beaches until official all-clear.",
    #         "Avoid rivers and streams flowing into the ocean.",
    #         "Monitor emergency broadcasts."
    #     ],
    #     "Landslide": [
    #         "Move away from the path of the landslide.",
    #         "Be alert to unusual sounds like cracking trees.",
    #         "Evacuate immediately if advised.",
    #         "Avoid river valleys and low areas.",
    #         "Watch for flooding after a landslide."
    #     ],
    #     "Volcanic Eruption": [
    #         "Follow evacuation orders quickly.",
    #         "Wear masks to avoid inhaling ash.",
    #         "Stay indoors if ash is falling.",
    #         "Avoid rivers and streams downstream of volcano.",
    #         "Protect electronics from ash."
    #     ],
    #     "Wildfire": [
    #         "Evacuate immediately if told.",
    #         "Close all windows and vents.",
    #         "Wear masks to avoid smoke inhalation.",
    #         "Keep emergency kit ready.",
    #         "Avoid driving through heavy smoke."
    #     ],
    #     "Hurricane / Cyclone / Typhoon": [
    #         "Secure your home and belongings.",
    #         "Stock emergency supplies.",
    #         "Evacuate if ordered by authorities.",
    #         "Stay indoors during the storm.",
    #         "Avoid flooded roads."
    #     ],
    #     "Tornado": [
    #         "Seek shelter in a basement or interior room.",
    #         "Stay away from windows.",
    #         "Cover yourself with a mattress or blanket.",
    #         "Listen to weather updates.",
    #         "Stay put until all-clear."
    #     ],
    #     "Avalanche": [
    #         "Move to the side of the avalanche path.",
    #         "Drop heavy gear to move faster.",
    #         "Use swimming motion to stay on surface.",
    #         "Create an air pocket if buried.",
    #         "Call for help immediately."
    #     ],
    #     "Drought": [
    #         "Conserve water at home and work.",
    #         "Avoid wasting water outdoors.",
    #         "Store emergency drinking water.",
    #         "Follow water restrictions.",
    #         "Plant drought-resistant vegetation."
    #     ],

    #     # Weather tips
    #     "Thunderstorm / Lightning": [
    #         "Seek shelter indoors immediately.",
    #         "Avoid tall structures and trees.",
    #         "Stay away from windows.",
    #         "Unplug electrical appliances.",
    #         "Wait 30 minutes after thunder before going out."
    #     ],
    #     "Extreme Heat / Heatwave": [
    #         "Stay hydrated and avoid direct sun.",
    #         "Wear light, loose-fitting clothing.",
    #         "Avoid strenuous activity outdoors.",
    #         "Check on vulnerable people.",
    #         "Stay in cool or shaded areas."
    #     ],
    #     "Extreme Cold / Blizzard": [
    #         "Stay indoors and keep warm.",
    #         "Wear multiple layers outdoors.",
    #         "Avoid travel unless necessary.",
    #         "Keep emergency supplies ready.",
    #         "Protect pets from the cold."
    #     ],
    #     "Heavy Rain / Monsoon Flooding": [
    #         "Avoid flood-prone areas.",
    #         "Stay indoors if possible.",
    #         "Do not drive through water.",
    #         "Keep valuables on higher shelves.",
    #         "Listen to weather alerts."
    #     ],
    #     "Dense Fog": [
    #         "Drive slowly with fog lights on.",
    #         "Avoid unnecessary travel.",
    #         "Use road reflectors for guidance.",
    #         "Keep a safe distance from other vehicles.",
    #         "Stay alert for sudden stops."
    #     ],
    #     "Hailstorm": [
    #         "Seek shelter indoors or in a vehicle.",
    #         "Stay away from windows.",
    #         "Protect pets and livestock.",
    #         "Avoid driving until it passes.",
    #         "Check for damage after the storm."
    #     ],
    #     "Dust Storm / Sandstorm": [
    #         "Stay indoors during the storm.",
    #         "Close windows and doors.",
    #         "Wear a mask if outside.",
    #         "Avoid driving in low visibility.",
    #         "Wait until conditions improve."
    #     ],
    #     "Ice Storm": [
    #         "Avoid travel due to slippery roads.",
    #         "Stay indoors to prevent injury.",
    #         "Keep emergency heat sources ready.",
    #         "Stay away from fallen power lines.",
    #         "Stock food and water."
    #     ],
    #     "Strong Winds / Gusts": [
    #         "Secure outdoor objects.",
    #         "Stay indoors during high winds.",
    #         "Avoid walking near trees and power lines.",
    #         "Park vehicles in sheltered areas.",
    #         "Listen to weather updates."
    #     ],
    #     "Severe Snowstorm": [
    #         "Avoid unnecessary travel.",
    #         "Wear warm, layered clothing.",
    #         "Keep emergency supplies in vehicle.",
    #         "Stay indoors during heavy snow.",
    #         "Clear snow from roofs if safe."
    #     ]
    # }

#     # Media links (can be expanded later)
#     video_links = {
#         "Earthquake": "https://www.youtube.com/watch?v=BLEPakj1YTY",
#         "Flood": "https://youtu.be/43M5mZuzHF8?si=R-3IOVTyfKuVDZn4",
#         "Tsunami" : "https://youtu.be/m7EDddq9ftQ?si=1exAIzOcR62D64Zb",
#         "Landslide": "https://youtu.be/9j_StYqR_Pg?si=oe7AkSvdxQufe-SH",
#         "Volcanic Eruption": "https://youtu.be/1rixHFw4Efg?si=i9Ts7BuP8tjFt7e4",
#         "wildfire": "https://youtu.be/apwK7Y362qU?si=30gzFpo3NhKQdhUf",
#         "Hurricane / Cyclone / Typhoon": "https://youtu.be/xHRbnuB9F1I?si=cFzqeomBOxRU52Dp",
#         "Tornado": "https://www.youtube.com/watch?v=_5TiTfuvotc",
#         "Avalanche": "https://youtu.be/8Vq-RkdwArA?si=xBkE4c1VUYSv8gdR",
#         "Droughts": "https://youtu.be/48OlDCI_Xrw?si=RF2YHegRec6rWV3_",
#         "Cybercrime (Hacking, Identity Theft)": "https://youtu.be/EHqXMxY4_Nk?si=sTJeAHsRfRz7E_8W",
#     }
#     default_image = {
#         "Earthquake": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Collapsed_building_in_Christchurch.jpg",
#         "Flood": "https://upload.wikimedia.org/wikipedia/commons/6/6b/2018_Kerala_floods.jpg",
#         "Theft / Pickpocketing": 'images/theft.jpg',
#         "Robbery (Armed/Unarmed)": 'images/Robbery.jpg',
#         "Severe Snowstorms": 'images/snow.jpg',
#         "Strong Winds / Gusts": "images/winds.avif",
#         "Human Trafficking": "images/trafficking.jpg",
#         "Thunderstorm / Lightning": "images/thunder.webp",
#         "Dust Storm / Sandstorm": "images/sand.jpg",
#         "Heavy Rain / Monsoon Flooding": "images/rain.avif",
#         "Ice Storm": "images/icestorm.avif",
#         "Extreme Heat / Heatwave": "images/heat.webp",
#         "Harassment / Stalking": "images/harresment.jpg",
#         "Hailstorm": "images/hailstorm.jpg",
#         "Fraud / Scam": "images/fraud.png",
#         "Extreme Cold / Blizzard": "images/cold.png",
#         "Dense Fog": "images/fog.jpg",
#         "Kidnapping / Abduction": "images/kidnap.jpg",



#     }

#     # Layout
#     category = st.selectbox("Select Category", list(categories.keys()))
#     incident = st.selectbox("Select Incident", categories[category])

#     st.subheader(f"Safety Tips: {incident}")

#     # Show relevant tips
#     if incident in incident_tips:
#         for tip in incident_tips[incident]:
#             st.write(f"• {tip}")
#     else:
#         st.warning("No specific tips found for this incident.")

#     # Show image or video if available
#     if incident in video_links:
#         st.video(video_links[incident])
#     elif incident in default_image:
#         st.image(default_image[incident], use_container_width=True)
#     else:
#         st.info("No media available for this incident.")





def safety(lang_code):
    import streamlit as st
    from deep_translator import GoogleTranslator

    # Translation helper
    def translate_text(text):
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except Exception:
            return text

    st.set_page_config(page_title=translate_text("Safety Information"), layout="wide")
    st.title(translate_text("Safety Information Center"))

    # Categories (English keys for lookup)
    categories = {
        "Crime": [
            "Theft / Pickpocketing",
            "Robbery (Armed/Unarmed)",
            "Assault",
            "Burglary (Home Invasion)",
            "Fraud / Scam",
            "Cybercrime (Hacking, Identity Theft)",
            "Kidnapping / Abduction",
            "Harassment / Stalking",
            "Vandalism",
            "Human Trafficking"
        ],
        "Disaster": [
            "Earthquake",
            "Flood",
            "Tsunami",
            "Landslide",
            "Volcanic Eruption",
            "Wildfire",
            "Hurricane / Cyclone / Typhoon",
            "Tornado",
            "Avalanche",
            "Drought"
        ],
        "Weather": [
            "Thunderstorm / Lightning",
            "Extreme Heat / Heatwave",
            "Extreme Cold / Blizzard",
            "Heavy Rain / Monsoon Flooding",
            "Dense Fog",
            "Hailstorm",
            "Dust Storm / Sandstorm",
            "Ice Storm",
            "Strong Winds / Gusts",
            "Severe Snowstorm"
        ]
    }

    # Tips dictionary (English keys, English tips)
    incident_tips = {
        "Theft / Pickpocketing": [
            "Keep valuables out of sight and secure.",
            "Use anti-theft bags or money belts.",
            "Be alert in crowded areas.",
            "Avoid displaying expensive items in public.",
            "Report theft to local authorities immediately."
        ],
        "Robbery (Armed/Unarmed)": [
            "Stay calm and do not resist.",
            "Observe details about the suspect.",
            "Comply with demands to avoid escalation.",
            "Call police as soon as it is safe.",
            "Seek medical and emotional support."
        ],
        "Assault": [
            "Get to a safe location immediately.",
            "Call emergency services.",
            "Avoid confronting the attacker again.",
            "Preserve evidence if reporting to police.",
            "Seek medical attention even for minor injuries."
        ],

        "Burglary (Home Invasion)": [
            "Leave the premises if possible.",
            "Call police from a safe location.",
            "Do not attempt to confront burglars.",
            "Secure doors and windows in the future.",
            "Consider installing a security system."
        ],
        "Fraud / Scam": [
            "Do not share personal or financial info.",
            "Verify the identity of callers or senders.",
            "Avoid clicking suspicious links.",
            "Report scams to authorities.",
            "Monitor accounts for suspicious activity."
        ],
        "Cybercrime (Hacking, Identity Theft)": [
            "Change compromised passwords immediately.",
            "Enable two-factor authentication.",
            "Scan devices for malware.",
            "Report to cybercrime authorities.",
            "Monitor financial accounts closely."
        ],
        "Kidnapping / Abduction": [
            "Try to signal for help discreetly.",
            "Remember details of surroundings.",
            "Look for escape opportunities safely.",
            "Comply with captor instructions to stay safe.",
            "Contact authorities immediately upon release."
        ],
        "Harassment / Stalking": [
            "Document all incidents.",
            "Block and avoid contact.",
            "Inform trusted friends/family.",
            "Report to authorities if it escalates.",
            "Increase personal security measures."
        ],
        "Vandalism": [
            "Do not confront vandals directly.",
            "Document damage with photos.",
            "Report to police or local authorities.",
            "Secure property to prevent future incidents.",
            "Consider security cameras."
        ],
        "Human Trafficking": [
            "Be cautious of suspicious job offers.",
            "Avoid traveling with strangers.",
            "Report suspicious activities immediately.",
            "Know local helplines.",
            "Trust your instincts."
        ],

        # Disaster tips
        "Earthquake": [
            "Drop, cover, and hold on during shaking.",
            "Stay away from windows and heavy objects.",
            "If outdoors, move to an open area.",
            "After shaking stops, evacuate if unsafe.",
            "Check for injuries and hazards."
        ],
        "Flood": [
            "Move to higher ground immediately.",
            "Avoid walking or driving through floodwaters.",
            "Listen to local alerts and instructions.",
            "Turn off electricity if safe to do so.",
            "Stay away from fast-moving water."
        ],
        "Tsunami": [
            "Move to higher ground without delay.",
            "Follow evacuation orders.",
            "Stay away from beaches until official all-clear.",
            "Avoid rivers and streams flowing into the ocean.",
            "Monitor emergency broadcasts."
        ],
        "Landslide": [
            "Move away from the path of the landslide.",
            "Be alert to unusual sounds like cracking trees.",
            "Evacuate immediately if advised.",
            "Avoid river valleys and low areas.",
            "Watch for flooding after a landslide."
        ],
        "Volcanic Eruption": [
            "Follow evacuation orders quickly.",
            "Wear masks to avoid inhaling ash.",
            "Stay indoors if ash is falling.",
            "Avoid rivers and streams downstream of volcano.",
            "Protect electronics from ash."
        ],
        "Wildfire": [
            "Evacuate immediately if told.",
            "Close all windows and vents.",
            "Wear masks to avoid smoke inhalation.",
            "Keep emergency kit ready.",
            "Avoid driving through heavy smoke."
        ],
        "Hurricane / Cyclone / Typhoon": [
            "Secure your home and belongings.",
            "Stock emergency supplies.",
            "Evacuate if ordered by authorities.",
            "Stay indoors during the storm.",
            "Avoid flooded roads."
        ],
        "Tornado": [
            "Seek shelter in a basement or interior room.",
            "Stay away from windows.",
            "Cover yourself with a mattress or blanket.",
            "Listen to weather updates.",
            "Stay put until all-clear."
        ],
        "Avalanche": [
            "Move to the side of the avalanche path.",
            "Drop heavy gear to move faster.",
            "Use swimming motion to stay on surface.",
            "Create an air pocket if buried.",
            "Call for help immediately."
        ],
        "Drought": [
            "Conserve water at home and work.",
            "Avoid wasting water outdoors.",
            "Store emergency drinking water.",
            "Follow water restrictions.",
            "Plant drought-resistant vegetation."
        ],

        # Weather tips
        "Thunderstorm / Lightning": [
            "Seek shelter indoors immediately.",
            "Avoid tall structures and trees.",
            "Stay away from windows.",
            "Unplug electrical appliances.",
            "Wait 30 minutes after thunder before going out."
        ],
        "Extreme Heat / Heatwave": [
            "Stay hydrated and avoid direct sun.",
            "Wear light, loose-fitting clothing.",
            "Avoid strenuous activity outdoors.",
            "Check on vulnerable people.",
            "Stay in cool or shaded areas."
        ],
        "Extreme Cold / Blizzard": [
            "Stay indoors and keep warm.",
            "Wear multiple layers outdoors.",
            "Avoid travel unless necessary.",
            "Keep emergency supplies ready.",
            "Protect pets from the cold."
        ],
        "Heavy Rain / Monsoon Flooding": [
            "Avoid flood-prone areas.",
            "Stay indoors if possible.",
            "Do not drive through water.",
            "Keep valuables on higher shelves.",
            "Listen to weather alerts."
        ],
        "Dense Fog": [
            "Drive slowly with fog lights on.",
            "Avoid unnecessary travel.",
            "Use road reflectors for guidance.",
            "Keep a safe distance from other vehicles.",
            "Stay alert for sudden stops."
        ],
        "Hailstorm": [
            "Seek shelter indoors or in a vehicle.",
            "Stay away from windows.",
            "Protect pets and livestock.",
            "Avoid driving until it passes.",
            "Check for damage after the storm."
        ],
        "Dust Storm / Sandstorm": [
            "Stay indoors during the storm.",
            "Close windows and doors.",
            "Wear a mask if outside.",
            "Avoid driving in low visibility.",
            "Wait until conditions improve."
        ],
        "Ice Storm": [
            "Avoid travel due to slippery roads.",
            "Stay indoors to prevent injury.",
            "Keep emergency heat sources ready.",
            "Stay away from fallen power lines.",
            "Stock food and water."
        ],
        "Strong Winds / Gusts": [
            "Secure outdoor objects.",
            "Stay indoors during high winds.",
            "Avoid walking near trees and power lines.",
            "Park vehicles in sheltered areas.",
            "Listen to weather updates."
        ],
        "Severe Snowstorm": [
            "Avoid unnecessary travel.",
            "Wear warm, layered clothing.",
            "Keep emergency supplies in vehicle.",
            "Stay indoors during heavy snow.",
            "Clear snow from roofs if safe."
        ]
    
        # ... (keep your remaining tips exactly as in your original code) ...
    }

    # Media links
    video_links = {
        "Earthquake": "https://www.youtube.com/watch?v=BLEPakj1YTY",
        "Flood": "https://youtu.be/43M5mZuzHF8?si=R-3IOVTyfKuVDZn4",
        "Tsunami" : "https://youtu.be/m7EDddq9ftQ?si=1exAIzOcR62D64Zb",
        "Landslide": "https://youtu.be/9j_StYqR_Pg?si=oe7AkSvdxQufe-SH",
        "Volcanic Eruption": "https://youtu.be/1rixHFw4Efg?si=i9Ts7BuP8tjFt7e4",
        "wildfire": "https://youtu.be/apwK7Y362qU?si=30gzFpo3NhKQdhUf",
        "Hurricane / Cyclone / Typhoon": "https://youtu.be/xHRbnuB9F1I?si=cFzqeomBOxRU52Dp",
        "Tornado": "https://www.youtube.com/watch?v=_5TiTfuvotc",
        "Avalanche": "https://youtu.be/8Vq-RkdwArA?si=xBkE4c1VUYSv8gdR",
        "Droughts": "https://youtu.be/48OlDCI_Xrw?si=RF2YHegRec6rWV3_",
        "Cybercrime (Hacking, Identity Theft)": "https://youtu.be/EHqXMxY4_Nk?si=sTJeAHsRfRz7E_8W",
    }

    # Default images
    default_image = {
        "Earthquake": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Collapsed_building_in_Christchurch.jpg",
        "Flood": "https://upload.wikimedia.org/wikipedia/commons/6/6b/2018_Kerala_floods.jpg",
        "Theft / Pickpocketing": 'images/theft.jpg',
        "Robbery (Armed/Unarmed)": 'images/Robbery.jpg',
        "Severe Snowstorms": 'images/snow.jpg',
        "Strong Winds / Gusts": "images/winds.avif",
        "Human Trafficking": "images/trafficking.jpg",
        "Thunderstorm / Lightning": "images/thunder.webp",
        "Dust Storm / Sandstorm": "images/sand.jpg",
        "Heavy Rain / Monsoon Flooding": "images/rain.avif",
        "Ice Storm": "images/icestorm.avif",
        "Extreme Heat / Heatwave": "images/heat.webp",
        "Harassment / Stalking": "images/harresment.jpg",
        "Hailstorm": "images/hailstorm.jpg",
        "Fraud / Scam": "images/fraud.png",
        "Extreme Cold / Blizzard": "images/cold.png",
        "Dense Fog": "images/fog.jpg",
        "Kidnapping / Abduction": "images/kidnap.jpg",
    }

    # Select category (translated display, English internal key)
    translated_categories = [translate_text(cat) for cat in categories.keys()]
    category_display = st.selectbox(translate_text("Select Category"), translated_categories)
    category_key = list(categories.keys())[translated_categories.index(category_display)]

    # Select incident (translated display, English internal key)
    translated_incidents = [translate_text(inc) for inc in categories[category_key]]
    incident_display = st.selectbox(translate_text("Select Incident"), translated_incidents)
    incident_key = categories[category_key][translated_incidents.index(incident_display)]

    # Show tips
    st.subheader(f"{translate_text('Safety Tips')}: {incident_display}")
    if incident_key in incident_tips:
        for tip in incident_tips[incident_key]:
            st.write(f"• {translate_text(tip)}")
    else:
        st.warning(translate_text("No specific tips found for this incident."))

    # Show media
    if incident_key in video_links:
        st.video(video_links[incident_key])
    elif incident_key in default_image:
        st.image(default_image[incident_key], use_container_width=True)
    else:
        st.info(translate_text("No media available for this incident."))
