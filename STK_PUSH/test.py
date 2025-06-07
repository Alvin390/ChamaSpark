from firebase_admin import credentials, initialize_app, firestore
from decouple import config

firebase_credentials = {
    "type": "service_account",
    "project_id": config('FIREBASE_PROJECT_ID'),
    "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": config('FIREBASE_CLIENT_EMAIL'),
    "client_id": config('FIREBASE_CLIENT_ID'),
    "auth_uri": config('FIREBASE_AUTH_URI'),
    "token_uri": config('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": config('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": config('FIREBASE_CLIENT_X509_CERT_URL'),
}

cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)

db = firestore.client()

def test_firestore():
    doc_ref = db.collection('test').document('test_doc')
    doc_ref.set({'message': 'Hello, Firebase!'})
    print("Data added successfully!")
test_firestore()