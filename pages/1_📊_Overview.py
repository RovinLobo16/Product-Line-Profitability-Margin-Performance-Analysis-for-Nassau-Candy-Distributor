import streamlit as st
import plotly.express as px
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# =========================
# PAGE TITLE
# =========================
st.title("📊 Executive Overview")
st.caption("High-level business performance snapshot")

# =========================
# SIDEBAR FILTERS (CRITICAL)
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    division = st.sidebar.multiselect(
        "Division", df["Division"].unique(), default=df["Division"].unique()
    )
    df = df[df["Division"].isin(division)]

if "Region" in df.columns:
    region = st.sidebar.multiselect(
        "Region", df["Region"].unique(), default=df["Region"].unique()
    )
    df = df[df["Region"].isin(region)]

if df.empty:
    st.warning("No data after filters.")
    st.stop()

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:18px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}
.small-text {
    font-size:13px;
    opacity:0.8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# KPI CALCULATIONS
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()
total_units = df["Units"].sum()

# Benchmarks (simple internal comparison)
median_margin = df["Gross Margin %"].median()

# =========================
# KPI CARDS (UPGRADED)
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card">
💰 <b>Revenue</b><br>
${total_sales:,.0f}<br>
<span class="small-text">Total sales value</span>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
📈 <b>Gross Profit</b><br>
${total_profit:,.0f}<br>
<span class="small-text">Profit before expenses</span>
</div>
""", unsafe_allow_html=True)

margin_status = "Strong" if avg_margin > median_margin else "Needs Attention"

col3.markdown(f"""
<div class="metric-card">
📊 <b>Avg Margin</b><br>
{avg_margin:.2f}%<br>
<span class="small-text">{margin_status}</span>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card">
📦 <b>Units Sold</b><br>
{total_units:,.0f}<br>
<span class="small-text">Total volume</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SMART INSIGHTS
# =========================
st.subheader("🧠 Executive Insights")

top_product = df.groupby("Product Name")["Gross Profit"].sum().idxmax()
low_margin_count = len(df[df["Gross Margin %"] < 20])
high_margin_count = len(df[df["Gross Margin %"] > 40])

colA, colB, colC = st.columns(3)

colA.success(f"Top profit driver: **{top_product}**")
colB.warning(f"{low_margin_count} products below 20% margin")
colC.info(f"{high_margin_count} high-margin products (>40%)")

# =========================
# TOP PRODUCTS CHART (IMPROVED)
# =========================
st.subheader("📊 Top Profit Drivers")

top_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    text_auto=True,
    color="Gross Profit",
    title="Top 5 Products by Gross Profit"
)

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MINI TREND INSIGHT (NEW)
# =========================
st.subheader("📌 Profitability Snapshot")

st.markdown(f"""
- Revenue generated: **${total_sales:,.0f}**
- Gross profit: **${total_profit:,.0f}**
- Average margin: **{avg_margin:.2f}%**
- Focus area: **Reduce low-margin products and scale high-margin ones**
""")
