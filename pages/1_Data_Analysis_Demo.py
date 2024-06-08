import streamlit as st
import pandas as pd
import openpyxl

from authentication.auth import get_authenticator
from pages_funcs.data_analysis_funcs import process_data, classify_columns, chart

authenticator = get_authenticator()

st.markdown("# Data Analysis Demo")

uploaded_file = st.file_uploader(label="Upload a file", type=['csv','xlsx'], help="only csv or xlsx files are supported")

df_init, df_filled = process_data(uploaded_file)

if df_init is not None:
    numerical_columns, categorical_columns, temporal_columns = classify_columns(df_filled)

    tab_statistics, tab_charts = st.tabs(["Descriptive Statistics", "Charts"])

    tab_statistics.write(df_filled.describe(include="all"))

    with tab_charts:
        filters_col, display_col = st.columns([0.4, 0.6])

        with filters_col:
            chart_type = st.selectbox(label="What chart would you like to display?",
                                      options=('Bar Chart', 'Line Chart', 'Scatter Chart'))

            if chart_type == 'Bar Chart':
                x_axis = st.selectbox(label="Which is the targeted column for the x-axis?",
                                      options=categorical_columns)
                y_axis = st.selectbox(label="Which is the targeted column for the y-axis?",
                                      options=numerical_columns)
                agg_function = st.selectbox(label="Select aggregation function:",
                                            options=('Count', 'Sum', 'Mean', 'Std'))

            elif chart_type == 'Line Chart':
                x_axis = st.selectbox(label="Which is the targeted column for the x-axis?",
                                      options=temporal_columns)
                y_axis = st.selectbox(label="Which is the targeted column for the y-axis?",
                                      options=numerical_columns)
                agg_function = st.selectbox(label="Select aggregation function:",
                                            options=('Count', 'Sum', 'Mean', 'Std'))

            elif chart_type == 'Scatter Chart':
                x_axis = st.selectbox(label="Which is the targeted column for the x-axis?",
                                      options=numerical_columns)
                y_axis = st.selectbox(label="Which is the targeted column for the y-axis?",
                                      options=numerical_columns)
                agg_function = None

            if x_axis and y_axis and x_axis != y_axis:
                with display_col:
                    chart(df_filled, chart_type, x_axis, y_axis, agg_function)
            else:
                st.warning("Please select different columns for the x-axis and y-axis.")
