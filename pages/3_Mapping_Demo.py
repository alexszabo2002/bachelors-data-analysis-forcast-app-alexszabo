import streamlit as st
import pandas as pd
import pydeck as pdk

from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("# Interactive Map with Date Filter")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Ensure the columns are named appropriately
    data.columns = ['latitude_start', 'longitude_start', 'latitude_end', 'longitude_end', 'datetime', 'id_cursa', 'nume_sofer']

    # Convert the 'datetime' column to datetime type
    data['datetime'] = pd.to_datetime(data['datetime'])

    # Display the uploaded data
    st.write("Uploaded Data:", data)

    # Check if data is loaded correctly
    if not data.empty:
        # Create a slider for selecting date range
        min_date = data['datetime'].min().date()
        max_date = data['datetime'].max().date()

        if min_date != max_date:
            start_date, end_date = st.slider(
                "Select Date Range",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="MM/DD/YY"
            )

            # Filter data based on the selected date range
            filtered_data = data[(data['datetime'] >= pd.to_datetime(start_date)) & (data['datetime'] <= pd.to_datetime(end_date))]

            # Display the filtered data
            st.write("Filtered Data:", filtered_data)

            # Define the scatterplot layer for start points
            start_points_layer = pdk.Layer(
                "ScatterplotLayer",
                data=filtered_data,
                get_position='[longitude_start, latitude_start]',
                get_color='[0, 255, 0, 160]',
                get_radius=100,
                pickable=True,
                auto_highlight=True
            )

            # Define the scatterplot layer for end points
            end_points_layer = pdk.Layer(
                "ScatterplotLayer",
                data=filtered_data,
                get_position='[longitude_end, latitude_end]',
                get_color='[255, 0, 0, 160]',
                get_radius=100,
                pickable=True,
                auto_highlight=True
            )

            # Define the line layer to show routes
            route_layer = pdk.Layer(
                "LineLayer",
                data=filtered_data,
                get_source_position='[longitude_start, latitude_start]',
                get_target_position='[longitude_end, latitude_end]',
                get_color='[0, 0, 255, 160]',
                get_width=5,
                pickable=True,
                auto_highlight=True
            )

            # Define the tooltip
            tooltip = {
                "html": "<b>Start Latitude:</b> {latitude_start} <br/> <b>Start Longitude:</b> {longitude_start} <br/>" +
                        "<b>End Latitude:</b> {latitude_end} <br/> <b>End Longitude:</b> {longitude_end} <br/>" +
                        "<b>Date:</b> {datetime} <br/> <b>Driver:</b> {nume_sofer} <br/> <b>Route ID:</b> {id_cursa}",
                "style": {"color": "white"}
            }

            # Define the view
            view_state = pdk.ViewState(
                latitude=filtered_data['latitude_start'].mean(),
                longitude=filtered_data['longitude_start'].mean(),
                zoom=11,
                pitch=50,
            )

            # Render the deck.gl map
            r = pdk.Deck(layers=[start_points_layer, end_points_layer, route_layer], initial_view_state=view_state, tooltip=tooltip)
            st.pydeck_chart(r)
        else:
            st.write("The date range is invalid, please check your data.")
    else:
        st.write("No data available in the uploaded file.")
else:
    st.write("Please upload a CSV file.")
