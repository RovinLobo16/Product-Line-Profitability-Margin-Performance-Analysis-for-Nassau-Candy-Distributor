import streamlit as st
import plotly.graph_objects as go
from utils import load_data

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

st.title("📈 Pareto Analysis (80/20 Rule)")
st.caption("Identify the products driving the majority of profit")

# =========================
# SIDEBAR CONTROL (NEW 🔥)
# =========================
top_n = st.sidebar.slider("Select Top N Products", 10, 50, 30)

# =========================
# AGGREGATE
# =========================
product = df.groupby("Product Name")["Gross Profit"].sum().reset_index()
product = product.sort_values(by="Gross Profit", ascending=False)

total_profit = product["Gross Profit"].sum()

# Contribution %
product["Contribution %"] = (product["Gross Profit"] / total_profit) * 100

# Cumulative %
product["Cumulative %"] = product["Contribution %"].cumsum()

# Limit for visualization
display_df = product.head(top_n)

# =========================
# PARETO CHART
# =========================
fig = go.Figure()

# Bars
fig.add_bar(
    x=display_df["Product Name"],
    y=display_df["Gross Profit"],
    name="Gross Profit"
)

# Cumulative line
fig.add_scatter(
    x=display_df["Product Name"],
    y=display_df["Cumulative %"],
    name="Cumulative %",
    yaxis="y2",
    mode="lines+markers"
)

# 80% line
fig.add_hline(
    y=80,
    line_dash="dash",
    line_color="red",
    annotation_text="80% Threshold",
    yref="y2"
)

fig.update_layout(
    title="Profit Concentration by Product",
    xaxis_title="Product",
    yaxis_title="Gross Profit",
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right"
    ),
    xaxis_tickangle=45,
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    height=550
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# KPI SUMMARY (NEW 🔥)
# =========================
st.subheader("📊 Pareto Summary")

top_80 = product[product["Cumulative %"] <= 80]

num_products = len(top_80)
total_products = len(product)
percentage = (num_products / total_products) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Top Products (80%)", num_products)
col2.metric("Total Products", total_products)
col3.metric("Concentration %", f"{percentage:.2f}%")

# =========================
# INSIGHTS (UPGRADED)
# =========================
st.subheader("🧠 Strategic Insights")

top_product = product.iloc[0]["Product Name"]

st.markdown(f"""
- **Top contributor:** {top_product}  
- **{num_products} products drive ~80% of total profit**  
- Only **{percentage:.2f}% of products** generate the majority of value  

📌 **Key Insight:**  
A small subset of products dominates profitability.

📌 **Recommendation:**  
- Focus on scaling top-performing products  
- Review or eliminate low-impact products  
- Optimize portfolio for efficiency  
""")

# =========================
# TOP CONTRIBUTORS TABLE
# =========================
st.subheader("🏆 Top Profit-Contributing Products")

st.dataframe(top_80.head(10), use_container_width=True)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "⬇️ Download Pareto Data",
    product.to_csv(index=False),
    file_name="pareto_analysis.csv",
    mime="text/csv"
)
