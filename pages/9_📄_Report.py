import streamlit as st
from utils import load_data
from ai_module import generate_insights
from report_generator import create_report
import datetime

# =========================
# LOAD DATA
# =========================
df = load_data()

st.title("📄 AI Report Generator")

# =========================
# GENERATE INSIGHTS PREVIEW
# =========================
st.subheader("🧠 Insights Preview")

insights = generate_insights(df)

# Show preview (structured)
for section, items in insights.items():
    if section == "narrative":
        st.info(items)
    else:
        if items:
            st.markdown(f"**{section.upper()}**")
            for i in items:
                st.write("•", i)

st.markdown("---")

# =========================
# GENERATE REPORT
# =========================
if st.button("📥 Generate Report"):

    with st.spinner("Generating report..."):
        try:
            # Create timestamped file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Nassau_Report_{timestamp}.pdf"

            file_path = create_report(insights, filename)

            st.success("✅ Report Generated Successfully!")

            # =========================
            # DOWNLOAD BUTTON
            # =========================
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Report",
                    data=f,
                    file_name=filename,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ Error generating report: {e}")

# =========================
# OPTIONAL REFRESH
# =========================
if st.button("🔄 Refresh Insights"):
    st.cache_data.clear()
    st.experimental_rerun()
