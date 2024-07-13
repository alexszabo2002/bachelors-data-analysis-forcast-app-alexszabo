import streamlit as st

from firebase.firebase_funcs import get_all_links
from pages_funcs.gallery_funcs import restore_dataframe

st.title("Gallery")

links = get_all_links()

restore_dataframe(links)
