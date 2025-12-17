import os
import requests
import json

ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
url = "https://api.elevenlabs.io/v1/voices"
headers = {"xi-api-key": ELEVENLABS_KEY}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    voices = response.json()
    with open("all_voices.json", "w") as f:
        json.dump(voices, f, indent=4)
    print("[✓] Saved all voices to all_voices.json")
else:
    print(f"[!] Error {response.status_code}: {response.text}")
