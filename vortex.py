import os
import httpx
from bs4 import BeautifulSoup
from google import genai
from dotenv import load_dotenv

# Setup
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_embedding(text):
    # convert text into 768 numbers
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return result.embeddings[0].values

def crawl_and_embed(url):
    print(f"CRAWLING: {url}")

    # Get the HTML
    headers = {"User-Agent": "Mozilla/5.0"}
    response = httpx.get(url,headers=headers, follow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")

    # Clean the Text
    title = soup.title.string
    text_content = soup.get_text(separator=' ',strip=True)[:8000] # Limit of 8000 chars
    print(f"FOUND: {title}")

    # GET THE NUMBERS
    print("GENERATING VECTORS...")
    vector = get_embedding(text_content)
    print(f"VECTOR LENGTH: {len(vector)}")
    # Save to the NEW vault table
    data = {
        "filename": title,
        "content": text_content,
        "embedding": vector
    }
    
    print("SAVING TO VAULT...")
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    db_response = httpx.post(f"{SUPABASE_URL}/rest/v1/vault", json=data, headers=headers)

    if db_response.status_code == 201:
        print("SUCCESS: Data + Vectorts Saved!")
    else: 
        print(f"ERROR: {db_response.text}")

if __name__ == "__main__":
    target = input("Enter URL to Embed: ")
    crawl_and_embed(target)
    