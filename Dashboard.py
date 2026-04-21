import streamlit as st

st.set_page_config(page_title="AI Dashboard", layout="wide")

st.markdown("""
<style>
body { background-color:#0e1117; color:white; }
.metric {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:15px; border-radius:12px; text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.title("🍬 Nassau Candy AI Intelligence Platform")

st.write("Use sidebar to navigate modules.")
