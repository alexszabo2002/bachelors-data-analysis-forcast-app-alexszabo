import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("### Welcome to homepage!")
st.markdown("# Data Analysis and Forecast App")

left_col, right_col = st.columns(2)

with left_col:
    with st.columns(5)[2]:
        st.markdown("# :bar_chart:")
    left_btn = st.button(label="Data Analysis", use_container_width=True)
    if left_btn:
        switch_page("Data Analysis")

with right_col:
    with st.columns(5)[2]:
        st.markdown("# :chart_with_upwards_trend:")
    right_btn = st.button(label="Forecast", use_container_width=True)
    if right_btn:
        switch_page("Forecast")
