import streamlit as st
import plotly.graph_objects as go
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("📈 Pareto Analysis (80/20 Rule)")

# =========================
# AGGREGATE DATA
# =========================
product = df.groupby("Product Name")["Gross Profit"].sum().reset_index()
product = product.sort_values(by="Gross Profit", ascending=False)

# Calculate cumulative %
product["Cumulative %"] = (
    product["Gross Profit"].cumsum() /
    product["Gross Profit"].sum()
) * 100

# Limit display (top 30 for readability)
display_df = product.head(30)

# =========================
# PARETO CHART
# =========================
fig = go.Figure()

# Bar (profit)
fig.add_bar(
    x=display_df["Product Name"],
    y=display_df["Gross Profit"],
    name="Profit",
)

# Line (cumulative %)
fig.add_scatter(
    x=display_df["Product Name"],
    y=display_df["Cumulative %"],
    name="Cumulative %",
    yaxis="y2",
    mode="lines+markers"
)

# Add 80% reference line
fig.add_hline(
    y=80,
    line_dash="dash",
    annotation_text="80% Threshold",
    yref="y2"
)

# Layout improvements
fig.update_layout(
    title="Profit Concentration (Top Products)",
    xaxis_title="Product",
    yaxis_title="Profit",
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right"
    ),
    xaxis_tickangle=45,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.subheader("🧠 Pareto Insights")

# Find number of products contributing to 80%
top_80 = product[product["Cumulative %"] <= 80]
num_products = len(top_80)
total_products = len(product)

percentage = (num_products / total_products) * 100

col1, col2 = st.columns(2)

col1.success(
    f"{num_products} products contribute to ~80% of total profit."
)

col2.info(
    f"That is only {percentage:.2f}% of all products."
)

# =========================
# TOP CONTRIBUTORS TABLE
# =========================
st.subheader("🏆 Top Profit-Contributing Products")

st.dataframe(top_80.head(10), use_container_width=True)

# =========================
# DOWNLOAD OPTION
# =========================
st.download_button(
    "⬇️ Download Pareto Data",
    product.to_csv(index=False),
    file_name="pareto_analysis.csv",
    mime="text/csv"
)
