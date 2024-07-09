import streamlit as st
import pandas as pd
from firebase.firebase_script import bucket

from authentication.auth import get_authenticator

authenticator = get_authenticator()

st.markdown("# Gallery")

user_id = 'alexszabo'

blobs = bucket.list_blobs(prefix=f'{user_id}/')

files = [blob.name for blob in blobs]
selected_file = st.selectbox("Select file to display", files)

if selected_file:
    blob = bucket.blob(selected_file)
    url = blob.public_url
    if selected_file.endswith('.csv'):
        df = pd.read_csv(url)
        st.dataframe(df)
    elif selected_file.endswith('.png'):
        st.image(url)
