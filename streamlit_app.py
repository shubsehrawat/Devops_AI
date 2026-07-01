import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Enterprise DevOps AI Copilot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Enterprise DevOps AI Copilot")
st.caption("Hybrid RAG + Agentic AI")

query = st.text_area(
    "Ask a DevOps Question",
    height=120,
    placeholder="Example: Why did the Payment API fail yesterday?",
)

if st.button("Ask AI", type="primary"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching enterprise knowledge base..."):

        response = requests.post(
            API_URL,
            json={
                "query": query
            }
        )

    if response.status_code != 200:

        st.error("Unable to connect to FastAPI.")
        st.stop()

    result = response.json()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Intent",
            result["intent"]
        )

    with col2:
        st.metric(
            "Confidence",
            f'{result["confidence"]:.2f}'
        )

    st.divider()

    st.subheader("Answer")

    st.markdown(result["answer"])

    st.divider()