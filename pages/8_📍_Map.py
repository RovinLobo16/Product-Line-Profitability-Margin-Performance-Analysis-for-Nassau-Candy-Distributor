import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("🌍 Advanced Geo Analytics")

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# FACTORY COORDINATES
# =========================
factory_coords = pd.DataFrame({
    "Factory": ["Lot's O' Nuts", "Wicked Choccy's", "Sugar Shack",
                "Secret Factory", "The Other Factory"],
    "Latitude": [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
    "Longitude": [-111.768036, -81.088371, -96.18115, -90.565487, -89.97107]
})

# =========================
# MERGE DATA
# =========================
if "Factory" in df.columns:
    df = df.merge(factory_coords, on="Factory", how="left")

df = df.dropna(subset=["Latitude", "Longitude"])

if df.empty:
    st.error("No geographic data available.")
    st.stop()

# =========================
# SIDEBAR CONTROLS
# =========================
st.sidebar.header("🌐 Map Controls")

metric = st.sidebar.selectbox(
    "Metric",
    ["Sales", "Gross Profit"]
)

view = st.sidebar.radio(
    "View Type",
    ["Bubble Map", "Heatmap"]
)

# =========================
# AGGREGATE
# =========================
geo = df.groupby(["Factory", "Latitude", "Longitude"]).agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

# =========================
# KPI SUMMARY
# =========================
st.subheader("📊 Geo KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Locations", len(geo))
col2.metric("Total Sales", f"${geo['Sales'].sum():,.0f}")
col3.metric("Total Profit", f"${geo['Gross Profit'].sum():,.0f}")

# =========================
# BUBBLE MAP
# =========================
if view == "Bubble Map":

    fig = px.scatter_mapbox(
        geo,
        lat="Latitude",
        lon="Longitude",
        size=metric,
        color="Factory",
        hover_name="Factory",
        hover_data=["Sales", "Gross Profit"],
        zoom=3,
        height=550
    )

    fig.update_layout(mapbox_style="carto-darkmatter")

# =========================
# HEATMAP
# =========================
else:

    fig = px.density_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        z=metric,
        radius=25,
        zoom=3,
        height=550
    )

    fig.update_layout(mapbox_style="carto-darkmatter")

st.plotly_chart(fig, use_container_width=True)

# =========================
# FACTORY PERFORMANCE
# =========================
st.subheader("🏭 Factory Performance")

fig2 = px.bar(
    geo.sort_values(by="Gross Profit", ascending=False),
    x="Factory",
    y=["Sales", "Gross Profit"],
    barmode="group",
    title="Revenue vs Profit by Factory"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# AI GEO INSIGHTS
# =========================
st.subheader("🧠 Geo Insights")

top_factory = geo.loc[geo["Gross Profit"].idxmax()]
low_factory = geo.loc[geo["Gross Profit"].idxmin()]

colA, colB = st.columns(2)

colA.success(
    f"Top factory: {top_factory['Factory']} "
    f"(${top_factory['Gross Profit']:,.0f} profit)"
)

colB.warning(
    f"Lowest performing factory: {low_factory['Factory']}"
)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Geo Data",
    geo.to_csv(index=False),
    file_name="geo_analysis.csv",
    mime="text/csv"
)
