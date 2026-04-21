import streamlit as st
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# PAGE TITLE
# =========================
st.title("📊 Executive Overview")

# =========================
# CUSTOM CSS (PREMIUM LOOK)
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
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}
.small-text {
    font-size:14px;
    opacity:0.8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CALCULATIONS
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()
total_units = df["Units"].sum()

# Optional: comparison baseline (simple proxy)
sales_per_product = df.groupby("Product Name")["Sales"].sum()
profit_per_product = df.groupby("Product Name")["Gross Profit"].sum()

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card">
💰 <b>Total Sales</b><br>
${total_sales:,.0f}<br>
<span class="small-text">Across all products</span>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
📈 <b>Total Profit</b><br>
${total_profit:,.0f}<br>
<span class="small-text">Net contribution</span>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
📊 <b>Avg Margin</b><br>
{avg_margin:.2f}%<br>
<span class="small-text">Profitability health</span>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card">
📦 <b>Total Units</b><br>
{total_units:,.0f}<br>
<span class="small-text">Volume sold</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# QUICK INSIGHTS (AUTO)
# =========================
st.subheader("🧠 Quick Insights")

top_product = profit_per_product.idxmax()
low_margin_count = len(df[df["Gross Margin %"] < 20])

colA, colB = st.columns(2)

colA.info(f"Top product driving profit: **{top_product}**")
colB.warning(f"{low_margin_count} products have margin below 20%")

# =========================
# OPTIONAL: MINI CHART
# =========================
import plotly.express as px

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
    title="Top 5 Products by Profit"
)

st.plotly_chart(fig, use_container_width=True)
