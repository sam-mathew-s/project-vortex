import os 
from google import genai
from dotenv import load_dotenv 

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

text = "I am Warrior."

# Google to turn this text into number(Embeddings)
result = client.models.embed_content(
    model="text-embedding-004",
    contents=text,
)

# Get the list of number
vector = result.embeddings[0].values

print(f"TEXT: '{text}'")
print(f"TOTAL NUMBERS (DIMENSIONS): {len(vector)}")
print(f"FIRST 10 NUMBERS: {vector[:10]}")

