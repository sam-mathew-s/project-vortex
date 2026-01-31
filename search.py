import os
import httpx
from dotenv import load_dotenv

# Load Secrets
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def search_vortex(query):
    print(f"SEARCHING VORTEX FOR: '{query}'...")

    # The Cloud Query
    # 'ilike' (Case-insensitive matching) and this says find rows where ' content is contains query 
    # The % symbols mean "anything before" and "anything after "

    search_term = f"%{query}%"

    endpoint = f"{SUPABASE_URL}/rest/v1/pages"

    params = {
        "content": f"ilike.{search_term}",
        "select": "*" # Give me all colums  
    }

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    try:
        response = httpx.get(endpoint, headers=headers, params=params)
        results = response.json()

        if len(results) == 0:
            print("No results found in the archives.")
        else:
            print(f"FOUND {len(results)} MATCHES:\n")
            for page in results:
                print(f"URL: {page['url']}")
                print(f"TITLE: {page['title']}")
                # print just the first 100 characters of text to keep it clean
                preview = page['content'][:150].replace("\n", " ")
                print(f"TEXT: {preview}...")
                print("-" * 40)

    except Exception as e:
        print(f"ERROR: {e}")

# --- THE INFINITE LOOP ---
if __name__ == "__main__":
    print("--- VORTEX SEARCH ENGINE ONLINE ---")
    print("(Type 'exit to quit)")

    while True:
        user_input = input("\n Enter Search Term: ")
        break
    
    search_vortex(user_input)

        
        