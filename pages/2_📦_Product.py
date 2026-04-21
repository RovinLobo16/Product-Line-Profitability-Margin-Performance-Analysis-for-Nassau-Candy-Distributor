import streamlit as st
import plotly.express as px
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("📦 Product Performance Analysis")

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
# AGGREGATE DATA
# =========================
product = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Gross Profit": "sum"
}).reset_index()

product["Margin %"] = (product["Gross Profit"] / product["Sales"]) * 100

# =========================
# CLASSIFICATION (KEY FEATURE)
# =========================
def classify(row):
    if row["Sales"] > product["Sales"].quantile(0.75) and row["Margin %"] > 30:
        return "High Value ⭐"
    elif row["Sales"] > product["Sales"].quantile(0.75) and row["Margin %"] <= 30:
        return "Volume Trap ⚠️"
    elif row["Margin %"] < 20:
        return "Low Performer ❌"
    else:
        return "Moderate"

product["Category"] = product.apply(classify, axis=1)

# =========================
# SCATTER PLOT
# =========================
fig = px.scatter(
    product,
    x="Sales",
    y="Margin %",
    color="Category",
    size="Gross Profit",
    hover_name="Product Name",
    title="Product Segmentation (Sales vs Margin)",
    size_max=60
)

# Add reference lines
fig.add_hline(y=30, line_dash="dash", line_color="green")
fig.add_hline(y=20, line_dash="dash", line_color="red")

st.plotly_chart(fig, use_container_width=True)

# =========================
# TOP PRODUCTS TABLE
# =========================
st.subheader("🏆 Top Products by Profit")

top_products = product.sort_values(
    by="Gross Profit", ascending=False
).head(10)

st.dataframe(top_products, use_container_width=True)

# =========================
# QUICK INSIGHTS
# =========================
st.subheader("🧠 Insights")

high_value = len(product[product["Category"] == "High Value ⭐"])
volume_trap = len(product[product["Category"] == "Volume Trap ⚠️"])
low_perf = len(product[product["Category"] == "Low Performer ❌"])

col1, col2, col3 = st.columns(3)

col1.success(f"{high_value} high-value products driving strong profit.")
col2.warning(f"{volume_trap} products are high sales but low margin.")
col3.error(f"{low_perf} products underperform and need review.")

# =========================
# DOWNLOAD OPTION (BONUS)
# =========================
st.download_button(
    "⬇️ Download Product Analysis",
    product.to_csv(index=False),
    file_name="product_analysis.csv",
    mime="text/csv"
)
