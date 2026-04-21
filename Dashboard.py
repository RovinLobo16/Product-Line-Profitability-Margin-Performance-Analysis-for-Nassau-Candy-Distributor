import streamlit as st
import pandas as pd
import plotly.express as px
import os

from components.filters import apply_filters

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau AI Dashboard",
    layout="wide",
    page_icon="🍬"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df.columns = df.columns.str.strip()

    for col in ["Sales", "Units", "Gross Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Sales", "Units", "Gross Profit"])
    df = df[(df["Sales"] > 0) & (df["Units"] > 0)]

    df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    return df

df = load_data()

if df.empty:
    st.stop()

# =========================
# APPLY GLOBAL FILTERS
# =========================
df = apply_filters(df)

# =========================
# LOGO
# =========================
LOGO_PATH = "assets/unified_mentor_logo.png"

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:18px;
}
.insight-box {
    background-color:#1c1f26;
    padding:15px;
    border-left:5px solid #00c8ff;
    border-radius:10px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1.5, 6])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)

with col2:
    st.markdown("""
        <h1>🍬 Nassau Candy Intelligence Platform</h1>
        <p style='color:gray;'>AI-powered profitability analytics</p>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# KPIs
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()
total_units = df["Units"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f'<div class="metric-card">💰 Revenue<br>${total_sales:,.0f}</div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card">📈 Gross Profit<br>${total_profit:,.0f}</div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card">📊 Margin<br>{avg_margin:.2f}%</div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card">📦 Units<br>{total_units:,.0f}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# TOP PRODUCTS
# =========================
st.subheader("📊 Top Profit Drivers")

top_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    color="Gross Profit"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.subheader("🤖 Executive Insights")

top_product = top_products.iloc[0]["Product Name"]

low_margin = len(df[df["Gross Margin %"] < 20])
volume_trap = len(df[
    (df["Sales"] > df["Sales"].quantile(0.75)) &
    (df["Gross Margin %"] < 25)
])

st.markdown(f"""
<div class="insight-box">
Revenue: ${total_sales:,.0f}<br>
Profit: ${total_profit:,.0f}<br>
Top product: {top_product}<br>
Low margin products: {low_margin}<br>
Volume traps: {volume_trap}
</div>
""", unsafe_allow_html=True)
