import streamlit as st
import plotly.express as px
from components.filters import apply_filters
from utils import load_data

df = load_data()
df, margin_threshold = apply_filters(df)

# =========================
# LOAD DATA
# =========================

if df.empty:
    st.error("No data available")
    st.stop()

st.title("⚠️ Cost vs Sales Risk Analysis")
st.caption("Identify cost inefficiencies and margin risks")

# =========================
# SIDEBAR FILTERS
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
# AGGREGATE BY PRODUCT (IMPORTANT)
# =========================
risk_df = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Cost": "sum",
    "Gross Profit": "sum"
}).reset_index()

# Safe ratio
risk_df["Cost Ratio"] = risk_df["Cost"] / risk_df["Sales"]

# =========================
# DYNAMIC BENCHMARK
# =========================
avg_cost_ratio = risk_df["Cost Ratio"].mean()

# =========================
# CLASSIFICATION (SMARTER)
# =========================
def classify(row):
    if row["Cost Ratio"] > 0.8:
        return "High Risk 🔴"
    elif row["Cost Ratio"] > avg_cost_ratio:
        return "Moderate Risk 🟡"
    else:
        return "Efficient 🟢"

risk_df["Risk Category"] = risk_df.apply(classify, axis=1)

# =========================
# KPI SUMMARY
# =========================
st.subheader("📊 Risk KPIs")

high_risk = len(risk_df[risk_df["Risk Category"] == "High Risk 🔴"])
moderate_risk = len(risk_df[risk_df["Risk Category"] == "Moderate Risk 🟡"])
efficient = len(risk_df[risk_df["Risk Category"] == "Efficient 🟢"])

col1, col2, col3 = st.columns(3)

col1.metric("High Risk Products", high_risk)
col2.metric("Moderate Risk", moderate_risk)
col3.metric("Efficient Products", efficient)

# =========================
# SCATTER PLOT (IMPROVED)
# =========================
st.subheader("📈 Cost Efficiency Map")

fig = px.scatter(
    risk_df,
    x="Sales",
    y="Cost",
    color="Risk Category",
    size="Gross Profit",
    hover_name="Product Name",
    title="Cost vs Sales Risk Segmentation",
    size_max=60
)

# Ideal cost line (60%)
fig.add_scatter(
    x=risk_df["Sales"],
    y=risk_df["Sales"] * 0.6,
    mode="lines",
    name="Ideal Cost (60%)"
)

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TOP RISK PRODUCTS
# =========================
st.subheader("🚨 High-Risk Products")

high_risk_df = risk_df[
    risk_df["Risk Category"] == "High Risk 🔴"
].sort_values(by="Cost Ratio", ascending=False)

st.dataframe(high_risk_df.head(10), use_container_width=True)

# =========================
# INSIGHTS (UPGRADED)
# =========================
st.subheader("🧠 Strategic Insights")

worst_product = high_risk_df.iloc[0]["Product Name"] if not high_risk_df.empty else "N/A"

st.markdown(f"""
- **High-risk products:** {high_risk}  
- **Moderate risk products:** {moderate_risk}  
- **Worst cost efficiency:** {worst_product}  

📌 **Key Insight:**  
Several products are consuming a large portion of revenue as cost, reducing profitability.

📌 **Recommendation:**  
- Reduce cost structure for high-risk products  
- Re-evaluate pricing strategy  
- Focus on scaling efficient products  
""")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Risk Analysis",
    risk_df.to_csv(index=False),
    file_name="risk_analysis.csv",
    mime="text/csv"
)
