import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG (WITH LOGO ICON)
# =========================
st.set_page_config(
    page_title="Nassau AI Dashboard",
    layout="wide",
    page_icon="logo of uni.avif"   # 🔥 rename your image to logo.png
)

# =========================
# LOAD DATA (SAFE)
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

    return df

df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

# =========================
# SIDEBAR LOGO (GLOBAL BRANDING)
# =========================
st.sidebar.image("logo.png", width=120)

# =========================
# HEADER (LOGO + TITLE)
# =========================
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo.png", width=80)

with col2:
    st.title("🍬 Nassau Candy Intelligence Platform")
    st.caption("AI-powered profitability & performance analytics")

st.markdown("---")

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
body { background-color:#0e1117; color:white; }

.metric-card {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:18px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:18px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.4);
}

.insight-box {
    background-color:#1c1f26;
    padding:15px;
    border-left:5px solid #00c8ff;
    border-radius:10px;
    margin-bottom:10px;
    line-height:1.6;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    division = st.sidebar.multiselect(
        "Division",
        sorted(df["Division"].dropna().unique()),
        default=sorted(df["Division"].dropna().unique())
    )
    df = df[df["Division"].isin(division)]

if "Region" in df.columns:
    region = st.sidebar.multiselect(
        "Region",
        sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique())
    )
    df = df[df["Region"].isin(region)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# KPI CARDS
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()
total_units = df["Units"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="metric-card">💰 Revenue<br>${total_sales:,.0f}</div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card">📈 Gross Profit<br>${total_profit:,.0f}</div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card">📊 Avg Margin<br>{avg_margin:.2f}%</div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card">📦 Units Sold<br>{total_units:,.0f}</div>', unsafe_allow_html=True)

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
    color="Gross Profit",
    title="Top 10 Products by Gross Profit"
)

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# AI INSIGHTS
# =========================
st.subheader("🤖 Executive Insights")

top_product = top_products.iloc[0]["Product Name"]

low_margin_df = df[df["Gross Margin %"] < 20]
volume_trap_df = df[
    (df["Sales"] > df["Sales"].quantile(0.75)) &
    (df["Gross Margin %"] < 25)
]

# =========================
# EXECUTIVE SUMMARY
# =========================
st.markdown(f"""
<div class="insight-box">
<b>📌 Executive Summary</b><br>
The business generated <b>${total_sales:,.0f}</b> in revenue and <b>${total_profit:,.0f}</b> in gross profit,
with an average margin of <b>{avg_margin:.2f}%</b>.<br><br>

<b>{top_product}</b> is the leading profit contributor.
However, <b>{len(low_margin_df)}</b> low-margin products and 
<b>{len(volume_trap_df)}</b> volume traps are reducing profitability.<br><br>

<b>Recommendation:</b> Focus on pricing optimization, cost reduction, and scaling high-margin products.
</div>
""", unsafe_allow_html=True)

# =========================
# KEY OBSERVATIONS
# =========================
st.markdown("### 🔍 Key Observations")

insights = [
    f"Revenue: ${total_sales:,.0f} | Gross Profit: ${total_profit:,.0f}",
    f"Average margin is {avg_margin:.2f}%",
    f"Top product: {top_product}",
    f"{len(low_margin_df)} products have margin below 20%",
    f"{len(volume_trap_df)} high-sales products are low-margin (volume trap)"
]

for i in insights:
    st.markdown(f'<div class="insight-box">{i}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# NAVIGATION
# =========================
st.info("👉 Use the sidebar to explore deeper analytics: Product | Division | Risk | Pareto | AI | Pricing | Geo | Report")
