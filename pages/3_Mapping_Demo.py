import streamlit as st
from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("# Mapping Demo")
