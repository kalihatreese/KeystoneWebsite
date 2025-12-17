#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
if not ELEVENLABS_KEY:
    raise Exception("ELEVENLABS_KEY not found in .env")

TEXT_TO_SPEAK = "Hello, I am Veritas. The truth is my frequency."
AGENT_ID = "agent_7901kc5p7s26epkbpcq2wn3r6phx"
url = f"https://api.elevenlabs.io/v1/agents/{AGENT_ID}/speak"
headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
data = {"text": TEXT_TO_SPEAK}

response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    with open("veritas.mp3", "wb") as f:
        f.write(response.content)
    print("[✓] Audio generated successfully: veritas.mp3")
else:
    print(f"[!] Error {response.status_code}: {response.json()}")
