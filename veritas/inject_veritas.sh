#!/bin/bash
# This script will trigger Veritas TTS generation

PROMPT="Who am I?"
OUTPUT="veritas.mp3"

# Run Python snippet to generate TTS
python3 - <<PYTHON
from veritas_tts import tts

audio = tts.generate("$PROMPT")
audio.save("$OUTPUT")
print("Veritas audio saved to $OUTPUT")
PYTHON
