from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

class SparkGalFirestore:
    @staticmethod
    def save_message(user_id, conversation_id, role, content, language, feedback=None):
        doc_ref = db.collection('conversations').document(conversation_id)
        doc_ref.collection('messages').add({
            'timestamp': datetime.utcnow(),
            'role': role,
            'content': content,
            'language': language,
            'feedback': feedback,
        })

    @staticmethod
    def create_conversation(user_id):
        doc_ref = db.collection('conversations').document()
        doc_ref.set({
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'last_active': datetime.utcnow(),
        })
        return doc_ref.id

    @staticmethod
    def update_last_active(conversation_id):
        db.collection('conversations').document(conversation_id).update({
            'last_active': datetime.utcnow()
        })
    
    @staticmethod
    def get_last_n_messages(conversation_id, n=5):
        doc_ref = db.collection('conversations').document(conversation_id)
        messages_ref = doc_ref.collection('messages').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(n)
        messages = []
        for doc in messages_ref.stream():
            msg = doc.to_dict()
            # Ensure role/content keys exist for prompt formatting
            msg['role'] = msg.get('role', 'user')
            msg['content'] = msg.get('content', '')
            messages.append(msg)
        # Return in chronological order (oldest first)
        return list(reversed(messages))