import streamlit as st
from utils import load_data

df = load_data()

st.title("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("Profit", f"${df['Gross Profit'].sum():,.0f}")
col3.metric("Margin", f"{df['Gross Margin %'].mean():.2f}%")
col4.metric("Units", f"{df['Units'].sum():,.0f}")
