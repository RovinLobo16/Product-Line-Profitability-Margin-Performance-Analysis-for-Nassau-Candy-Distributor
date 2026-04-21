import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

division = df.groupby("Division").agg({
    "Sales":"sum","Gross Profit":"sum"
}).reset_index()

fig = px.bar(division, x="Division", y=["Sales","Gross Profit"], barmode="group")

st.plotly_chart(fig)
