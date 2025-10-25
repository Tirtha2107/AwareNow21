
def disaster_heat():    
    import streamlit as st

    st.set_page_config(page_title="India Disaster Heatmap", layout="centered")

    st.markdown(
        "<h1 style='text-align: center; color: #2E86C1;'>India Disaster Heatmap</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 16px; color: #555;'>Select a year and disaster type to view the corresponding heatmap of India</p>",
        unsafe_allow_html=True
    )

    year = st.selectbox("Select Year", ["Select", 2020, 2021, 2022, 2023, 2024])

    disaster_types = ["Select", "Earthquake", "Flood", "Landsliding", "Cyclone", "Wildfires", "Volcanic Eruption"]
    disaster = st.selectbox("Select Disaster Type", disaster_types)

    image_links = {
        (2020, "Earthquake"): "https://upload.wikimedia.org/wikipedia/commons/4/44/Seismic-Map-of-India.png",
        (2020, "Flood"): "https://www.mapsofindia.com/top-ten/geography/india-flood-prone-areas-map-2021.jpg",
        (2020, "Landsliding"): "https://pmfias.b-cdn.net/wp-content/uploads/2024/01/Picture-2-5.png",
        (2020, "Cyclone"): "https://www.researchgate.net/publication/360065714/figure/fig3/AS:1146867601682439@1650445952855/The-number-of-cyclones-occurring-in-nine-Indian-coastal-states-for-2006-2020.jpg",
        (2020, "Wildfires"): "https://www.researchgate.net/publication/388615799/figure/fig5/AS:11431281311793367@1740453631567/Map-showing-different-locations-of-forest-fires-in-India-in-the-year-2020_Q320.jpg",
        (2020, "Volcanic Eruption"): "https://media.geeksforgeeks.org/wp-content/uploads/20240401153934/colcanoes-in-india-1.png",

        (2021, "Earthquake"): "https://upload.wikimedia.org/wikipedia/commons/6/68/India_earthquake_zone_map_en.svg   ",
        (2021, "Flood"): "https://www.researchgate.net/publication/356527540/figure/fig2/AS:1094864993296384@1638047564528/Flood-index-map-for-18-19-May-2021-showing-flooded-regions-due-to-impact-of-Cyclone.png",
        (2021, "Landsliding"): "https://www.researchgate.net/publication/371154156/figure/fig1/AS:11431281162892631@1685456262060/Landslide-prone-states-in-India-as-per-Geological-Survey-of-India-GSI.jpg",
        (2021, "Cyclone"): "https://www.mapsofindia.com/maps/india/cyclone-prone-area.jpg",
        (2021, "Wildfires"): "https://www.iasgyan.in//ig-uploads/images//image00243.png",
        (2021, "Volcanic Eruption"): "https://i.pinimg.com/736x/c1/0a/a3/c10aa3e773c9dd0b29f44351bdacead6.jpg",

        (2022, "Earthquake"):"https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs12040-024-02368-2/MediaObjects/12040_2024_2368_Fig11_HTML.png",
        (2022, "Flood"): "https://upload.wikimedia.org/wikipedia/commons/d/d2/India_flood_zone_map.svg",
        (2022, "Landsliding"): "https://d2av8kbir6lh9m.cloudfront.net/uploads/419_661af93c70dac.png",
        (2022, "Cyclone"): "https://socialissuesindia.wordpress.com/wp-content/uploads/2014/01/indias-cyclone-prone-area.jpg",
        (2022, "Wildfires"): " https://drishtiias.com/images/uploads/1710997825_WHAT'S_BURNING_IN_THE_SUBCONTINENT.png",
        (2022, "Volcanic Eruption"): "https://lotusarise.com/wp-content/uploads/2021/09/Deccan-Traps.jpg",

        (2023, "Earthquake"):"https://sc0.blr1.cdn.digitaloceanspaces.com/inline/hmkazohxgf-1576300838.gif",
        (2023, "Flood"): "https://www.studyiq.com/articles/wp-content/uploads/2023/07/10140055/flood-1024x992.jpg",
        (2023, "Landsliding"): "https://pwonlyias.com/wp-content/uploads/2024/08/unnamed-2024-08-02t165652245-66acd1e79c603.webp",
        (2023, "Cyclone"): "https://www.researchgate.net/publication/347050067/figure/fig1/AS:978416266391555@1610284024637/Cyclone-hazard-map-of-India-Source-BMTPC-India-2019.jpg",
        (2023, "Wildfires"): "https://drishtiias.com/images/uploads/1739536267_Fire_Prone_States.png",
        (2023, "Volcanic Eruption"): "https://lotusarise.com/wp-content/uploads/2024/02/India-Volcanoes-882x1024.png",

        (2024, "Earthquake"):"https://mapsforupsc.com/wp-content/uploads/2025/04/Seismic-Zones-of-India-Map.png",
        (2024, "Flood"): "https://sandrp.in/wp-content/uploads/2024/07/1.-subdiv.jpeg?w=982",
        (2024, "Landsliding"): "https://exampariksha.com/wp-content/uploads/2015/03/landslide-india-profile.png",
        (2024, "Cyclone"): "https://qph.cf2.quoracdn.net/main-qimg-df2925c69657f9cce4e8a3b00616a116-lq",
        (2024, "Wildfires"): "https://images.news18.com/ibnlive/uploads/2024/12/forest-fires-2024-12-e0e6e9c5174cae30417c95f2fb45a15f.png?impolicy=website&width=0&height=0",
        (2024, "Volcanic Eruption"): "https://lotusarise.com/wp-content/uploads/2021/09/Dhinodhar-Hills.jpg",
    }

    if year != "Select" and disaster != "Select":
        st.markdown(
            f"""
            <div style='text-align:center; margin-bottom: 10px;'>
                <span style='background-color:#1ABC9C; color:white; padding:6px 14px; border-radius:8px; font-size:16px; margin-right: 10px;'>
                    Year: {year}
                </span>
                <span style='background-color:#E67E22; color:white; padding:6px 14px; border-radius:8px; font-size:16px;'>
                    Disaster: {disaster}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        img_path = image_links.get((year, disaster))
        if img_path:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <img src="{img_path}" alt="Heatmap - {year} - {disaster}" 
                        style="border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); max-width: 95%;">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("No image available for the selected year and disaster type.")