import streamlit as st
import plotly.express as px
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("⚠️ Cost vs Sales Risk Analysis")

# =========================
# SIDEBAR FILTER
# =========================
division_filter = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

df = df[df["Division"].isin(division_filter)]

# =========================
# CREATE COST RATIO
# =========================
df["Cost Ratio"] = df["Cost"] / df["Sales"]

# =========================
# CLASSIFICATION
# =========================
def classify(row):
    if row["Cost Ratio"] > 0.8:
        return "High Risk 🔴"
    elif row["Cost Ratio"] > 0.6:
        return "Moderate Risk 🟡"
    else:
        return "Efficient 🟢"

df["Risk Category"] = df.apply(classify, axis=1)

# =========================
# SCATTER PLOT (ENHANCED)
# =========================
fig = px.scatter(
    df,
    x="Sales",
    y="Cost",
    color="Risk Category",
    size="Gross Profit",
    hover_name="Product Name",
    title="Cost vs Sales (Risk Detection)",
    size_max=60
)

# Add reference line (ideal cost)
fig.add_trace(
    px.line(
        x=df["Sales"],
        y=df["Sales"] * 0.6
    ).data[0]
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# RISK SUMMARY
# =========================
st.subheader("🧠 Risk Insights")

high_risk = len(df[df["Risk Category"] == "High Risk 🔴"])
moderate_risk = len(df[df["Risk Category"] == "Moderate Risk 🟡"])

col1, col2 = st.columns(2)

col1.error(f"{high_risk} products have dangerously high costs (>80% of sales).")
col2.warning(f"{moderate_risk} products show moderate cost inefficiency.")

# =========================
# TOP RISK PRODUCTS
# =========================
st.subheader("🚨 High-Risk Products")

risk_products = df[df["Risk Category"] == "High Risk 🔴"] \
    .sort_values(by="Cost Ratio", ascending=False) \
    .head(10)

st.dataframe(risk_products, use_container_width=True)

# =========================
# DOWNLOAD OPTION
# =========================
st.download_button(
    "⬇️ Download Risk Data",
    df.to_csv(index=False),
    file_name="risk_analysis.csv",
    mime="text/csv"
)
