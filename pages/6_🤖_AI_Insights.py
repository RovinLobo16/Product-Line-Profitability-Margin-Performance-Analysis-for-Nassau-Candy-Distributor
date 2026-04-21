import streamlit as st
from utils import load_data
from ai_module import generate_insights

# =========================
# LOAD DATA
# =========================
df = load_data()
insights = generate_insights(df)

st.title("🤖 AI Business Intelligence")

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
.card {
    background-color:#1c1f26;
    padding:18px;
    border-radius:12px;
    margin-bottom:10px;
}

.kpi {
    background: linear-gradient(135deg,#1f77b4,#2ca02c);
    padding:15px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-weight:bold;
}

.high { border-left:5px solid red; }
.medium { border-left:5px solid orange; }
.low { border-left:5px solid green; }
</style>
""", unsafe_allow_html=True)

# =========================
# EXECUTIVE SUMMARY (BULLETS)
# =========================
st.subheader("📊 Executive Snapshot")

cols = st.columns(len(insights["bullets"]))

for i, val in enumerate(insights["bullets"]):
    cols[i].markdown(f'<div class="kpi">{val}</div>', unsafe_allow_html=True)

# =========================
# NARRATIVE
# =========================
st.subheader("🧠 Executive Narrative")

st.markdown(
    f'<div class="card">{insights["narrative"]}</div>',
    unsafe_allow_html=True
)

# =========================
# HELPER FUNCTION
# =========================
def render_section(title, items):
    st.subheader(title)

    for item in items:
        if "HIGH" in item:
            cls = "high"
        elif "MEDIUM" in item:
            cls = "medium"
        else:
            cls = "low"

        st.markdown(
            f'<div class="card {cls}">{item}</div>',
            unsafe_allow_html=True
        )

# =========================
# SECTIONS
# =========================
render_section("🚀 Performance Highlights", insights["performance"])
render_section("⚠️ Risk Alerts", insights["risk"])
render_section("💡 Opportunities", insights["opportunity"])
