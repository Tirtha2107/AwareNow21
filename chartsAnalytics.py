






def charts():
    import pandas as pd
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px

    from datetime import datetime, timedelta
    from folium.plugins import HeatMap, MarkerCluster
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    from sklearn.linear_model import LinearRegression
    from streamlit_option_menu import option_menu
    from streamlit_folium import folium_static, st_folium
    from home import show_Home
    import openrouteservice
    from openrouteservice import convert
    st.header(("Charts And Analytics"))

    with st.expander("Choose Section", expanded=True):
        section = st.radio("Select Section", [
            "Crime: City-wise Breakdown",
            "Crime: Top 10 Cities by Type",
            "Crime: Type Prediction (2025)",
            "Crime: Type Pie Charts",
            "Disaster: Deaths by Type",
            "Disaster: Type Pie Charts",
            "Disaster: 2025 Death Prediction"
        ])

    st.markdown("---")

    # Load datasets
    crime_df = pd.read_csv("crime_dataset_india (3).csv")
    crime_df.columns = crime_df.columns.str.strip()
    crime_df['Date of Occurrence'] = pd.to_datetime(crime_df['Date of Occurrence'], errors='coerce')
    crime_df['Year'] = crime_df['Date of Occurrence'].dt.year
    crime_df = crime_df.dropna(subset=['City', 'Crime Description', 'Year'])

    disaster_df = pd.read_csv("disasterIND .csv")
    disaster_df.columns = disaster_df.columns.str.strip()
    disaster_df = disaster_df.dropna(subset=["Location", "Disaster Type", "Start Year", "Total Deaths"])
    disaster_df["Start Year"] = disaster_df["Start Year"].astype(int)
    disaster_df = disaster_df[disaster_df["Start Year"].between(2020, 2024)]

    # Section 1
    if section == "Crime: City-wise Breakdown":
        st.header("Crime Breakdown by City and Year")
        cities = sorted(crime_df['City'].unique())
        years = sorted(crime_df['Year'].unique())
        selected_city = st.selectbox("Choose a City", cities)
        selected_year = st.selectbox("Choose a Year", years)

        filtered = crime_df[
            (crime_df['City'].str.lower() == selected_city.lower()) &
            (crime_df['Year'] == selected_year)
        ]

        if filtered.empty:
            st.warning("No crime data available for this city and year.")
        else:
            grouped = filtered.groupby('Crime Description').size().reset_index(name='Count')
            grouped = grouped.sort_values(by='Count', ascending=False)
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=grouped, x='Crime Description', y='Count', palette="Set2", ax=ax)
            ax.set_title(f"Crime Breakdown in {selected_city} - {selected_year}", fontsize=16)
            ax.set_xlabel("Crime Type")
            ax.set_ylabel("Number of Crimes")
            plt.xticks(rotation=35, ha='right')
            for bar in ax.patches:
                ax.annotate(f'{int(bar.get_height())}', (bar.get_x() + bar.get_width() / 2, bar.get_height() + 1),
                            ha='center', fontsize=9, color='black')
            st.pyplot(fig)

    # Section 2
    elif section == "Crime: Top 10 Cities by Type":
        st.header("Top 10 Cities for a Selected Crime Type and Year")
        crime_types = sorted(crime_df['Crime Description'].unique())
        years = sorted(crime_df['Year'].unique())
        selected_crime = st.selectbox("Select Crime Type", crime_types)
        selected_year = st.selectbox("Select Year", years)

        filtered_df = crime_df[(crime_df['Crime Description'] == selected_crime) & (crime_df['Year'] == selected_year)]
        top_cities = (
            filtered_df.groupby('City')
            .size()
            .reset_index(name='Count')
            .sort_values(by='Count', ascending=False)
            .head(10)
        )

        if top_cities.empty:
            st.warning(f"No data found for '{selected_crime}' in {selected_year}.")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=top_cities, x='City', y='Count', palette='magma', ax=ax)
            y_max = top_cities['Count'].max()
            ax.set_ylim(0, y_max + 10)
            for i, v in enumerate(top_cities['Count']):
                ax.text(i, v + 1, str(v), color='black', ha='center', fontsize=9)
            ax.set_title(f"Top 10 Cities for '{selected_crime}' - {selected_year}")
            ax.set_ylabel("Number of Cases")
            ax.set_xlabel("City")
            plt.tight_layout()
            st.pyplot(fig)

    # Section 3
    elif section == "Crime: Type Prediction (2025)":
        st.header("Predict Crimes in 2025 by Crime Type")
        synthetic_df = pd.read_csv("synthetic_crime_data_2025.csv")
        combined_df = pd.concat([crime_df, synthetic_df], ignore_index=True)
        crime_types = sorted(combined_df['Crime Description'].unique())
        selected_crime = st.selectbox("Select a Crime Type to Predict:", crime_types)

        filtered_df = combined_df[combined_df['Crime Description'] == selected_crime]
        crime_trend = filtered_df.groupby('Year').size().reset_index(name='Count').sort_values('Year')

        X = crime_trend[crime_trend['Year'] < 2025][['Year']]
        y = crime_trend[crime_trend['Year'] < 2025]['Count']
        model = LinearRegression().fit(X, y)
        predicted_2025 = int(model.predict([[2025]])[0])

        if 2025 not in crime_trend['Year'].values:
            crime_trend = pd.concat([crime_trend, pd.DataFrame({"Year": [2025], "Count": [predicted_2025]})])

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=crime_trend, x='Year', y='Count', marker='o', ax=ax, label='Crime Count')
        ax.axvline(2025, color='red', linestyle='--', label='Predicted 2025')
        ax.text(2025, predicted_2025, f"{predicted_2025}", color='red', fontsize=12, ha='center', va='bottom')
        ax.set_title(f"Yearly Trend of '{selected_crime}' (2020–2025)", fontsize=16, fontweight='bold')
        ax.set_ylabel("Number of Cases")
        ax.set_xlabel("Year")
        ax.legend()
        st.pyplot(fig)

        st.subheader("Crime Counts by Year")
        st.dataframe(crime_trend.sort_values("Year").reset_index(drop=True))

    # Section 4
    elif section == "Crime: Type Pie Charts":
        st.header("Crime Type Distribution by Year")
        all_years = sorted(crime_df['Year'].dropna().unique())
        cols = st.columns(3)
        for idx, year in enumerate(all_years):
            year_df = crime_df[crime_df['Year'] == year]
            crime_counts = year_df['Crime Description'].value_counts()
            if crime_counts.empty:
                continue
            with cols[idx % 3]:
                st.markdown(f"### {year}")
                fig, ax = plt.subplots(figsize=(4, 4))
                colors = sns.color_palette('pastel')[0:len(crime_counts)]
                ax.pie(
                    crime_counts,
                    labels=crime_counts.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 6}
                )
                ax.axis('equal')
                st.pyplot(fig)

    # Section 5
    elif section == "Disaster: Deaths by Type":
        st.header("Disaster Impact (2020–2024)")
        col1, col2 = st.columns(2)
        disaster_types = sorted(disaster_df["Disaster Type"].unique())
        selected_disaster = col1.selectbox("Select Disaster Type", disaster_types)
        year_options = sorted(disaster_df["Start Year"].unique())
        selected_year = col2.selectbox("Select Year", year_options)

        filtered = disaster_df[
            (disaster_df["Disaster Type"] == selected_disaster) &
            (disaster_df["Start Year"] == selected_year)
        ]

        if filtered.empty:
            st.warning("No data available for the selected disaster and year.")
        else:
            deaths_by_location = (
                filtered.groupby("Location")["Total Deaths"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )
            fig, ax = plt.subplots(figsize=(10, 5))
            deaths_by_location.plot(kind="bar", ax=ax, color="crimson")
            ax.set_title(f"Total Deaths by Location - {selected_disaster} ({selected_year})")
            ax.set_xlabel("Location")
            ax.set_ylabel("Total Deaths")
            ax.set_xticklabels(deaths_by_location.index.str.slice(0, 25) + '...', rotation=30, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

    # Section 6
    elif section == "Disaster: Type Pie Charts":
        st.header("Disaster Type Distribution by Year (2020–2024)")
        years = sorted(disaster_df["Start Year"].unique())
        selected_year = st.selectbox("Select Year", years)

        filtered_df = disaster_df[disaster_df["Start Year"] == selected_year]
        deaths_by_disaster = (
            filtered_df.groupby("Disaster Type")["Total Deaths"]
            .sum()
            .sort_values(ascending=False)
        )

        if not deaths_by_disaster.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(
                deaths_by_disaster,
                labels=deaths_by_disaster.index,
                autopct='%1.1f%%',
                startangle=140,
                textprops={'fontsize': 9}
            )
            ax.axis('equal')
            ax.set_title(f"Disaster Type Distribution in {selected_year} (by % of Deaths)")
            st.pyplot(fig)
        else:
            st.warning(f"No disaster data available for {selected_year}.")

    # Section 7
    elif section == "Disaster: 2025 Death Prediction":
        st.header("Predict Disaster Deaths in 2025")
        disaster_types = sorted(disaster_df["Disaster Type"].unique())
        selected_disaster = st.selectbox("Select Disaster Type to Predict", disaster_types)

        filtered = disaster_df[disaster_df["Disaster Type"] == selected_disaster]
        yearly = (
            filtered.groupby("Start Year")["Total Deaths"]
            .sum()
            .reset_index()
            .rename(columns={"Start Year": "Year"})
            .sort_values("Year")
        )

        X = yearly[["Year"]]
        y = yearly["Total Deaths"]
        model = LinearRegression().fit(X, y)
        pred_2025 = int(model.predict([[2025]])[0])
        yearly_pred = pd.concat(
            [yearly, pd.DataFrame({"Year": [2025], "Total Deaths": [pred_2025]})],
            ignore_index=True
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=yearly_pred, x="Year", y="Total Deaths", marker="o", ax=ax, label="Total Deaths")
        ax.axvline(2025, color='red', linestyle='--', label="Predicted 2025")
        ax.text(2025, pred_2025, str(pred_2025), color="red", fontsize=10, ha="center", va="bottom")
        ax.set_title(f"Predicted Deaths due to {selected_disaster} (2020–2025)")
        ax.set_ylabel("Total Deaths")
        ax.set_xlabel("Year")
        ax.set_xticks(yearly_pred["Year"])
        ax.set_xticklabels(yearly_pred["Year"].astype(int))
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Year-wise Total Deaths")
        st.dataframe(yearly_pred.sort_values("Year").reset_index(drop=True))


