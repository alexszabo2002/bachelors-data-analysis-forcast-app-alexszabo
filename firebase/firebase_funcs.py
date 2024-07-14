import firebase_admin
from firebase_admin import credentials, firestore, storage
import json
from io import BytesIO
import uuid
import pandas as pd
import os


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


def save_dataframe_to_firebase(df, user_id, file_name):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    random_filename = uuid.uuid4()
    file_url = f'{user_id}/dataframes/{random_filename}.csv'

    blob = bucket.blob(file_url)
    blob.upload_from_file(csv_buffer, content_type='text/csv')

    db.collection('file_uploads').add({
        'user_id': user_id,
        'filename': f'{file_name}.csv',
        'url': file_url,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    return blob.path


def save_image_to_firebase(image_path, user_id):
    with open(image_path, "rb") as img_file:
        img_buffer = BytesIO(img_file.read())

    random_filename = uuid.uuid4()
    file_url = f'{user_id}/images/{random_filename}.png'

    blob = bucket.blob(file_url)
    blob.upload_from_file(img_buffer, content_type='image/png')

    db.collection('image_uploads').add({
        'user_id': user_id,
        'filename': os.path.basename(image_path),
        'url': file_url,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    return blob.path


def get_all_file_uploads_links():
    docs = db.collection('file_uploads').stream()
    links = {f"{doc.to_dict()['filename']} ({doc.to_dict()['timestamp']})": doc.to_dict() for doc in docs}
    
    return links


def get_all_image_uploads_links():
    docs = db.collection('image_uploads').stream()
    links = {f"{doc.to_dict()['filename']} ({doc.to_dict()['timestamp']})": doc.to_dict() for doc in docs}
    
    return links


def get_file_from_firebase(file_url):
    blob = bucket.blob(file_url)
    file = blob.download_as_bytes()
    
    return BytesIO(file)
