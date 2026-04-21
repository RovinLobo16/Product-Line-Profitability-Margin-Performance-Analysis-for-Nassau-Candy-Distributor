import streamlit as st
import plotly.express as px
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

st.title("📦 Product Performance Analysis")
st.caption("Identify profit drivers, risks, and optimization opportunities")

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
# AGGREGATE
# =========================
product = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

product["Margin %"] = (product["Gross Profit"] / product["Sales"]) * 100

# =========================
# DYNAMIC THRESHOLDS
# =========================
sales_q75 = product["Sales"].quantile(0.75)
margin_q75 = product["Margin %"].quantile(0.75)

# =========================
# CLASSIFICATION (IMPROVED)
# =========================
def classify(row):
    if row["Sales"] >= sales_q75 and row["Margin %"] >= margin_q75:
        return "High Value ⭐"
    elif row["Sales"] >= sales_q75 and row["Margin %"] < 25:
        return "Volume Trap ⚠️"
    elif row["Margin %"] < 20:
        return "Low Performer ❌"
    else:
        return "Moderate"

product["Category"] = product.apply(classify, axis=1)

# =========================
# KPI SUMMARY (NEW)
# =========================
st.subheader("📊 Product KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Products", len(product))
col2.metric("Avg Margin", f"{product['Margin %'].mean():.2f}%")
col3.metric("Total Profit", f"${product['Gross Profit'].sum():,.0f}")

# =========================
# SCATTER PLOT (IMPROVED)
# =========================
st.subheader("📈 Product Segmentation")

fig = px.scatter(
    product,
    x="Sales",
    y="Margin %",
    color="Category",
    size="Gross Profit",
    hover_name="Product Name",
    title="Sales vs Margin Segmentation",
    size_max=60
)

# Reference lines
fig.add_hline(y=25, line_dash="dash", annotation_text="Margin Benchmark")
fig.add_vline(x=sales_q75, line_dash="dash", annotation_text="Top 25% Sales")

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TOP PRODUCTS
# =========================
st.subheader("🏆 Top Profit Drivers")

top_products = product.sort_values(
    by="Gross Profit", ascending=False
).head(10)

st.dataframe(top_products, use_container_width=True)

# =========================
# FOCUS PRODUCTS (NEW)
# =========================
st.subheader("🎯 Action Focus")

volume_traps = product[product["Category"] == "Volume Trap ⚠️"]
low_perf = product[product["Category"] == "Low Performer ❌"]

colA, colB = st.columns(2)

colA.warning(f"{len(volume_traps)} products are high sales but low margin.")
colB.error(f"{len(low_perf)} products need immediate review.")

# =========================
# INSIGHTS (UPGRADED)
# =========================
st.subheader("🧠 Insights")

top_product = product.loc[
    product["Gross Profit"].idxmax(), "Product Name"
]

st.markdown(f"""
- **Top profit driver:** {top_product}  
- **High-value products:** {len(product[product['Category']=='High Value ⭐'])}  
- **Volume traps:** {len(volume_traps)}  
- **Low performers:** {len(low_perf)}  

📌 **Recommendation:**  
Focus on scaling high-margin products and optimizing pricing for volume traps.
""")

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Product Analysis",
    product.to_csv(index=False),
    file_name="product_analysis.csv",
    mime="text/csv"
)
