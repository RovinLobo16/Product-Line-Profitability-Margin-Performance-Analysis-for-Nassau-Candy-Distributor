import streamlit as st
import pandas as pd

# Only works if lat/long exists
df = pd.read_csv("Nassau Candy Distributor.csv")

if "Latitude" in df.columns:
    st.map(df[["Latitude","Longitude"]])
else:
    st.warning("No location data available")
