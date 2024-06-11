import streamlit as st
import streamlit.components.v1 as components

from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("### Welcome to homepage!")
st.markdown("# Data Analysis and Forecast App")

top_left_col, top_right_col = st.columns(2)

with top_left_col:
    with st.columns(5)[2]:
        st.markdown("# :bar_chart:")
    top_left_btn = st.button(label="Data Analysis", use_container_width=True)

with top_right_col:
    with st.columns(5)[2]:
        st.markdown("# :chart_with_upwards_trend:")
    top_right_btn = st.button(label="Forecast", use_container_width=True)
