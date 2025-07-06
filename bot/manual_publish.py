import firebase_admin
from firebase_admin import credentials, firestore
import datetime

def add_test_news():
    try:
        cred = credentials.Certificate('firebase_credentials.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        test_article = {
            "title": "Test News Article",
            "content": "This is a manually added test news article for verification.",
            "publishedAt": datetime.datetime.now().isoformat(),
            "source": "Test Source"
        }

        db.collection("news").add(test_article)
        print("Test news article added successfully.")
    except Exception as e:
        print(f"Error adding test news article: {e}")

if __name__ == "__main__":
    add_test_news()
