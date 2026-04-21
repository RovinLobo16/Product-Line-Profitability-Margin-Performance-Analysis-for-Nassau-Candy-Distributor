import streamlit as st
from utils import load_data
from ai_module import generate_insights
from report_generator import create_report
import datetime
import io

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

st.title("📄 AI Report Generator")
st.caption("Generate executive-ready PDF reports with insights")

# =========================
# SIDEBAR FILTERS (NEW 🔥)
# =========================
st.sidebar.header("🔍 Report Filters")

if "Division" in df.columns:
    div = st.sidebar.multiselect(
        "Division", df["Division"].unique(),
        default=df["Division"].unique()
    )
    df = df[df["Division"].isin(div)]

if "Region" in df.columns:
    reg = st.sidebar.multiselect(
        "Region", df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(reg)]

if df.empty:
    st.warning("No data after filters")
    st.stop()

# =========================
# GENERATE INSIGHTS
# =========================
insights = generate_insights(df)

# =========================
# REPORT OPTIONS (NEW 🔥)
# =========================
st.sidebar.header("⚙️ Report Options")

include_sections = {
    "Summary": st.sidebar.checkbox("Summary", True),
    "Performance": st.sidebar.checkbox("Performance", True),
    "Risk": st.sidebar.checkbox("Risk", True),
    "Opportunity": st.sidebar.checkbox("Opportunity", True),
    "Narrative": st.sidebar.checkbox("Narrative", True)
}

# =========================
# INSIGHTS PREVIEW (IMPROVED UI)
# =========================
st.subheader("🧠 Insights Preview")

def render_section(title, items):
    if not items:
        return
    st.markdown(f"### {title}")
    for i in items:
        st.markdown(f"- {i}")

if include_sections["Narrative"]:
    st.markdown("### 📌 Executive Narrative")
    st.info(insights.get("narrative", ""))

if include_sections["Summary"]:
    render_section("📊 Summary", insights.get("summary", []))

if include_sections["Performance"]:
    render_section("🚀 Performance", insights.get("performance", []))

if include_sections["Risk"]:
    render_section("⚠️ Risk", insights.get("risk", []))

if include_sections["Opportunity"]:
    render_section("💡 Opportunity", insights.get("opportunity", []))

st.markdown("---")

# =========================
# REPORT METADATA (NEW 🔥)
# =========================
report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown(f"""
📅 **Report Date:** {report_date}  
📊 **Filters Applied:**  
- Division: {', '.join(div) if 'div' in locals() else 'All'}  
- Region: {', '.join(reg) if 'reg' in locals() else 'All'}
""")

# =========================
# GENERATE REPORT
# =========================
generate = st.button("📥 Generate Report")

if generate:
    with st.spinner("Generating report..."):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Nassau_Report_{timestamp}.pdf"

            # Filter insights based on selection
            filtered_insights = {
                "summary": insights["summary"] if include_sections["Summary"] else [],
                "performance": insights["performance"] if include_sections["Performance"] else [],
                "risk": insights["risk"] if include_sections["Risk"] else [],
                "opportunity": insights["opportunity"] if include_sections["Opportunity"] else [],
                "narrative": insights["narrative"] if include_sections["Narrative"] else ""
            }

            file_path = create_report(filtered_insights, filename)

            st.success("✅ Report Generated Successfully!")

            # Read file into memory (better handling)
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="⬇️ Download Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ Error generating report: {e}")

# =========================
# REFRESH BUTTON (SAFE)
# =========================
if st.button("🔄 Refresh Insights"):
    st.cache_data.clear()
    st.rerun()
