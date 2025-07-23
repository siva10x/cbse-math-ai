# views/upload.py
import streamlit as st

def render():
    st.title("🧪 Generate Practice Questions")

    topic = st.selectbox("Choose a topic", ["Probability", "Linear Equations", "Trigonometry", "Geometry"])
    difficulty = st.radio("Select difficulty level", ["Easy", "Medium", "Hard"])

    if st.button("🎯 Generate"):
        st.info("⏳ Generating practice questions...")
        # Placeholder for generated questions
        st.success("📘 Q1: A fair die is rolled. What is the probability of getting an even number? [1 Mark]")