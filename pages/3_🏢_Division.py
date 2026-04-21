import streamlit as st
import plotly.express as px
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("🏢 Division Performance Analysis")

# =========================
# SIDEBAR FILTER (OPTIONAL)
# =========================
division_filter = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

df = df[df["Division"].isin(division_filter)]

# =========================
# AGGREGATE DATA
# =========================
division = df.groupby("Division").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

division["Margin %"] = (division["Gross Profit"] / division["Sales"]) * 100

# Sort by profit for better visualization
division = division.sort_values(by="Gross Profit", ascending=False)

# =========================
# KPI SUMMARY
# =========================
st.subheader("📊 Division KPIs")

col1, col2, col3 = st.columns(3)

top_div = division.iloc[0]
low_div = division.iloc[-1]

col1.success(f"Top Division: {top_div['Division']} (${top_div['Gross Profit']:,.0f})")
col2.warning(f"Lowest Division: {low_div['Division']} (${low_div['Gross Profit']:,.0f})")
col3.info(f"Avg Margin: {division['Margin %'].mean():.2f}%")

# =========================
# BAR CHART (IMPROVED)
# =========================
fig = px.bar(
    division,
    x="Division",
    y=["Sales", "Gross Profit"],
    barmode="group",
    text_auto=True,
    title="Revenue vs Profit by Division"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MARGIN CHART (NEW)
# =========================
st.subheader("📈 Profit Margin by Division")

fig2 = px.bar(
    division,
    x="Division",
    y="Margin %",
    color="Margin %",
    title="Division Margin Comparison"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.subheader("🧠 Insights")

high_margin = division.loc[division["Margin %"].idxmax()]
low_margin = division.loc[division["Margin %"].idxmin()]

colA, colB = st.columns(2)

colA.success(
    f"Highest margin division: {high_margin['Division']} ({high_margin['Margin %']:.2f}%)"
)

colB.error(
    f"Lowest margin division: {low_margin['Division']} ({low_margin['Margin %']:.2f}%)"
)

# =========================
# DOWNLOAD OPTION
# =========================
st.download_button(
    "⬇️ Download Division Data",
    division.to_csv(index=False),
    file_name="division_analysis.csv",
    mime="text/csv"
)
