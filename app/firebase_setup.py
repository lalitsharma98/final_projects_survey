# import firebase_admin
# from firebase_admin import credentials, firestore

# if not firebase_admin._apps:
#     cred = credentials.Certificate(r"C:\Users\Lalit.Sharma\OneDrive - languageline.com\What-ifs\survey\survey\firebase-key.json")
#     firebase_admin.initialize_app(cred)

# db = firestore.client()
# print(db)

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Build the service account dict from Streamlit secrets
firebase_config = {
    "type": st.secrets["FIREBASE"]["type"],
    "project_id": st.secrets["FIREBASE"]["project_id"],
    "private_key_id": st.secrets["FIREBASE"]["private_key_id"],
    "private_key": st.secrets["FIREBASE"]["private_key"],
    "client_email": st.secrets["FIREBASE"]["client_email"],
    "client_id": st.secrets["FIREBASE"]["client_id"],
    "auth_uri": st.secrets["FIREBASE"]["auth_uri"],
    "token_uri": st.secrets["FIREBASE"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["FIREBASE"]["client_x509_cert_url"],
    "universe_domain": st.secrets["FIREBASE"]["universe_domain"],
}

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

# Get Firestore DB
db = firestore.client()
print(db)
