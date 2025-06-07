# Contents for `STK_PUSH/utilis.py`

import firebase_admin
from firebase_admin import credentials, firestore
import requests
from django.conf import settings

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate('c:/Users/USER/Desktop/SCHOOL PROJECTS/Chama Firebase 1/Wamama_Chama_System/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def add_meeting(meeting_data):
    """Add a new meeting to Firestore."""
    meetings_ref = db.collection('meetings')
    meetings_ref.add(meeting_data)

def get_meetings():
    """Retrieve all meetings from Firestore."""
    meetings_ref = db.collection('meetings')
    return meetings_ref.stream()

def update_meeting(meeting_id, updated_data):
    """Update a meeting in Firestore."""
    meetings_ref = db.collection('meetings').document(meeting_id)
    meetings_ref.update(updated_data)

def delete_meeting(meeting_id):
    """Delete a meeting from Firestore."""
    meetings_ref = db.collection('meetings').document(meeting_id)
    meetings_ref.delete()

def add_register_chama(chama_data):
    """Add a new RegisterChama to Firestore."""
    chama_ref = db.collection('register_chama')
    chama_ref.add(chama_data)

def get_register_chama():
    """Retrieve all RegisterChama from Firestore."""
    chama_ref = db.collection('register_chama')
    return chama_ref.stream()

def update_register_chama(chama_id, updated_data):
    """Update a RegisterChama in Firestore."""
    chama_ref = db.collection('register_chama').document(chama_id)
    chama_ref.update(updated_data)

def delete_register_chama(chama_id):
    """Delete a RegisterChama from Firestore."""
    chama_ref = db.collection('register_chama').document(chama_id)
    chama_ref.delete()

def add_signup(signup_data):
    """Add a new SignUp to Firestore."""
    signup_ref = db.collection('signups')
    signup_ref.add(signup_data)

def get_signups():
    """Retrieve all SignUps from Firestore."""
    signup_ref = db.collection('signups')
    return signup_ref.stream()

def update_signup(signup_id, updated_data):
    """Update a SignUp in Firestore."""
    signup_ref = db.collection('signups').document(signup_id)
    signup_ref.update(updated_data)

def delete_signup(signup_id):
    """Delete a SignUp from Firestore."""
    signup_ref = db.collection('signups').document(signup_id)
    signup_ref.delete()

def add_article(article_data):
    """Add a new Article to Firestore."""
    article_ref = db.collection('articles')
    article_ref.add(article_data)

def get_articles():
    """Retrieve all Articles from Firestore."""
    article_ref = db.collection('articles')
    return article_ref.stream()

def update_article(article_id, updated_data):
    """Update an Article in Firestore."""
    article_ref = db.collection('articles').document(article_id)
    article_ref.update(updated_data)

def delete_article(article_id):
    """Delete an Article from Firestore."""
    article_ref = db.collection('articles').document(article_id)
    article_ref.delete()

def get_pesapal_access_token():
    url = f"{settings.PESAPAL_API_BASE_URL}/Auth/RequestToken"
    headers = {"Content-Type": "application/json"}
    data = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None