import streamlit as st
import pandas as pd

def apply_filters(df):

    st.sidebar.header("🔍 Global Filters")

    # =========================
    # DATE FILTER
    # =========================
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

        min_date = df["Order Date"].min()
        max_date = df["Order Date"].max()

        date_range = st.sidebar.date_input(
            "📅 Date Range",
            [min_date, max_date],
            key="date_filter"   # ✅ FIX
        )

        if len(date_range) == 2:
            df = df[
                (df["Order Date"] >= pd.to_datetime(date_range[0])) &
                (df["Order Date"] <= pd.to_datetime(date_range[1]))
            ]

    # =========================
    # DIVISION
    # =========================
    if "Division" in df.columns:
        division = st.sidebar.multiselect(
            "Division",
            df["Division"].unique(),
            default=df["Division"].unique(),
            key="division_filter"   # ✅ FIX
        )
        df = df[df["Division"].isin(division)]

    # =========================
    # PRODUCT SEARCH
    # =========================
    if "Product Name" in df.columns:
        search = st.sidebar.text_input(
            "🔍 Search Product",
            key="product_search"   # ✅ FIX
        )

        if search:
            df = df[df["Product Name"].str.contains(search, case=False, na=False)]

    # =========================
    # MARGIN SLIDER
    # =========================
    if "Gross Margin %" in df.columns:
        margin = st.sidebar.slider(
            "📊 Margin Threshold (%)",
            0, 100, 0,
            key="margin_filter"   # ✅ FIX
        )

        df = df[df["Gross Margin %"] >= margin]

    return df
