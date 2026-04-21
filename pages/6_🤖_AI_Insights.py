import streamlit as st
from utils import load_data
from ai_module import generate_insights

df = load_data()

st.title("🤖 AI Business Intelligence")

insights = generate_insights(df)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.insight-box {
    background-color:#1c1f26;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}
.high { border-left:5px solid red; }
.medium { border-left:5px solid orange; }
.low { border-left:5px solid green; }
</style>
""", unsafe_allow_html=True)

# =========================
# NARRATIVE SUMMARY
# =========================
st.subheader("🧠 Executive Narrative")

st.markdown(
    f'<div class="insight-box">{insights["narrative"]}</div>',
    unsafe_allow_html=True
)

# =========================
# HELPER FUNCTION
# =========================
def render_insights(title, items):
    st.subheader(title)

    for item in items:
        if "HIGH" in item:
            cls = "high"
        elif "MEDIUM" in item:
            cls = "medium"
        else:
            cls = "low"

        st.markdown(
            f'<div class="insight-box {cls}">{item}</div>',
            unsafe_allow_html=True
        )

# =========================
# DISPLAY SECTIONS
# =========================
render_insights("📊 Summary", insights["summary"])
render_insights("🚀 Performance", insights["performance"])
render_insights("⚠️ Risks", insights["risk"])
render_insights("💡 Opportunities", insights["opportunity"])
