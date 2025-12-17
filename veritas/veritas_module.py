#!/usr/bin/env python3
"""
Veritas Voice Module for Keystone Trinity
- Plays final polished voice and supports dynamic ElevenLabs TTS
"""

import subprocess
import os

ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
VOICE_ID = "WPtXPWDQ7bbXaHrgjCcW"
MODEL_ID = "eleven_multilingual_v2"
DEFAULT_AUDIO = "veritas_final.mp3"

STABILITY = 0.65
SIMILARITY = 0.75
STYLE = 0.12
SPEED = 0.85

def play_audio(file_path: str):
    try:
        subprocess.run(["mpv", file_path], check=True)
    except:
        try:
            subprocess.run(["termux-media-player", "play", file_path], check=True)
        except:
            try:
                subprocess.run(["play", file_path], check=True)
            except:
                print(f"Saved {file_path} — play it on PC/phone.")

def speak(text: str, output_file: str = "veritas_temp.mp3"):
    import json
    import requests

    if not ELEVENLABS_KEY:
        raise ValueError("ELEVENLABS_KEY not set in environment")

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": STABILITY,
            "similarity_boost": SIMILARITY,
            "style": STYLE,
            "speed": SPEED
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        play_audio(output_file)
    else:
        print(f"Error generating TTS: {response.status_code} {response.text}")

if __name__ == "__main__":
    print("✅ Playing default Veritas voice...")
    play_audio(DEFAULT_AUDIO)
