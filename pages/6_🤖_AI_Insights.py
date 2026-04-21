import streamlit as st
from utils import load_data
from ai_module import generate_insights
from components.filters import apply_filters
from utils import load_data

df = load_data()
df, margin_threshold = apply_filters(df)

# =========================
# LOAD DATA
# =========================

if df.empty:
    st.error("No data available")
    st.stop()

# =========================
# SIDEBAR FILTERS (NEW 🔥)
# =========================
st.sidebar.header("🔍 Filters")

if "Division" in df.columns:
    division = st.sidebar.multiselect(
        "Division",
        df["Division"].unique(),
        default=df["Division"].unique()
    )
    df = df[df["Division"].isin(division)]

if "Region" in df.columns:
    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(region)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# GENERATE INSIGHTS
# =========================
insights = generate_insights(df)

st.title("🤖 AI Business Intelligence")
st.caption("Automated insights for executive decision-making")

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

.alert {
    background-color:#2b1d1d;
    padding:15px;
    border-left:5px solid red;
    border-radius:10px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# PRIORITY ALERT (NEW 🔥)
# =========================
high_risks = [r for r in insights.get("risk", []) if "HIGH" in r]

if high_risks:
    st.markdown(
        f'<div class="alert">🚨 <b>Critical Risks:</b> {high_risks[0]}</div>',
        unsafe_allow_html=True
    )

# =========================
# EXECUTIVE SNAPSHOT
# =========================
st.subheader("📊 Executive Snapshot")

bullets = insights.get("bullets", [])

cols = st.columns(len(bullets) if bullets else 1)

for i, val in enumerate(bullets):
    cols[i].markdown(f'<div class="kpi">{val}</div>', unsafe_allow_html=True)

# =========================
# EXECUTIVE NARRATIVE
# =========================
st.subheader("🧠 Executive Narrative")

st.markdown(
    f'<div class="card">{insights.get("narrative","No narrative available")}</div>',
    unsafe_allow_html=True
)

# =========================
# HELPER FUNCTION
# =========================
def render_section(title, items):
    if not items:
        return

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
render_section("🚀 Performance Highlights", insights.get("performance", []))
render_section("⚠️ Risk Alerts", insights.get("risk", []))
render_section("💡 Opportunities", insights.get("opportunity", []))

# =========================
# ACTION PANEL (NEW 🔥)
# =========================
st.subheader("🎯 Recommended Actions")

st.markdown("""
<div class="card">
<ul>
<li>Optimize pricing for low-margin products</li>
<li>Reduce cost inefficiencies in high-risk areas</li>
<li>Scale high-performing product lines</li>
<li>Re-evaluate underperforming segments</li>
</ul>
</div>
""", unsafe_allow_html=True)
