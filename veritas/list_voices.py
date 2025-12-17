import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_KEY")

# API endpoint to list voices
url = "https://api.elevenlabs.io/v1/voices"

headers = {
    "xi-api-key": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    voices = response.json().get("voices", [])
    for v in voices:
        print(f"Voice Name: {v['name']}, Voice ID: {v['voice_id']}")
else:
    print(f"Error {response.status_code}: {response.text}")
