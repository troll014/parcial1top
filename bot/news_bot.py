import asyncio
from pyppeteer import launch
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import time
from google import genai

def initialize_firebase():
    try:
        cred = credentials.Certificate('firebase_credentials.json')
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return None

db = initialize_firebase()

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyCsVh2SR_GdPlI2MvtC0qi4cWlmOKNzkjo")

def generate_summary_with_gemini(text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Rewrite the following news title into a detailed news summary:\nTitle: {text}\nSummary:"
        )
        return response.text.strip()
    except Exception as e:
        print(f"Exception during Gemini API call: {e}")
        return "No hay resumen disponible"

async def scrape_news():
    url = "https://elpais.com/america/"
    browser = await launch(executablePath='C:\\Users\\looja\\AppData\\Local\\Chromium\\Application\\chrome.exe', headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await asyncio.sleep(5)  # wait for dynamic content to load

    articles = await page.evaluate('''() => {
        const articleNodes = document.querySelectorAll('article');
        const articles = [];
        articleNodes.forEach(article => {
            const titleElem = article.querySelector('h2');
            const summaryElem = article.querySelector('p.c_d');
            const title = titleElem ? titleElem.innerText.trim() : null;
            const content = summaryElem ? summaryElem.innerText.trim() : null;
            if (title) {
                articles.push({title, content});
            }
        });
        return articles;
    }''')

    await browser.close()

    # Add publishedAt, source fields and generate summary with Gemini if missing
    now = datetime.datetime.now()
    for article in articles:
        print(f"Processing article: {article['title']}")
        print(f"Original content: {article['content']}")
        article['publishedAt'] = now.isoformat()
        article['source'] = "El País América"
        if not article['content'] or article['content'] == "No hay resumen disponible":
            # Use Gemini API to generate summary from title
            generated_summary = generate_summary_with_gemini(article['title'])
            print(f"Generated summary: {generated_summary}")
            article['content'] = generated_summary

    return articles

def publish_news_to_firebase(articles):
    if db is None:
        print("Firestore client is not initialized. Cannot publish articles.")
        return

    for i, article in enumerate(articles):
        # Skip articles with default summary
        if not article['content'] or article['content'] == "No hay resumen disponible":
            print(f"Skipping article '{article['title']}' due to missing or default summary.")
            continue

        # publishedAt is already ISO string
        # Check if article already exists by title
        try:
            docs = db.collection("news").where("title", "==", article["title"]).stream()
            if any(docs):
                print(f"Article '{article['title']}' already exists. Skipping.")
                continue
        except Exception as e:
            print(f"Error checking existing articles in Firestore: {e}")
            continue

        # Add new article
        try:
            db.collection("news").add(article)
            print(f"Published article '{article['title']}' to Firebase.")
        except Exception as e:
            print(f"Error publishing article '{article['title']}' to Firebase: {e}")

        # Publish only one article and stop
        print("Published one article, stopping for verification.")
        break

async def main():
    print("Iniciando el bot de noticias con pyppeteer y resumen generado por Gemini...")
    try:
        print("\nObteniendo noticias nuevas...")
        articles = await scrape_news()
        if articles:
            print(f"Se encontraron {len(articles)} artículos")
            publish_news_to_firebase(articles)
            print("Artículos publicados en Firebase")
        else:
            print("No se encontraron nuevos artículos")
    except Exception as e:
        print(f"Error en el ciclo principal: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
