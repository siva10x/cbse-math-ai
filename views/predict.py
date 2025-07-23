# views/upload.py
import streamlit as st

def render():
    st.title("🔮 Predict Next Year Questions")

    if st.button("📈 Predict Now"):
        st.info("🧠 Analyzing 10 years of trends...")
        # Placeholder for predicted questions
        st.success("✅ Prediction Complete")
        st.write("**Q1:** Prove that √2 is irrational. [2 Marks]")