import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

product = df.groupby("Product Name").agg({
    "Sales":"sum","Gross Profit":"sum"
}).reset_index()

product["Margin %"] = (product["Gross Profit"]/product["Sales"])*100

fig = px.scatter(product, x="Sales", y="Margin %",
                 size="Gross Profit", hover_name="Product Name")

st.plotly_chart(fig, use_container_width=True)
