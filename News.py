# def news():
#     import streamlit as st
#     import urllib.parse
#     import feedparser
#     import requests
#     import datetime as dt
#     import matplotlib.pyplot as plt
#     import folium
#     from streamlit_folium import st_folium


#     WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
#     GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"


#     def fetch_news(area_name, category):
#         if category.lower() in ["sports", "politics", "technology"]:
#             category = "general"
#         if category.lower() == "weather":
#             query = f"{area_name} weather"
#         else:
#             query = f"{category} {area_name}"

#         base_url = "https://news.google.com/rss/search"
#         params = {"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
#         url = f"{base_url}?{urllib.parse.urlencode(params)}"
#         feed = feedparser.parse(url)

#         if not feed.entries:
#             params = {"q": "general", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
#             url = f"{base_url}?{urllib.parse.urlencode(params)}"
#             feed = feedparser.parse(url)

#         return feed.entries


#     def fetch_weather(area_name):
#         api_key = WEATHER_API_KEY

#         def get_geo_data(query):
#             geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={query},IN&limit=1&appid={api_key}"
#             resp = requests.get(geo_url, timeout=5)
#             if resp.status_code != 200:
#                 return None
#             data = resp.json()
#             return data if data else None

#         geo_data = get_geo_data(area_name)
#         if not geo_data:
#             parts = area_name.split()
#             if len(parts) > 1:
#                 geo_data = get_geo_data(parts[-1])
#         if not geo_data:
#             geo_data = get_geo_data("Mumbai")

        
#         if not geo_data:
#             return None, None, 19.0760, 72.8777, None, None

#         lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

#         current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
#         current_weather = requests.get(current_url, timeout=5).json()

#         forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
#         forecast_data = requests.get(forecast_url, timeout=5).json()

#         forecast_list = []
#         dates_added = set()
#         for item in forecast_data.get("list", []):
#             date_txt = item["dt_txt"].split()[0]
#             if date_txt not in dates_added:
#                 forecast_list.append({
#                     "date": date_txt,
#                     "temp": item["main"]["temp"],
#                     "desc": item["weather"][0]["description"],
#                     "icon": item["weather"][0]["icon"]
#                 })
#                 dates_added.add(date_txt)
#             if len(forecast_list) >= 3:
#                 break

#         hourly_temps = []
#         hourly_times = []
#         for item in forecast_data.get("list", [])[:8]:
#             time_txt = item["dt_txt"].split()[1][:5]
#             hourly_times.append(time_txt)
#             hourly_temps.append(item["main"]["temp"])

#         return current_weather, forecast_list, lat, lon, hourly_times, hourly_temps


#     def format_date(date_str):
#         try:
#             return dt.datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %b %d")
#         except:
#             return date_str


#     st.set_page_config(page_title="Local Safety News & Weather", layout="wide")
#     st.markdown("<h2 style='color:white; background:#0B2447; padding:10px; border-radius:10px;'>🔍 Local Safety News & Weather Dashboard</h2>", unsafe_allow_html=True)


#     st.markdown("### 🔍 Search Parameters")
#     with st.container():
#         col_a, col_b = st.columns([2, 1])
#         with col_a:
#             area_name = st.text_input("Enter Area / City / Pincode:", "Mumbai")
#         with col_b:
#             category_options = ["crime", "weather", "general", "traffic"]
#             category = st.selectbox("Select Category:", category_options)

#     if not area_name.strip():
#         st.warning("Please enter a valid area name.")
#         st.stop()

#     with st.spinner("Fetching weather data..."):
#         current_weather, forecast, lat, lon, hourly_times, hourly_temps = fetch_weather(area_name)

#     with st.spinner("Fetching news articles..."):
#         news_cat = category if category in ["crime", "weather"] else "general"
#         news_entries = fetch_news(area_name, news_cat)


#     if category == "traffic":
#         if not lat or not lon:
#             lat, lon = 19.0760, 72.8777  # fallback Mumbai

#         st.markdown(f"## 🚦 Traffic Status in {area_name}")

