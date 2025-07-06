import firebase_admin
from firebase_admin import credentials, firestore

def list_news():
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    print("Listing news articles in Firestore:")
    docs = db.collection("news").stream()
    count = 0
    for doc in docs:
        data = doc.to_dict()
        print(f"Title: {data.get('title')}")
        print(f"Content: {data.get('content')}")
        print(f"Published At: {data.get('publishedAt')}")
        print(f"Source: {data.get('source')}")
        print("-----")
        count += 1
    if count == 0:
        print("No news articles found in Firestore.")

if __name__ == "__main__":
    list_news()
