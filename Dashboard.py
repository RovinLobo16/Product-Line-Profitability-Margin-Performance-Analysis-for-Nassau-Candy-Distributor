import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")
    df = df[(df["Sales"] > 0) & (df["Units"] > 0)]
    df["Gross Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100
    return df

df = load_data()

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
# TITLE
# =========================
st.title("🍬 Nassau Candy AI Intelligence Platform")

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="metric-card">💰 Sales<br>${df["Sales"].sum():,.0f}</div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card">📈 Profit<br>${df["Gross Profit"].sum():,.0f}</div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card">📊 Avg Margin<br>{df["Gross Margin %"].mean():.2f}%</div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card">📦 Units<br>{df["Units"].sum():,.0f}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# QUICK VISUALS
# =========================
st.subheader("📊 Quick Insights")

import plotly.express as px

# Top 10 products
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
    title="Top 10 Products by Profit"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# AI INSIGHTS (AUTO GENERATED)
# =========================
st.subheader("🤖 AI Insights")

insights = []

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_margin = df["Gross Margin %"].mean()

top_product = top_products.iloc[0]["Product Name"]

low_margin_count = len(df[df["Gross Margin %"] < 20])

volume_trap_count = len(
    df[
        (df["Sales"] > df["Sales"].quantile(0.75)) &
        (df["Gross Margin %"] < 25)
    ]
)

# Generate insights
insights.append(f"Total revenue is ${total_sales:,.0f} with profit of ${total_profit:,.0f}.")
insights.append(f"Average margin is {avg_margin:.2f}%, indicating overall profitability health.")
insights.append(f"Top-performing product is '{top_product}' driving the highest profit.")
insights.append(f"{low_margin_count} products have margins below 20%, indicating cost or pricing issues.")
insights.append(f"{volume_trap_count} high-sales products are generating low margins (volume trap risk).")

# Display nicely
for insight in insights:
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================
# NAVIGATION HELP
# =========================
st.info("👉 Use the sidebar to explore detailed analysis: Product, Division, Risk, Pareto, AI Insights, Pricing Simulator.")
