import os

import requests
import streamlit as st


st.set_page_config(page_title="AI Sales Agent", layout="centered")
st.title("AI Sales Agent")

api_base = os.getenv("API_BASE_URL", "http://localhost:8000")

with st.sidebar:
    st.caption("API")
    api_base = st.text_input("API base URL", value=api_base)

company_url = st.text_input("Company URL", value="https://example.com")
analyze = st.button("Analyze company")

col1, col2 = st.columns(2)
with col1:
    if st.button("Health"):
        try:
            r = requests.get(f"{api_base}/health", timeout=5)
            st.json(r.json())
        except Exception as e:
            st.error(str(e))

with col2:
    st.write("")

st.divider()

if analyze:
    try:
        r = requests.post(f"{api_base}/analyze_company", json={"company_url": company_url}, timeout=60)
        data = r.json()
        if r.status_code >= 400:
            st.error(data)
        else:
            st.subheader("Company profile")
            st.json(data.get("company", {}))

            st.subheader("Insights")
            st.json(data.get("insights", {}))

            if st.button("Generate report"):
                rr = requests.post(
                    f"{api_base}/generate_report",
                    json={"company": data.get("company", {}), "insights": data.get("insights", {}), "format": "both"},
                    timeout=30,
                )
                report = rr.json()
                st.subheader("Report (JSON)")
                st.json(report.get("json", {}))
                st.subheader("Report (Markdown)")
                st.code(report.get("markdown", ""), language="markdown")
    except Exception as e:
        st.error(str(e))

