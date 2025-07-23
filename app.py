# app.py
import streamlit as st
from views import upload, practice, predict, analytics

st.set_page_config(page_title="CBSE Math AI", page_icon="📘", layout="wide")

# Sidebar
st.sidebar.title("Thilak Sir's - Super Clever Academy")
st.sidebar.image("assets/logo.png", width=150)

# Setup session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation buttons that update query param (in-place navigation)
nav_items = {
    "🏠 Home": "home",
    "📤 Upload Papers": "upload",
    "🧪 Practice Questions": "practice",
    "🔮 Predict Questions": "predict",
    "📊 Marks Analytics": "analytics"
}

for label, key in nav_items.items():
    if st.sidebar.button(label, type="tertiary"):
        st.session_state.page = key
        st.query_params["page"] = key

# Read current page from query param (default = home)
page = st.query_params.get("page", st.session_state.page)
st.session_state.page = page

# Route to page view
if page == "home":
    st.title("🎓 CBSE Math Assistant")
    st.write("Welcome! Upload question papers and explore predictions, analytics and practice sets.")
elif page == "upload":
    upload.render()
elif page == "practice":
    practice.render()
elif page == "predict":
    predict.render()
elif page == "analytics":
    analytics.render()