#         m = folium.Map(location=[lat, lon], zoom_start=14)
#         folium.TileLayer(
#             tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
#             attr="OpenStreetMap"
#         ).add_to(m)

        
#         folium.TileLayer(
#             tiles="https://mt1.google.com/vt/lyrs=m,traffic&x={x}&y={y}&z={z}",
#             attr="Google",
#             name="Traffic",
#             overlay=True,
#             control=True
#         ).add_to(m)

#         folium.LayerControl().add_to(m)
#         st_folium(m, width=700, height=500)


#     if category == "weather" and current_weather:
#         st.markdown(f"### Weather in {area_name}")
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             icon_code = current_weather['weather'][0]['icon']
#             st.image(f"http://openweathermap.org/img/wn/{icon_code}@4x.png", width=120)
#         with col2:
#             temp = current_weather['main']['temp']
#             desc = current_weather['weather'][0]['description'].title()
#             humidity = current_weather['main']['humidity']
#             wind_speed = current_weather['wind']['speed']
#             feels_like = current_weather['main']['feels_like']
#             st.markdown(f"### {temp}°C, {desc}")
#             st.markdown(f"- Feels like: {feels_like}°C")
#             st.markdown(f"- Humidity: {humidity}%")
#             st.markdown(f"- Wind speed: {wind_speed} m/s")

        
#         st.markdown("### 📊 Weather Overview")
#         weather_metrics = {
#             "Temperature (°C)": temp,
#             "Humidity (%)": humidity,
#             "Wind Speed (m/s)": wind_speed
#         }
#         fig_bar, ax_bar = plt.subplots(figsize=(5, 3))
#         ax_bar.bar(weather_metrics.keys(), weather_metrics.values(), color=['orange', 'blue', 'green'])
#         ax_bar.set_ylabel("Value")
#         ax_bar.set_ylim(0, max(weather_metrics.values()) + 10)
#         for i, v in enumerate(weather_metrics.values()):
#             ax_bar.text(i, v + 1, str(v), ha='center', fontweight='bold')
#         st.pyplot(fig_bar)
#         plt.close(fig_bar)

        
#         st.markdown("### Hourly Temperature (Next 24 hours)")
#         fig_hr, ax_hr = plt.subplots(figsize=(9, 3))
#         ax_hr.plot(hourly_times, hourly_temps, marker='o', color='orange')
#         ax_hr.set_title("Temperature (°C)")
#         ax_hr.set_xlabel("Time")
#         ax_hr.set_ylabel("Temperature")
#         ax_hr.grid(True, linestyle='--', alpha=0.6)
#         st.pyplot(fig_hr)
#         plt.close(fig_hr)

        
#         st.markdown("###  Next 3 Days Forecast")
#         dates = [format_date(day['date']) for day in forecast]
#         temps = [day['temp'] for day in forecast]
#         fig, ax = plt.subplots(figsize=(7, 3))
#         ax.plot(dates, temps, marker='o', linestyle='-', color='orange')
#         ax.set_title('Temperature Forecast (°C)', fontsize=14)
#         ax.set_ylabel('Temperature (°C)', fontsize=12)
#         ax.grid(True, linestyle='--', alpha=0.6)
#         st.pyplot(fig)
#         plt.close(fig)

#         fc_cols = st.columns(3)
#         for i, day in enumerate(forecast):
#             with fc_cols[i]:
#                 st.image(f"http://openweathermap.org/img/wn/{day['icon']}@2x.png", width=80)
#                 st.markdown(f"**{dates[i]}**")
#                 st.markdown(f"{day['temp']}°C")
#                 st.markdown(day['desc'].title())


#     st.markdown(f"## 📰 News in {area_name}")
#     if news_entries:
#         for i in range(0, min(len(news_entries), 10), 2):
#             cols = st.columns(2)
#             for j in range(2):
#                 idx = i + j
#                 if idx >= len(news_entries):
#                     break
#                 entry = news_entries[idx]
#                 title = entry.title
#                 link = entry.link
#                 published = entry.published if "published" in entry else "N/A"
#                 published_date = dt.datetime(*entry.published_parsed[:6]).strftime("%b %d, %Y %H:%M") if hasattr(entry, "published_parsed") else published
#                 image_url = None
#                 if "media_content" in entry and entry.media_content:
#                     image_url = entry.media_content[0]["url"]
#                 with cols[j]:
#                     st.markdown(f"### [{title}]({link})")
#                     if image_url:
#                         st.image(image_url, use_column_width=True)
#                     st.markdown(f"Published: {published_date}")
#                     st.markdown("---")
#     else:
#         st.info("No news articles found for this selection.")

