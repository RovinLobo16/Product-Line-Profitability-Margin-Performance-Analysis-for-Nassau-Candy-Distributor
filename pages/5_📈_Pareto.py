import streamlit as st
import plotly.graph_objects as go
from utils import load_data

df = load_data()

product = df.groupby("Product Name")["Gross Profit"].sum().reset_index()
product = product.sort_values(by="Gross Profit", ascending=False)

product["cum%"] = product["Gross Profit"].cumsum()/product["Gross Profit"].sum()*100

fig = go.Figure()

fig.add_bar(x=product["Product Name"], y=product["Gross Profit"])
fig.add_scatter(x=product["Product Name"], y=product["cum%"], yaxis="y2")

fig.update_layout(yaxis2=dict(overlaying='y', side='right'))

st.plotly_chart(fig)
