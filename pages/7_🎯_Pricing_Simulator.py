import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

st.title("🎯 Pricing Simulator (What-If Analysis)")
st.caption("Simulate price changes with demand elasticity and identify profit-optimal scenarios")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    div = st.sidebar.multiselect("Division", df["Division"].unique(),
                                default=df["Division"].unique())
    df = df[df["Division"].isin(div)]

if "Region" in df.columns:
    reg = st.sidebar.multiselect("Region", df["Region"].unique(),
                                default=df["Region"].unique())
    df = df[df["Region"].isin(reg)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# SELECT PRODUCT
# =========================
products = sorted(df["Product Name"].dropna().unique())
product = st.selectbox("Select Product", products)

subset = df[df["Product Name"] == product]

# =========================
# BASELINE (SAFE)
# =========================
base_sales = subset["Sales"].sum()
base_profit = subset["Gross Profit"].sum()
base_units = subset["Units"].sum()

if base_units <= 0 or base_sales <= 0:
    st.error("Selected product has insufficient data.")
    st.stop()

base_price = base_sales / base_units
base_cost_total = base_sales - base_profit
cost_per_unit = base_cost_total / base_units
base_margin = (base_profit / base_sales) * 100

# =========================
# USER INPUTS
# =========================
colA, colB = st.columns(2)

with colA:
    change = st.slider("Price Change (%)", -30, 60, 0, step=1)

with colB:
    elasticity = st.slider(
        "Demand Elasticity",
        0.0, 2.5, 1.0,
        help=">1 = elastic (demand drops faster when price rises)"
    )

# =========================
# SCENARIO FUNCTION
# =========================
def simulate(change_pct, elasticity, base_units, base_price, cost_per_unit):
    price_factor = 1 + (change_pct / 100.0)
    # Linear elasticity response (simple but interpretable)
    demand_factor = 1 - (elasticity * change_pct / 100.0)
    demand_factor = max(demand_factor, 0)  # clamp

    new_units = base_units * demand_factor
    new_price = base_price * price_factor

    new_sales = new_units * new_price
    new_cost = new_units * cost_per_unit
    new_profit = new_sales - new_cost

    new_margin = (new_profit / new_sales) * 100 if new_sales > 0 else 0
    return new_units, new_sales, new_profit, new_margin

# =========================
# CURRENT SCENARIO
# =========================
new_units, new_sales, new_profit, new_margin = simulate(
    change, elasticity, base_units, base_price, cost_per_unit
)

# =========================
# KPI DISPLAY
# =========================
st.subheader("📊 Scenario Comparison")

def pct_delta(new, base):
    if base == 0:
        return "—"
    return f"{((new - base) / base) * 100:.1f}%"

c1, c2, c3, c4 = st.columns(4)

c1.metric("Units", f"{new_units:,.0f}", pct_delta(new_units, base_units))
c2.metric("Revenue", f"${new_sales:,.0f}", pct_delta(new_sales, base_sales))
c3.metric("Gross Profit", f"${new_profit:,.0f}", pct_delta(new_profit, base_profit))
c4.metric("Margin %", f"{new_margin:.2f}%", f"{new_margin - base_margin:.2f}")

# =========================
# BEFORE VS AFTER BAR
# =========================
fig_bar = go.Figure()
fig_bar.add_bar(name="Baseline", x=["Revenue", "Profit"], y=[base_sales, base_profit])
fig_bar.add_bar(name="Scenario", x=["Revenue", "Profit"], y=[new_sales, new_profit])

fig_bar.update_layout(
    barmode="group",
    title="Baseline vs Scenario",
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig_bar, use_container_width=True)

# =========================
# PROFIT CURVE (OPTIMIZATION)
# =========================
st.subheader("📈 Profit vs Price Change")

grid = np.arange(-30, 61, 2)
profits = []
revenues = []

for g in grid:
    _, s, p, _ = simulate(g, elasticity, base_units, base_price, cost_per_unit)
    profits.append(p)
    revenues.append(s)

# Find optimal (max profit)
opt_idx = int(np.argmax(profits))
opt_change = grid[opt_idx]
opt_profit = profits[opt_idx]

fig_curve = go.Figure()
fig_curve.add_scatter(x=grid, y=profits, mode="lines+markers", name="Profit")
fig_curve.add_scatter(x=grid, y=revenues, mode="lines", name="Revenue", yaxis="y2")

# Mark optimal point
fig_curve.add_scatter(
    x=[opt_change],
    y=[opt_profit],
    mode="markers",
    marker=dict(size=10),
    name="Optimal"
)

fig_curve.update_layout(
    xaxis_title="Price Change (%)",
    yaxis_title="Profit",
    yaxis2=dict(title="Revenue", overlaying="y", side="right"),
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    height=500
)

st.plotly_chart(fig_curve, use_container_width=True)

st.info(f"💡 Profit-maximizing change (given elasticity={elasticity:.2f}): **{opt_change:+d}%**")

# =========================
# ASSUMPTIONS PANEL
# =========================
with st.expander("⚙️ Assumptions"):
    st.markdown(f"""
- Baseline price per unit: **${base_price:,.2f}**
- Cost per unit (assumed constant): **${cost_per_unit:,.2f}**
- Elasticity model: linear demand response
- No capacity constraints or competitor reactions modeled
""")

# =========================
# RECOMMENDATION
# =========================
st.subheader("🧠 Recommendation")

if new_profit > base_profit:
    st.success("✅ Scenario improves profitability. Consider testing (A/B or phased rollout).")
elif new_profit < base_profit:
    st.error("❌ Scenario reduces profit. Avoid or adjust pricing/elasticity assumptions.")
else:
    st.info("⚖️ Minimal impact. Validate with market testing.")

if elasticity > 1.5 and change > 0:
    st.warning("⚠️ High elasticity: price increases may sharply reduce demand.")

# =========================
# DOWNLOAD
# =========================
import pandas as pd
export_df = pd.DataFrame({
    "Price Change %": grid,
    "Revenue": revenues,
    "Profit": profits
})

st.download_button(
    "⬇️ Download Scenario Curve",
    export_df.to_csv(index=False),
    file_name="pricing_scenarios.csv",
    mime="text/csv"
)
