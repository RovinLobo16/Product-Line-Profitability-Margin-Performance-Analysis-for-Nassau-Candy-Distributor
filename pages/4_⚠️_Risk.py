import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

fig = px.scatter(df, x="Sales", y="Cost",
                 color="Division", hover_name="Product Name")

st.plotly_chart(fig)
