import streamlit as st
import plotly.graph_objects as go
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("🎯 Pricing Simulator (What-If Analysis)")

# =========================
# SELECT PRODUCT
# =========================
product = st.selectbox("Select Product", df["Product Name"].unique())

subset = df[df["Product Name"] == product]

# Aggregate baseline
base_sales = subset["Sales"].sum()
base_profit = subset["Gross Profit"].sum()
base_units = subset["Units"].sum()

base_margin = (base_profit / base_sales) * 100

# =========================
# USER INPUTS
# =========================
change = st.slider("Price Change (%)", -20, 50, 0)

elasticity = st.slider(
    "Demand Sensitivity (Elasticity)",
    0.0, 2.0, 1.0,
    help="Higher = demand drops more when price increases"
)

# =========================
# SIMULATION LOGIC
# =========================
price_factor = 1 + (change / 100)

# Demand adjustment
demand_factor = 1 - (elasticity * change / 100)

# Clamp demand (avoid negative)
demand_factor = max(demand_factor, 0)

new_units = base_units * demand_factor
new_sales = new_units * (base_sales / base_units) * price_factor

# Assume cost unchanged → profit recalculated
cost = base_sales - base_profit
cost_per_unit = cost / base_units

new_cost = new_units * cost_per_unit
new_profit = new_sales - new_cost

new_margin = (new_profit / new_sales) * 100 if new_sales > 0 else 0

# =========================
# KPI DISPLAY
# =========================
st.subheader("📊 Scenario Comparison")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Sales",
    f"${new_sales:,.0f}",
    f"{((new_sales-base_sales)/base_sales)*100:.1f}%"
)

col2.metric(
    "Profit",
    f"${new_profit:,.0f}",
    f"{((new_profit-base_profit)/base_profit)*100:.1f}%"
)

col3.metric(
    "Margin %",
    f"{new_margin:.2f}%",
    f"{new_margin - base_margin:.2f}"
)

# =========================
# VISUAL COMPARISON
# =========================
fig = go.Figure()

fig.add_bar(name="Baseline", x=["Sales", "Profit"], y=[base_sales, base_profit])
fig.add_bar(name="New Scenario", x=["Sales", "Profit"], y=[new_sales, new_profit])

fig.update_layout(
    title="Before vs After Pricing Change",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# AI RECOMMENDATION
# =========================
st.subheader("🧠 Recommendation")

if new_profit > base_profit:
    st.success("✅ Price change improves profitability. Consider implementing.")
elif new_profit < base_profit:
    st.error("❌ Price change reduces profit. Not recommended.")
else:
    st.info("⚖️ Minimal impact. Consider testing in market.")

# Additional insight
if elasticity > 1.5 and change > 0:
    st.warning("⚠️ High elasticity: price increase may significantly reduce demand.")
