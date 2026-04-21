import streamlit as st

def apply_filters(df):

    st.sidebar.header("🔍 Global Filters")

    if "Division" in df.columns:
        division = st.sidebar.multiselect(
            "Division", df["Division"].unique(), default=df["Division"].unique()
        )
        df = df[df["Division"].isin(division)]

    if "Region" in df.columns:
        region = st.sidebar.multiselect(
            "Region", df["Region"].unique(), default=df["Region"].unique()
        )
        df = df[df["Region"].isin(region)]

    if "Product Name" in df.columns:
        product = st.sidebar.multiselect(
            "Product", df["Product Name"].unique()
        )
        if product:
            df = df[df["Product Name"].isin(product)]

    return df
