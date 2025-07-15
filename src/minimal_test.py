import streamlit as st
import time
import os

# Minimal test app - no ML imports, no PyTorch
st.set_page_config(
    page_title="Minimal Test",
    page_icon="✨",
    layout="wide"
)

st.title("🧠 Minimal Test App")
st.caption("Testing basic Streamlit functionality")

# Simple input and button
user_input = st.text_area("Enter text:", height=100)
if st.button("Test Button"):
    if user_input:
        st.success(f"✅ Success! You entered: {user_input}")
        st.info("🎉 Streamlit is working correctly!")
    else:
        st.warning("⚠️ Please enter some text")

st.info("👆 This is a minimal test to check if Streamlit works without ML libraries") 