import streamlit as st

from firebase.firebase_funcs import get_all_file_uploads_links, get_all_image_uploads_links
from pages_funcs.gallery_funcs import restore_dataframe, restore_images

st.title("Gallery")

file_links = get_all_file_uploads_links()

restore_dataframe(file_links)

image_links = get_all_image_uploads_links()

restore_images(image_links)