def news(lang_code):
    import streamlit as st
    import urllib.parse
    import feedparser
    import requests
    import datetime as dt
    import matplotlib.pyplot as plt
    import folium
    from streamlit_folium import st_folium

    WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
    GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

    def translate_text(text):
        from deep_translator import GoogleTranslator
        try:
            return GoogleTranslator(source='auto', target=lang_code).translate(text)
        except:
            return text

    def fetch_news(area_name, category):
        if category.lower() in ["sports", "politics", "technology"]:
            category = "general"
        query = f"{category} {area_name}" if category.lower() != "weather" else f"{area_name} weather"

        base_url = "https://news.google.com/rss/search"
        params = {"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        feed = feedparser.parse(url)

        if not feed.entries:
            params = {"q": "general", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            feed = feedparser.parse(url)

        return feed.entries

    def fetch_weather(area_name):
        api_key = WEATHER_API_KEY

        def get_geo_data(query):
            geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={query},IN&limit=1&appid={api_key}"
            resp = requests.get(geo_url, timeout=5)
            if resp.status_code != 200:
                return None
            data = resp.json()
            return data if data else None

        geo_data = get_geo_data(area_name)
        if not geo_data:
            parts = area_name.split()
            if len(parts) > 1:
                geo_data = get_geo_data(parts[-1])
        if not geo_data:
            geo_data = get_geo_data("Mumbai")

        if not geo_data:
            return None, None, 19.0760, 72.8777, None, None

        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        current_weather = requests.get(current_url, timeout=5).json()

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        forecast_data = requests.get(forecast_url, timeout=5).json()

        forecast_list = []
        dates_added = set()
        for item in forecast_data.get("list", []):
            date_txt = item["dt_txt"].split()[0]
            if date_txt not in dates_added:
                forecast_list.append({
                    "date": date_txt,
                    "temp": item["main"]["temp"],
                    "desc": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                })
                dates_added.add(date_txt)
            if len(forecast_list) >= 3:
                break

        hourly_temps = []
        hourly_times = []
        for item in forecast_data.get("list", [])[:8]:
            time_txt = item["dt_txt"].split()[1][:5]
            hourly_times.append(time_txt)
            hourly_temps.append(item["main"]["temp"])

        return current_weather, forecast_list, lat, lon, hourly_times, hourly_temps

    def format_date(date_str):
        try:
            return dt.datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %b %d")
        except:
            return date_str

    st.set_page_config(page_title=translate_text("Local Safety News & Weather"), layout="wide")
    st.markdown(f"<h2 style='color:white; background:#0B2447; padding:10px; border-radius:10px;'> {translate_text('Local Safety News & Weather Dashboard')}</h2>", unsafe_allow_html=True)

    st.markdown(f"###  {translate_text('Search Parameters')}")
    with st.container():
        col_a, col_b = st.columns([2, 1])
        with col_a:
            area_name = st.text_input(translate_text("Enter Area / City / Pincode:"), "Mumbai")
        with col_b:
            category_options = ["crime", "weather", "general", "traffic"]
            category = st.selectbox(translate_text("Select Category:"), category_options)

    if not area_name.strip():
        st.warning(translate_text("Please enter a valid area name."))
        st.stop()

    with st.spinner(translate_text("Fetching weather data...")):
        current_weather, forecast, lat, lon, hourly_times, hourly_temps = fetch_weather(area_name)

    with st.spinner(translate_text("Fetching news articles...")):
        news_cat = category if category in ["crime", "weather"] else "general"
        news_entries = fetch_news(area_name, news_cat)

    if category == "traffic":
        if not lat or not lon:
            lat, lon = 19.0760, 72.8777

        st.markdown(f"## 🚦 {translate_text('Traffic Status in')} {area_name}")

        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(
            tiles="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="OpenStreetMap"
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m,traffic&x={x}&y={y}&z={z}",
            attr="Google",
            name="Traffic",
            overlay=True,
            control=True
        ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width=700, height=500)

    if category == "weather" and current_weather:
        st.markdown(f"### {translate_text('Weather in')} {area_name}")
        col1, col2 = st.columns([1, 3])
        with col1:
            icon_code = current_weather['weather'][0]['icon']
            st.image(f"http://openweathermap.org/img/wn/{icon_code}@4x.png", width=120)
        with col2:
            temp = current_weather['main']['temp']
            desc = current_weather['weather'][0]['description'].title()
            humidity = current_weather['main']['humidity']
            wind_speed = current_weather['wind']['speed']
            feels_like = current_weather['main']['feels_like']
            st.markdown(f"### {temp}°C, {translate_text(desc)}")
            st.markdown(f"- {translate_text('Feels like')}: {feels_like}°C")
            st.markdown(f"- {translate_text('Humidity')}: {humidity}%")
            st.markdown(f"- {translate_text('Wind speed')}: {wind_speed} m/s")

        st.markdown(f"### 📊 {translate_text('Weather Overview')}")
        weather_metrics = {
            translate_text("Temperature (°C)"): temp,
            translate_text("Humidity (%)"): humidity,
            translate_text("Wind Speed (m/s)"): wind_speed
        }
        fig_bar, ax_bar = plt.subplots(figsize=(5, 3))
        ax_bar.bar(weather_metrics.keys(), weather_metrics.values(), color=['orange', 'blue', 'green'])
        ax_bar.set_ylabel(translate_text("Value"))
        ax_bar.set_ylim(0, max(weather_metrics.values()) + 10)
        for i, v in enumerate(weather_metrics.values()):
            ax_bar.text(i, v + 1, str(v), ha='center', fontweight='bold')
        st.pyplot(fig_bar)
        plt.close(fig_bar)

        st.markdown(f"### {translate_text('Hourly Temperature (Next 24 hours)')}")
        fig_hr, ax_hr = plt.subplots(figsize=(9, 3))
        ax_hr.plot(hourly_times, hourly_temps, marker='o', color='orange')
        ax_hr.set_title(translate_text("Temperature (°C)"))
        ax_hr.set_xlabel(translate_text("Time"))
        ax_hr.set_ylabel(translate_text("Temperature"))
        ax_hr.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig_hr)
        plt.close(fig_hr)

        st.markdown(f"### {translate_text('Next 3 Days Forecast')}")
        dates = [format_date(day['date']) for day in forecast]
        temps = [day['temp'] for day in forecast]
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(dates, temps, marker='o', linestyle='-', color='orange')
        ax.set_title(translate_text('Temperature Forecast (°C)'), fontsize=14)
        ax.set_ylabel(translate_text('Temperature (°C)'), fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
        plt.close(fig)

        fc_cols = st.columns(3)
        for i, day in enumerate(forecast):
            with fc_cols[i]:
                st.image(f"http://openweathermap.org/img/wn/{day['icon']}@2x.png", width=80)
                st.markdown(f"**{dates[i]}**")
                st.markdown(f"{day['temp']}°C")
                st.markdown(translate_text(day['desc'].title()))

    st.markdown(f"## 📰 {translate_text('News in')} {area_name}")
    if news_entries:
        for i in range(0, min(len(news_entries), 10), 2):
            cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx >= len(news_entries):
                    break
                entry = news_entries[idx]
                title = translate_text(entry.title)
                link = entry.link
                published = entry.published if "published" in entry else "N/A"
                published_date = dt.datetime(*entry.published_parsed[:6]).strftime("%b %d, %Y %H:%M") if hasattr(entry, "published_parsed") else published
                image_url = None
                if "media_content" in entry and entry.media_content:
                    image_url = entry.media_content[0]["url"]
                with cols[j]:
                    st.markdown(f"### [{title}]({link})")
                    if image_url:
                        st.image(image_url, use_column_width=True)
                    st.markdown(f"{translate_text('Published')}: {published_date}")
                    st.markdown("---")
    else:
        st.info(translate_text("No news articles found for this selection."))
