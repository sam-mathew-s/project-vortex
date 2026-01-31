import os
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# --- THE SAVE FUNCTION ---
def save_to_cloud(url, title, content):
    endpoint = f"{SUPABASE_URL}/rest/v1/pages"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "prefer": "return=representation"
    }
    payload = {"url": url, "title": title, "content": content}

    try:
        response = httpx.post(endpoint, headers=headers, json=payload)
        if response.status_code == 201:
            print(f"SAVED: {title}")
        elif response.status_code == 409:
            print(f"EXISTS: {title}")
        else:
            print(f"DB ERROR: {response.text}")
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

#--- THE NEW CRAWLER FUNCTION ---
def crawl_website(url):
    print(f"CRAWLING: {url}...")

    # Fetch the HTML 
    headers = {f"User-Agent": "VortexBot/1.0"} # Pretend to be a real browser
    try:
        response = httpx.get(url, headers=headers)

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Title
        title = soup.title.string if soup.title else "No Title"

        #Extract Text ( Clean up spaces)
        text_content = soup.get_text(separator=" ", strip=True)[:5000] # Limit to 5000 chars

        print (f"FOUND:  {title}")

        # Save to Cloud
        save_to_cloud(url, title, text_content)

    except Exception as e:
        print(f"FAILED TO CRAWL: {e}")

# --- EXCUTE ---
if __name__ == "__main__":
    # Test with a real site (Paul Graham's Essay)
    crawl_website("https://paulgraham.com/avg.html")