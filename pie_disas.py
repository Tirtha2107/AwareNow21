

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit setup
st.set_page_config(page_title="Disaster Share by Year", layout="wide")
st.title("📊 Disaster Type Distribution by Year (Based on Deaths)")

# Load data
df = pd.read_csv("disasterIND .csv")

# Clean data
df = df.dropna(subset=["Disaster Type", "Start Year", "Total Deaths"])
df["Start Year"] = df["Start Year"].astype(int)
df = df[df["Start Year"].between(2020, 2024)]

# Year selector
years = sorted(df["Start Year"].unique())
selected_year = st.selectbox("Select Year", years)

# Filter by selected year
filtered_df = df[df["Start Year"] == selected_year]

# Group by disaster type
deaths_by_disaster = (
    filtered_df.groupby("Disaster Type")["Total Deaths"]
    .sum()
    .sort_values(ascending=False)
)

# Show chart title
st.subheader(f"Disaster Type Distribution in {selected_year} (by % of Deaths)")

if not deaths_by_disaster.empty:
    # Plot pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(
        deaths_by_disaster,
        labels=deaths_by_disaster.index,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 9}
    )
    ax.axis('equal')  # Equal aspect ratio for a perfect circle
    st.pyplot(fig)
else:
    st.warning(f"No disaster data available for {selected_year}.")
