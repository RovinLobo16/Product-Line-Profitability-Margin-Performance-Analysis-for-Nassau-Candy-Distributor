import streamlit as st
import plotly.express as px
from utils import load_data
from components.filters import apply_filters
from utils import load_data

df = load_data()
df = apply_filters(df)

# =========================
# LOAD DATA
# =========================

if df.empty:
    st.error("No data available")
    st.stop()

st.title("🏢 Division Performance Analysis")
st.caption("Evaluate revenue, profitability, and efficiency across divisions")

# =========================
# SIDEBAR FILTERS (UPGRADED)
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    division_filter = st.sidebar.multiselect(
        "Division",
        df["Division"].unique(),
        default=df["Division"].unique()
    )
    df = df[df["Division"].isin(division_filter)]

if "Region" in df.columns:
    region_filter = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(region_filter)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# AGGREGATE DATA
# =========================
division = df.groupby("Division").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

division["Margin %"] = (division["Gross Profit"] / division["Sales"]) * 100

# Contribution %
total_profit = division["Gross Profit"].sum()
division["Profit Contribution %"] = (division["Gross Profit"] / total_profit) * 100

# Sort
division = division.sort_values(by="Gross Profit", ascending=False)

# =========================
# KPI SECTION (UPGRADED)
# =========================
st.subheader("📊 Division KPIs")

col1, col2, col3 = st.columns(3)

top_div = division.iloc[0]
low_div = division.iloc[-1]
avg_margin = division["Margin %"].mean()

col1.metric(
    "Top Division",
    top_div["Division"],
    f"${top_div['Gross Profit']:,.0f}"
)

col2.metric(
    "Lowest Division",
    low_div["Division"],
    f"${low_div['Gross Profit']:,.0f}"
)

col3.metric(
    "Average Margin",
    f"{avg_margin:.2f}%"
)

# =========================
# REVENUE VS PROFIT
# =========================
st.subheader("📊 Revenue vs Profit")

fig = px.bar(
    division,
    x="Division",
    y=["Sales", "Gross Profit"],
    barmode="group",
    text_auto=True,
    title="Revenue vs Gross Profit by Division"
)

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MARGIN ANALYSIS
# =========================
st.subheader("📈 Profitability Analysis")

fig2 = px.bar(
    division,
    x="Division",
    y="Margin %",
    color="Margin %",
    text_auto=True,
    title="Profit Margin by Division"
)

fig2.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# CONTRIBUTION CHART (NEW 🔥)
# =========================
st.subheader("💰 Profit Contribution")

fig3 = px.pie(
    division,
    names="Division",
    values="Gross Profit",
    title="Profit Contribution by Division"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# INSIGHTS (UPGRADED)
# =========================
st.subheader("🧠 Strategic Insights")

high_margin = division.loc[division["Margin %"].idxmax()]
low_margin = division.loc[division["Margin %"].idxmin()]

st.markdown(f"""
- **Top performing division:** {top_div['Division']} generates the highest profit.
- **Most efficient division:** {high_margin['Division']} with {high_margin['Margin %']:.2f}% margin.
- **Underperforming division:** {low_margin['Division']} with lowest margin.

📌 **Recommendation:**
- Scale operations in high-margin divisions  
- Investigate cost structure in low-margin divisions  
- Rebalance investment toward profitable segments  
""")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Division Data",
    division.to_csv(index=False),
    file_name="division_analysis.csv",
    mime="text/csv"
)
