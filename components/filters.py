import streamlit as st

def apply_filters(df):

    st.sidebar.header("🔍 Global Filters")

    filtered_df = df.copy()

    # =========================
    # DIVISION
    # =========================
    if "Division" in filtered_df.columns:
        divisions = sorted(filtered_df["Division"].dropna().unique())

        selected_div = st.sidebar.multiselect(
            "Division",
            divisions,
            default=divisions
        )

        filtered_df = filtered_df[filtered_df["Division"].isin(selected_div)]

    # =========================
    # REGION
    # =========================
    if "Region" in filtered_df.columns:
        regions = sorted(filtered_df["Region"].dropna().unique())

        selected_reg = st.sidebar.multiselect(
            "Region",
            regions,
            default=regions
        )

        filtered_df = filtered_df[filtered_df["Region"].isin(selected_reg)]

    # =========================
    # PRODUCT
    # =========================
    if "Product Name" in filtered_df.columns:
        products = sorted(filtered_df["Product Name"].dropna().unique())

        selected_prod = st.sidebar.multiselect(
            "Product",
            products
        )

        if selected_prod:
            filtered_df = filtered_df[filtered_df["Product Name"].isin(selected_prod)]

    return filtered_df
