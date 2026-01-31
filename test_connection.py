import os 
import httpx
from dotenv import load_dotenv

# Load the keys from the safe (.env)
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Define the Target (the expriment table)
endpoint = f"{url}/rest/v1/experiments"

# Define the headers
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation" # this asks supabase to send back data
}

# The message payload
payload = {
    "message": "hello from Sam's Laptop via Python!"
}

# Fire the laser (Post Request)
print("--- INITIATING UPLOAD ---")
try:
    response = httpx.post(endpoint, headers=headers, json=payload)

    if response.status_code == 201:
        print("SUCESS: Data uploaded successfully!")
        print("Server Replied:", response.json())
    else:
        print("Failed to upload data.")
        print("Error Code:", response.status_code)
        print("Reason:", response.text)

except Exception as e:
    print("CRITICAL ERROR:",e)

print("-----------------------------")
