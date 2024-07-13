import streamlit as st
import pandas as pd

from firebase.firebase_funcs import get_file_from_firebase


def restore_dataframe(links):
    if links:
        file_names = list(links.keys())
        selected_file = st.selectbox("Select a file to view", file_names)    
        if selected_file:
            file_data = links[selected_file]
            response_blob = get_file_from_firebase(file_data["url"])
            if not response_blob:
                st.warning("The selected file no longer exists in the database.")
            else:
                loaded_df = pd.read_csv(response_blob)
                st.dataframe(loaded_df)
    else:
        st.warning("No files available in the database.")
