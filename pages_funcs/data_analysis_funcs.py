import streamlit as st
import pandas as pd
import openpyxl

def load_data(uploaded_file):

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(df)
        except:
            df = pd.read_excel(io=uploaded_file, engine='openpyxl')
            st.write(df)
    else:
        st.stop()
        
    return df

def classify_columns(df):

    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    temporal_columns = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

    return numerical_columns, categorical_columns, temporal_columns

def chart(df, chart_type, x_axis, y_axis, agg_func):

    if not x_axis or not y_axis or not agg_func:
        st.error("Please select all options.")
        return None

    if agg_func == 'Sum':
        grouped_df = df.groupby(x_axis)[y_axis].sum().reset_index()
    elif agg_func == 'Mean':
        grouped_df = df.groupby(x_axis)[y_axis].mean().reset_index()
    elif agg_func == 'Std':
        grouped_df = df.groupby(x_axis)[y_axis].std().reset_index()

    if chart_type:
        if chart_type == 'Area Chart':
            chart = st.area_chart(grouped_df.set_index(x_axis))
        elif chart_type == 'Bar Chart':
            chart = st.bar_chart(grouped_df.set_index(x_axis))
        elif chart_type == 'Line Chart':
            chart = st.line_chart(grouped_df.set_index(x_axis))
        elif chart_type == 'Scatter Chart':
            chart = st.scatter_chart(grouped_df.set_index(x_axis))

    return chart
