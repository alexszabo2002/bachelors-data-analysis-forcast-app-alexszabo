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
    st.write("")
    st.write("The Data Analysis page allows users to upload CSV or Excel files, preprocess the data, fill missing values, generate descriptive statistics, and create various charts to visualize the data insights.")

with right_col:
    with st.columns(5)[2]:
        st.markdown("# :chart_with_upwards_trend:")
    right_btn = st.button(label="Forecast", use_container_width=True)
    if right_btn:
        switch_page("Forecast")
    st.write("")
    st.write("The Forecast page enables users to select a date range and a ticker symbol for a cryptocurrency or stock, extract data using the yfinance library, analyze the data as a time series, apply the ARIMA model, verify the accuracy of the forecast, calculate RMSE, and forecast future values.")
