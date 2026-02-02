import streamlit as st 
import os 
import httpx 
from google import genai 
from dotenv import load_dotenv 

#CONFIG
st.set_page_config(page_title="VORTEX AI", page_icon="🌪", layout="centered")
load_dotenv()
PRIMARY_MODEL = "gemini-2.0-flash"
BACKUP_MODEL = "gemini-flash-latest"
EMERGENCY_MODEL = "gemini-pro"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

#ENGINE
def get_query_embedding(text):
    try:
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text,
        )
        return result.embeddings[0].values
    except Exception as e:
        return None 

def ask_brain_hybrid(question, context, model_choice):
    prompt = f"""
    You are VORTEX. Answer based on this CONTEXT:
    {context}

    QUESTION: {question}
"""
    #ATTEMPT 1
    try:
        response = client.models.generate_content(
            model=model_choice,
            contents=prompt
        )
        return response.text, model_choice

    except Exception as e:
        #ATTEMPT 2 
        if model_choice == BACKUP_MODEL:
            return f"❌ System Overload. Please wait 1 minute.", "None"
        
        try:
            response = client.models.generate_content(
                model=BACKUP_MODEL,
                contents=prompt
            )
            return response.text, f"{BACKUP_MODEL} (Backup Active)"
        
        except Exception as e2:
            #ATTEMPT 3 
            try:
                response = client.models.generate_content(
                    model=EMERGENCY_MODEL,
                    contents=prompt
                )
                return response.text, f"{EMERGENCY_MODEL} (Emergency)"
            except Exception as e:
                print(f" FATAL ERROR: {e}")
                return f"❌ ERROR: {e}.", "None"
            
# UI 
st.title("🌪 VORTEX")
st.caption("Hybrid AI Search Engine | Powered by Gemini 2.0 & 1.5")

with st.sidebar:
    st.header("⚙ Engine Settings")
    selected_model = st.radio(
        "Choose Intelligence Level:",
        ["gemini-2.0-flash", "gemini-1.5-flash"],
        captions=["Vortex 2.0 (Smartest)", "Vortex 1.5 (Most Stable)"]
    )
    st.divider()
    st.info(f"Active Core: {selected_model}")

query = st.text_input("Ask a question...", placeholder="e.g., How to get rich?")

if query:
    with st.spinner("🧠 Vortex is searching memories..."):

        try:
            query_vector = get_query_embedding(query)
            
            if query_vector is None:
                st.error("❌ Vector Engine Failed.Check API Key.")
            else:
                rpc_url = f"{SUPABASE_URL}/rest/v1/rpc/match_documents"
                headers = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "query_embedding": query_vector,
                    "match_threshold": 0.3,
                    "match_count": 1
                }

                response = httpx.post(rpc_url, json=payload, headers=headers)
                results = response.json()

                if results:
                    best_match = results[0]
                    similarity = best_match['similarity'] * 100

                    st.success(f"✅ Found Match ({similarity:.1f}% Confidence)")

                    st.markdown("### 🤖 Vortex Answer:")
                    ai_answer, used_model = ask_brain_hybrid(query, best_match['content'], selected_model)

                    if "Backup" in used_model or "Emergency" in used_model:
                        st.warning(f"⚠ Primary Engine Busy. Switched to {used_model}.")

                    st.write(ai_answer)

                    with st.expander("📄 View Original Source Text"):
                        st.info(best_match['content'][:1000] + "...")

                else:
                    st.warning("🔍 No relevant documents found in the database.")

        except Exception as e:
            st.error(f"Critical Error: {e}")
