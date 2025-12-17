import os, requests, json

ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")  # make sure it's set
VOICE_NAME = "Veritas"
TEXT = "Hello, this is Veritas speaking through the ElevenLabs API."

# Get voices
voices = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": ELEVENLABS_KEY}).json()
voice_data = next((v for v in voices.get("voices", []) if v.get("name") == VOICE_NAME), None)

if not voice_data:
    print("Veritas voice not found!")
    exit(1)

voice_id = voice_data["voice_id"]
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
payload = {"text": TEXT, "voice_settings": {"stability":0.75,"similarity_boost":0.75}}
resp = requests.post(url, headers={"xi-api-key": ELEVENLABS_KEY,"Content-Type":"application/json"}, json=payload)

if resp.status_code == 200:
    with open("veritas.mp3", "wb") as f:
        f.write(resp.content)
    print("[✓] Veritas audio saved as veritas.mp3")
else:
    print(f"[!] Error {resp.status_code}: {resp.text}")
