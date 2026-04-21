import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau AI Dashboard",
    layout="wide",
    page_icon="🍬"
)

# =========================
# LOAD DATA (SAFE)
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Nassau Candy Distributor.csv")

        df.columns = df.columns.str.strip()

        # Convert numeric
        for col in ["Sales", "Units", "Gross Profit"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Sales", "Units", "Gross Profit"])
        df = df[(df["Sales"] > 0) & (df["Units"] > 0)]

        df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

        return df

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# =========================
# LOGO PATH (FIXED ERROR)
# =========================
LOGO_PATH = "assets/unified_mentor_logo.png"  # your actual file name

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
body { background-color:#0e1117; color:white; }

.metric-card {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:18px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.4);
}

.section {
    margin-top:25px;
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
# HEADER (BIG LOGO + TITLE)
# =========================
col1, col2 = st.columns([1.5, 6])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    else:
        st.warning("Logo not found")

with col2:
    st.markdown("""
        <h1 style='margin-bottom:0;'>🍬 Nassau Candy Intelligence Platform</h1>
        <p style='color:gray; margin-top:0; font-size:16px;'>
        AI-powered profitability & performance analytics
        </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# SIDEBAR (LOGO + FILTERS)
# =========================
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=160)

st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    division = st.sidebar.multiselect(
        "Division",
        df["Division"].unique(),
        default=df["Division"].unique()
    )
    df = df[df["Division"].isin(division)]

if "Region" in df.columns:
    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(region)]

# =========================
# KPI CARDS
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()
total_units = df["Units"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(
    f'<div class="metric-card">💰 Revenue<br>${total_sales:,.0f}</div>',
    unsafe_allow_html=True
)

col2.markdown(
    f'<div class="metric-card">📈 Gross Profit<br>${total_profit:,.0f}</div>',
    unsafe_allow_html=True
)

col3.markdown(
    f'<div class="metric-card">📊 Avg Margin<br>{avg_margin:.2f}%</div>',
    unsafe_allow_html=True
)

col4.markdown(
    f'<div class="metric-card">📦 Units Sold<br>{total_units:,.0f}</div>',
    unsafe_allow_html=True
)

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
    font_color="white"
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
The business generated <b>${total_sales:,.0f}</b> in revenue and 
<b>${total_profit:,.0f}</b> in gross profit,
with an average margin of <b>{avg_margin:.2f}%</b>.<br><br>

<b>{top_product}</b> is the leading profit contributor.<br><br>

⚠️ <b>{len(low_margin_df)}</b> low-margin products  
⚠️ <b>{len(volume_trap_df)}</b> volume traps<br><br>

<b>Recommendation:</b> Optimize pricing, reduce costs, scale high-margin products.
</div>
""", unsafe_allow_html=True)

# =========================
# KEY INSIGHTS
# =========================
st.markdown("### 🔍 Key Observations")

insights = [
    f"Revenue: ${total_sales:,.0f} | Gross Profit: ${total_profit:,.0f}",
    f"Average margin is {avg_margin:.2f}%",
    f"Top product: {top_product}",
    f"{len(low_margin_df)} products have margin below 20%",
    f"{len(volume_trap_df)} high-sales products are low-margin"
]

for i in insights:
    st.markdown(
        f'<div class="insight-box">{i}</div>',
        unsafe_allow_html=True
    )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.info(
    "👉 Use sidebar to explore: Product | Division | Risk | Pareto | AI | Pricing | Geo | Report"
)
