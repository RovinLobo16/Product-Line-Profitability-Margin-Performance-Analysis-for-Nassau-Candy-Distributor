import streamlit as st

def show_kpis(df):

    if df.empty:
        st.warning("No data available for KPIs")
        return

    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    avg_margin = df["Gross Margin %"].mean()
    total_units = df["Units"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Revenue",
        f"${total_sales:,.0f}"
    )

    col2.metric(
        "📈 Gross Profit",
        f"${total_profit:,.0f}"
    )

    col3.metric(
        "📊 Avg Margin",
        f"{avg_margin:.2f}%"
    )

    col4.metric(
        "📦 Units Sold",
        f"{total_units:,.0f}"
    )
