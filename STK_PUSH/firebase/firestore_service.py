import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(str(settings.FIREBASE_CREDENTIALS))
    firebase_admin.initialize_app(cred)


# Initialize Firestore
db = firestore.client()

class FirestoreService:
    @staticmethod
    def create_meeting(data):
        db.collection('meetings').add(data)

    @staticmethod
    def get_meetings():
        meetings_ref = db.collection('meetings')
        return meetings_ref.stream()

    @staticmethod
    def update_meeting(meeting_id, data):
        db.collection('meetings').document(meeting_id).update(data)

    @staticmethod
    def delete_meeting(meeting_id):
        db.collection('meetings').document(meeting_id).delete()

    @staticmethod
    def create_register_chama(data):
        db.collection('register_chama').add(data)

    @staticmethod
    def get_register_chama():
        register_chama_ref = db.collection('register_chama')
        return register_chama_ref.stream()

    @staticmethod
    def update_register_chama(chama_id, data):
        db.collection('register_chama').document(chama_id).update(data)

    @staticmethod
    def delete_register_chama(chama_id):
        db.collection('register_chama').document(chama_id).delete()

    @staticmethod
    def create_signup(data):
        db.collection('signups').add(data)

    @staticmethod
    def get_signups():
        signups_ref = db.collection('signups')
        return signups_ref.stream()

    @staticmethod
    def update_signup(signup_id, data):
        db.collection('signups').document(signup_id).update(data)

    @staticmethod
    def delete_signup(signup_id):
        db.collection('signups').document(signup_id).delete()

    @staticmethod
    def create_article(data):
        db.collection('articles').add(data)

    @staticmethod
    def get_articles():
        articles_ref = db.collection('articles')
        return articles_ref.stream()

    @staticmethod
    def update_article(article_id, data):
        db.collection('articles').document(article_id).update(data)

    @staticmethod
    def delete_article(article_id):
        db.collection('articles').document(article_id).delete()


    @staticmethod
    def find_register_chama(first_name, phone_number, name_of_chama):
        ref = db.collection('register_chama')
        query = ref.where('first_name', '==', first_name)\
                   .where('phone_number', '==', phone_number)\
                   .where('name_of_chama', '==', name_of_chama)
        results = list(query.stream())
        if results:
            doc = results[0]
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    # @staticmethod
    # def create_register_chama(data):
    #     db.collection('register_chama').add(data)

    @staticmethod
    def find_signup_by_phone(phone_number):
        ref = db.collection('signups')
        query = ref.where('phone_number', '==', phone_number)
        results = list(query.stream())
        if results:
            doc = results[0]
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    @staticmethod
    def get_all_articles():
        articles_ref = db.collection('articles')
        return articles_ref.stream()
    
    @staticmethod
    def find_register_chama_by_phone(phone_number):
        ref = db.collection('register_chama')
        query = ref.where('phone_number', '==', phone_number)
        results = list(query.stream())
        if results:
            doc = results[0]
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    @staticmethod
    def get_all_meetings():
        meetings_ref = db.collection('meetings')
        return meetings_ref.stream()