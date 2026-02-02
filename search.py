import os 
import httpx 
from google import genai 
from dotenv import load_dotenv 
from brain import ask_vortex_brain 

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_query_embedding(text):
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return result.embeddings[0].values

def search_vortex_smart(query):
    print(f"\n ANALYZING CONCEPT: '{query}'...")

    #convert question to numbers
    query_vector = get_query_embedding(query)

    # RPC call to supabse 
    rpc_url = f"{SUPABASE_URL}/rest/v1/rpc/match_documents"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query_embedding": query_vector,
        "match_threshold": 0.0,
        "match_count": 1
    }

    response = httpx.post(rpc_url, json=payload, headers=headers)
    results = response.json()

    if not results:
        print("No matching concepts found.")
        return
    
    # SUCESS
    best_match = results[0]
    similarity = best_match['similarity'] *100
    print(f"FOUND MATCH ({similarity:.1f}% Confidence)")
    print(f"CONTENT SNIPET: {best_match['content'][:200]}...")

    # Activate Brain 
    print("\n VORTEX AI IS READY.")
    ai_prompt = input("Ask the AI about this result: ")
    if ai_prompt:
        answer = ask_vortex_brain(ai_prompt, best_match['content'])
        print("\n" +"="*40)
        print("VORTEX AI SAYS:")
        print(answer)
        print("="*40 + "\n")

if __name__ == "__main__":
    while True:
        q = input("\n Ask a Question(or 'exit'): ")
        if q == 'exit': break 
        search_vortex_smart(q)
