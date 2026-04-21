import streamlit as st
from utils import load_data
from ai_module import generate_insights
from report_generator import create_report

df = load_data()

if st.button("Generate Report"):
    insights = generate_insights(df)
    file = create_report(insights)
    st.success("Report Generated!")
