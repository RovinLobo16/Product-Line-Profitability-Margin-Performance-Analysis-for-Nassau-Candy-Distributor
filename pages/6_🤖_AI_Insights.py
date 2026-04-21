import streamlit as st
from utils import load_data
from ai_module import generate_insights

df = load_data()

st.title("🤖 AI Insights")

insights = generate_insights(df)

for i in insights:
    st.info(i)
