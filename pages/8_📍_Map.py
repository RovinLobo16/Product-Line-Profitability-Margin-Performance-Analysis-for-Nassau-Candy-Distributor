import streamlit as st
import pandas as pd

st.title("📍 Geographic Distribution")

# =========================
# LOAD DATA SAFELY
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Nassau Candy Distributor.csv")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# =========================
# CHECK LOCATION DATA
# =========================
required_cols = ["Latitude", "Longitude"]

if all(col in df.columns for col in required_cols):

    # Clean coordinates
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    df = df.dropna(subset=["Latitude", "Longitude"])

    # =========================
    # OPTIONAL METRIC FILTER
    # =========================
    if "Division" in df.columns:
        division_filter = st.sidebar.multiselect(
            "Select Division",
            df["Division"].unique(),
            default=df["Division"].unique()
        )
        df = df[df["Division"].isin(division_filter)]

    # =========================
    # SIZE / COLOR OPTIONS
    # =========================
    size_option = st.selectbox(
        "Bubble Size Based On",
        ["None", "Sales", "Gross Profit"]
    )

    map_df = df.copy()

    if size_option != "None" and size_option in df.columns:
        # Normalize for map sizing
        map_df["size"] = df[size_option] / df[size_option].max()
    else:
        map_df["size"] = 1

    # =========================
    # MAP DISPLAY
    # =========================
    st.subheader("🗺️ Location Map")

    st.map(
        map_df.rename(columns={
            "Latitude": "lat",
            "Longitude": "lon"
        })[["lat", "lon"]]
    )

    # =========================
    # SUMMARY
    # =========================
    st.subheader("📊 Location Summary")

    col1, col2 = st.columns(2)

    col1.metric("Total Locations", len(map_df))
    if "Sales" in df.columns:
        col2.metric("Total Sales", f"${map_df['Sales'].sum():,.0f}")

else:
    # =========================
    # FALLBACK MESSAGE
    # =========================
    st.warning("⚠️ No Latitude/Longitude data available.")

    st.info("""
To enable map visualization, add these columns to your dataset:
- Latitude
- Longitude

Example:
Latitude | Longitude  
40.7128  | -74.0060
""")
