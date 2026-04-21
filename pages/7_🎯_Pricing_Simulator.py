import streamlit as st
from utils import load_data

df = load_data()

product = st.selectbox("Select Product", df["Product Name"].unique())

change = st.slider("Price Change %", -20, 50, 0)

subset = df[df["Product Name"] == product]

new_sales = subset["Sales"] * (1 + change/100)
new_profit = subset["Gross Profit"] * (1 + change/100)

st.write("New Sales:", new_sales.sum())
st.write("New Profit:", new_profit.sum())
