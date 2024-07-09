import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
import json
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt


def initialize_firebase():

    if not firebase_admin._apps:

        with open("./firebase/firebase_config.json") as f:
            firebase_config = json.load(f)

        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            'storageBucket': firebase_config['storageBucket']
        })

initialize_firebase()

db = firestore.client()
bucket = storage.bucket()


def save_dataframe_to_firebase(df, user_id, filename):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    blob = bucket.blob(f'{user_id}/dataframes/{filename}.csv')
    blob.upload_from_file(csv_buffer, content_type='text/csv')
    return blob.public_url


def save_plot_to_firebase(plot_figure, user_id, filename):
    img_buffer = BytesIO()
    plot_figure.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    blob = bucket.blob(f'{user_id}/plots/{filename}.png')
    blob.upload_from_file(img_buffer, content_type='image/png')
    return blob.public_url
