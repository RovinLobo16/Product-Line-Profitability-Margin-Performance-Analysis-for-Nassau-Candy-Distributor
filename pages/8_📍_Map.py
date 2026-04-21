import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("🌍 Advanced Geo Analytics")
st.caption("Analyze factory-level performance and geographic contribution")

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("❌ Data not loaded.")
    st.stop()

df.columns = df.columns.str.strip()

# =========================
# SIDEBAR FILTERS (NEW 🔥)
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    div = st.sidebar.multiselect(
        "Division", df["Division"].unique(),
        default=df["Division"].unique()
    )
    df = df[df["Division"].isin(div)]

if "Region" in df.columns:
    reg = st.sidebar.multiselect(
        "Region", df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(reg)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# PRODUCT → FACTORY MAP
# =========================
product_factory = {
    "Wonka Bar – Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar – Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar – Scrumdidilyumptious": "Lot's O' Nuts",
    "Wonka Bar – Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar – Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

df["Factory"] = df["Product Name"].map(product_factory)

# =========================
# COORDINATES
# =========================
coords = {
    "Lot's O' Nuts": (32.88, -111.76),
    "Wicked Choccy's": (32.07, -81.08),
    "Sugar Shack": (48.11, -96.18),
    "Secret Factory": (41.44, -90.56),
    "The Other Factory": (35.11, -89.97)
}

df["Latitude"] = df["Factory"].map(lambda x: coords.get(x, (None, None))[0])
df["Longitude"] = df["Factory"].map(lambda x: coords.get(x, (None, None))[1])

# =========================
# CLEAN
# =========================
df = df.dropna(subset=["Latitude", "Longitude"])

if df.empty:
    st.error("❌ No geographic data available.")
    st.stop()

# =========================
# SIDEBAR CONTROLS
# =========================
metric = st.sidebar.selectbox("Metric", ["Sales", "Gross Profit"])
view = st.sidebar.radio("View", ["Bubble Map", "Heatmap"])

# =========================
# AGGREGATE
# =========================
geo = df.groupby(["Factory", "Latitude", "Longitude"]).agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

# Contribution %
total_profit = geo["Gross Profit"].sum()
geo["Profit Contribution %"] = (geo["Gross Profit"] / total_profit) * 100

# =========================
# KPI SUMMARY (NEW 🔥)
# =========================
st.subheader("📊 Geo KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Factories", len(geo))
col2.metric("Total Sales", f"${geo['Sales'].sum():,.0f}")
col3.metric("Total Profit", f"${geo['Gross Profit'].sum():,.0f}")

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
        hover_data=["Sales", "Gross Profit", "Profit Contribution %"],
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

fig.update_layout(
    mapbox_style="carto-darkmatter",
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# FACTORY PERFORMANCE TABLE (NEW 🔥)
# =========================
st.subheader("🏭 Factory Performance")

st.dataframe(
    geo.sort_values(by="Gross Profit", ascending=False),
    use_container_width=True
)

# =========================
# INSIGHTS (UPGRADED)
# =========================
st.subheader("🧠 Geo Insights")

top = geo.loc[geo["Gross Profit"].idxmax()]
low = geo.loc[geo["Gross Profit"].idxmin()]

st.markdown(f"""
- **Top performing factory:** {top['Factory']} (${top['Gross Profit']:,.0f})  
- **Lowest performing factory:** {low['Factory']}  
- **Highest contribution:** {top['Profit Contribution %']:.2f}% of total profit  

📌 **Recommendation:**  
- Scale production from top-performing factories  
- Investigate inefficiencies in low-performing locations  
- Optimize supply chain distribution  
""")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Geo Data",
    geo.to_csv(index=False),
    file_name="geo_analysis.csv",
    mime="text/csv"
)
