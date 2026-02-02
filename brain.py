import os
from google import genai
from dotenv import load_dotenv

# Load secrets
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Wake up the client 
client = genai.Client(api_key=api_key)

def ask_vortex_brain(user_question, context_text):
    print("VORTEX IS THINKING...")

    prompt = f"""
    You are VORTEX, an inteligent assistant.

    CONTEXT FROM DATABASE:
    "{context_text}"

    USER QUESTION:
    "{user_question}"

    ANSWER (Keep it short and technical):
"""
    try:
        # Call the Model (Gemini Flash)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text 
    except Exception as e:
        return f"BRAIN ERROR:{e}"
    
# --- TEST ZONE ---
if __name__ == "__main__":
    test_context = "Python was created by Guido van Rossum in 1991."
    print(ask_vortex_brain("Who is created Python?", test_context))