import os
from google import genai 
from dotenv import load_dotenv 

# Load the key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

print(f"CHECKING KEY: {api_key[:5]}...(Rest hidden)")

# Connect 
try:
    client = genai.Client(api_key=api_key)
    print("CONTACTING GOOGLE SERVERS...")

    # ASK FOR THE LIST
    found_any = False
    for m in client.models.list():
        if "gemini" in m.name:
            print(f"AVAILABLE MODEL: {m.name}")
            found_any = True 


    if not found_any:
        print("CONNECTED, BUT NO GEMINI MODELS FOUND.")

except Exception as e:
    print(f"FATAL ERROR: {e}")