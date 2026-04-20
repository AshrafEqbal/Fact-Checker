import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from dotenv import load_dotenv
from utils import extract_text_from_pdf, extract_claims, verify_claim
load_dotenv()
st.set_page_config(page_title="Fact Check AI", layout="wide")
st.title("Fact-Check Agent")
st.write("Upload a PDF and verify claims using live web data.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    with st.spinner("Extracting text..."):
        text = extract_text_from_pdf(uploaded_file)
    if not text.strip():
        st.error("Empty or unreadable PDF.")
        st.stop()

    st.success("Text extraction completed.")
    claims = extract_claims(text)
    st.write(f"Detected {len(claims)} claims.")
    claims = claims[:12]
    results = []

    for claim in claims:
        with st.spinner(f"Checking: {claim[:60]}"):
            result = verify_claim(claim)
            results.append((claim, result))

    st.subheader("Results")
    for claim, result in results:
        st.markdown(f"**Claim:** {claim}")
        status = result.get("status", "Unknown")
        explanation = result.get("explanation", "")
        confidence = result.get("confidence", "")
        evidence = result.get("evidence", "")
        if status == "Verified":
            st.success(f"Status: {status}\n\nExplanation: {explanation}\n\nConfidence: {confidence}")
        elif status == "Inaccurate":
            st.warning(f"Status: {status}\n\nExplanation: {explanation}\n\nConfidence: {confidence}")
        elif status == "False":
            st.error(f"Status: {status}\n\nExplanation: {explanation}\n\nConfidence: {confidence}")
        else:
            st.info(f"Status: {status}\n\nExplanation: {explanation}\n\nConfidence: {confidence}")
        if evidence:
            st.caption(f"Evidence: {evidence[:250]}")
        st.markdown("---")
