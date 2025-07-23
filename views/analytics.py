# views/upload.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render():
    st.title("📊 Marks Distribution Analytics")

    # Simulated data for now
    df = pd.DataFrame({
        "Topic": ["Probability", "Geometry", "Algebra", "Trigonometry"],
        "2021": [4, 10, 8, 6],
        "2022": [5, 12, 7, 4],
        "2023": [6, 8, 9, 7]
    })

    df_melt = df.melt(id_vars=["Topic"], var_name="Year", value_name="Marks")
    fig = px.bar(df_melt, x="Topic", y="Marks", color="Year", barmode="group")

    st.plotly_chart(fig, use_container_width=True)