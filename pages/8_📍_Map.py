import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("🌍 Advanced Geo Analytics")

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("❌ Data not loaded.")
    st.stop()

df.columns = df.columns.str.strip()

# =========================
# PRODUCT → FACTORY MAPPING
# =========================
product_factory = pd.DataFrame({
    "Product Name": [
        "Wonka Bar – Nutty Crunch Surprise",
        "Wonka Bar – Fudge Mallows",
        "Wonka Bar – Scrumdidilyumptious",
        "Wonka Bar – Milk Chocolate",
        "Wonka Bar – Triple Dazzle Caramel",
        "Laffy Taffy", "SweeTARTS", "Nerds", "Fun Dip",
        "Everlasting Gobstopper", "Hair Toffee",
        "Fizzy Lifting Drinks", "Lickable Wallpaper",
        "Wonka Gum", "Kazookles"
    ],
    "Factory": [
        "Lot's O' Nuts", "Lot's O' Nuts", "Lot's O' Nuts",
        "Wicked Choccy's", "Wicked Choccy's",
        "Sugar Shack", "Sugar Shack", "Sugar Shack", "Sugar Shack",
        "Secret Factory", "The Other Factory",
        "Sugar Shack", "Secret Factory",
        "Secret Factory", "The Other Factory"
    ]
})

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
# VALIDATE PRODUCT COLUMN
# =========================
if "Product Name" not in df.columns:
    st.error("❌ 'Product Name' column missing.")
    st.stop()

# =========================
# MERGE PRODUCT → FACTORY
# =========================
df = df.merge(product_factory, on="Product Name", how="left")

# =========================
# MERGE FACTORY → GEO
# =========================
df = df.merge(factory_coords, on="Factory", how="left")

# =========================
# CLEAN GEO DATA
# =========================
df = df.dropna(subset=["Latitude", "Longitude"])

if df.empty:
    st.error("❌ No geographic data available after mapping.")
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Controls")

metric = st.sidebar.selectbox(
    "Metric", ["Sales", "Gross Profit"]
)

view = st.sidebar.radio(
    "View", ["Bubble Map", "Heatmap"]
)

# =========================
# AGGREGATE
# =========================
geo = df.groupby(["Factory", "Latitude", "Longitude"]).agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

# =========================
# MAP
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
# INSIGHTS
# =========================
st.subheader("🧠 Geo Insights")

top = geo.loc[geo["Gross Profit"].idxmax()]
low = geo.loc[geo["Gross Profit"].idxmin()]

col1, col2 = st.columns(2)

col1.success(f"Top factory: {top['Factory']} (${top['Gross Profit']:,.0f})")
col2.warning(f"Lowest factory: {low['Factory']}")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Geo Data",
    geo.to_csv(index=False),
    file_name="geo_analysis.csv",
    mime="text/csv"
)
