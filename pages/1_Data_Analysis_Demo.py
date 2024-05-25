import streamlit as st
import pandas as pd
import openpyxl

from authentication.auth import get_authenticator
from pages_funcs.data_analysis_funcs import load_data, classify_columns, chart

authenticator = get_authenticator()

st.markdown("# Data Analysis Demo")

uploaded_file = st.file_uploader(label="Upload a file", type=['csv','xlsx'], help="only csv or xlsx files are supported")

df = load_data(uploaded_file)

numerical_columns, categorical_columns, temporal_columns = classify_columns(df)

tab_statistics, tab_charts = st.tabs(["Descriptive Statistics", "Charts"])

tab_statistics.write(df.describe(include="all"))

with tab_charts:

    filters_col, display_col = st.columns([0.4, 0.6])

    with filters_col:

        chart_type = st.selectbox(label="What chart would you like to display?",
                              options=('Area Chart', 'Bar Chart', 'Line Chart', 'Scatter Chart'))
        
        if chart_type == 'Bar Chart':
            x_axis = st.selectbox(label="Which is the targeted column for the x-axis?", 
                                 options=categorical_columns)
        if chart_type in ['Area Chart', 'Line Chart']:
            x_axis = st.selectbox(label="Which is the targeted column for the x-axis?", 
                                 options=numerical_columns+temporal_columns)
        if chart_type == 'Scatter Chart':
            x_axis = st.selectbox(label="Which is the targeted column for the x-axis?", 
                                 options=numerical_columns)            

        y_axis = st.selectbox(label="Which is the targeted column for the y-axis?", 
                                 options=numerical_columns)
        
        agg_function = st.selectbox(label="Select aggregation function:",
                                 options=('Sum', 'Mean', 'Std'))
        
    with display_col:

        chart = chart(df, chart_type, x_axis, y_axis, agg_function)
