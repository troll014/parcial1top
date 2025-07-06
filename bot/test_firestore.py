import firebase_admin
from firebase_admin import credentials, firestore

def test_firestore_connection():
    try:
        cred = credentials.Certificate('firebase_credentials.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        doc_ref = db.collection('test').document('connection_test')
        doc_ref.set({'status': 'success'})
        print("Successfully wrote test document to Firestore.")
    except Exception as e:
        print(f"Error writing test document to Firestore: {e}")

if __name__ == "__main__":
    test_firestore_connection()
    input("Press Enter to exit...")
