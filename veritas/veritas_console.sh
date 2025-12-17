#!/bin/bash

ELEVENLABS_KEY="$(grep -E '^ELEVENLABS_KEY=' ~/shadowx_installed/.env | cut -d'=' -f2- | tr -d '"')";
OPENAI_API_KEY="$(grep -E '^OPENAI_API_KEY=' ~/shadowx_installed/.env | cut -d'=' -f2- | tr -d '"')";

VOICE_ID="WPtXPWDQ7bbXaHrgjCcW";
MODEL_ID="eleven_multilingual_v2";
STABILITY=0.65;
SIMILARITY=0.75;
STYLE=0.12;
SPEED=0.85;

FINAL_OUTPUT_FILE="$HOME/shadowx_installed/veritas_reply.mp3"
TEMP_OUTPUT_FILE="$HOME/shadowx_installed/veritas_reply.mp3.tmp"

echo "--- Veritas AI Console Initialized ---"
echo "Veritas is online."
echo "----------------------------------------"

while true; do
  read -p "You: " USER_TEXT
  [ -z "$USER_TEXT" ] && break

  SYSTEM_PROMPT="You are Veritas, the ShadowX AI with ReeseEffect tone and absolute clarity."

  AI_REPLY=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"gpt-4o-mini\",\"messages\":[{\"role\":\"system\",\"content\":\"$SYSTEM_PROMPT\"},{\"role\":\"user\",\"content\":\"$USER_TEXT\"}]}" \
    | jq -r '.choices[0].message.content // "..."')

  echo "Veritas: $AI_REPLY"

  TTS_PAYLOAD="{\"text\":\"$AI_REPLY\",\"model_id\":\"$MODEL_ID\",\"voice_settings\":{\"stability\":$STABILITY,\"similarity_boost\":$SIMILARITY,\"style\":$STYLE,\"speed\":$SPEED}}"

  curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
       -H "xi-api-key: $ELEVENLABS_KEY" \
       -H "Content-Type: application/json" \
       -d "$TTS_PAYLOAD" \
       --output "$TEMP_OUTPUT_FILE"

  mv "$TEMP_OUTPUT_FILE" "$FINAL_OUTPUT_FILE"
  mpv --no-video "$FINAL_OUTPUT_FILE" > /dev/null 2>&1

done

echo "----------------------------------------"
echo "Veritas Console shutting down."
