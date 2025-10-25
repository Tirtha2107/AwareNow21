def crime_heat():
    import streamlit as st

    st.markdown(
        "<h1 style='text-align: center; color: #2E86C1;'> India Crime Heatmap</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; font-size: 16px; color: #555;'>Select a year to view the corresponding crime heatmap of India</p>",
        unsafe_allow_html=True
    )

    year = st.selectbox("Select Year", ["Select",2011,2012,2013,2014,2015,2016, 2017,2018, 2019, 2020,2021, 2022, 2023, 2024])

    image_links = {

        2011:"https://www.researchgate.net/publication/320869704/figure/fig12/AS:557649246814208@1509965349706/Crime-map-of-India-i-crime-density-2011.png",
        2012:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/2012_Crime_Rate_against_Women_per_100000_in_India_by_its_States_and_Union_Territories%2C_VAW_Map.svg/960px-2012_Crime_Rate_against_Women_per_100000_in_India_by_its_States_and_Union_Territories%2C_VAW_Map.svg.png",
        2013:"https://pbs.twimg.com/media/GVpX0h7WwAAculP.jpg:large",
        2014:"https://www.geocurrents.info/wp-content/uploads/2014/05/India-2014-Election-map.png",
        2015:"https://gigadom.files.wordpress.com/2015/10/32.png?w=584",
        2016:"https://www.researchgate.net/publication/367162714/figure/fig2/AS:11431281113253407@1673802790200/Rate-of-IPC-Crimes-During-2016-Source-2016-report-of-NCRB-National-Crime-Records.png",
        2017:"https://www.mapsofindia.com/ci-moi-images/my-india//2019/10/map-showing-ipc-crime-data.jpg",
        2018:"https://www.drishtiias.com/images/uploads/1578644164_image2.jpg",
        2019:"https://akm-img-a-in.tosshub.com/indiatoday/images/bodyeditor/202009/Dalit_rape-02-x1536.jpg?NpI._bcXc.M51_YZ3wWATyvPz8MEyPcQ?size=750:*",
        2020: "https://pbs.twimg.com/media/FA7DOraVcAAE5ml?format=jpg&name=4096x4096",
        2021: "https://www.researchgate.net/publication/381672770/figure/fig1/AS:11431281254836694@1719323118959/Rates-of-Crimes-Against-Children-Across-States-UTs-in-India-2021-Click-here-to-access.png ",
        2022: " https://preview.redd.it/crime-against-women-in-the-indian-states-v0-9v5vcigfarqd1.jpeg?auto=webp&s=fb7ccf4c0360bb3d8b5056e0659b3d74ec0f51fe",
        2023: "https://pbs.twimg.com/media/GBEAgiSasAA0-KY?format=jpg&name=4096x4096",
        2024: "https://pbs.twimg.com/media/GySFMV9WQAUUpuI.jpg:large",
    }

    if year != "Select":
        st.markdown(
            f"<div style='text-align:center;'><span style='background-color:#1ABC9C; color:white; padding:6px 14px; border-radius:8px; font-size:16px;'>Selected Year: {year}</span></div>",
            unsafe_allow_html=True
        )

        img_path = image_links.get(year)
        if img_path:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; margin-top: 20px;">
                    <img src="{img_path}" alt="Weather Heatmap - {year}" 
                        style="border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); max-width: 95%;">
                </div>
                """,
                unsafe_allow_html=True
            )






























