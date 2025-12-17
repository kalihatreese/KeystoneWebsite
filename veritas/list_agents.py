#!/usr/bin/env python3
import os, requests
from dotenv import load_dotenv

load_dotenv()  # loads ELEVENLABS_KEY from .env

API_KEY = os.getenv("ELEVENLABS_KEY")
if not API_KEY:
    raise RuntimeError("ELEVENLABS_KEY not found")

resp = requests.get(
    "https://api.elevenlabs.io/v1/convai/agents",
    headers={"xi-api-key": API_KEY}
)

print("Status:", resp.status_code)
print(resp.json())
