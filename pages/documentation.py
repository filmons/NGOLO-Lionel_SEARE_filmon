import streamlit as st

st.set_page_config(
    page_title="Forest fires App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Iframe
st.components.v1.iframe("http://127.0.0.1:8000/docs", 
                        height=1000, 
                        width=1000, 
                        scrolling=True)
