from flask import Flask, render_template, request, jsonify, send_file
import os

app = Flask(__name__)

# The Crime Log path
LOG_FILE = "crime_log.txt"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    msg = request.json.get('message', '')
    
    # PERIOD PROTOCOL ENFORCEMENT
    if "." not in msg:
        with open(LOG_FILE, "a") as f:
            f.write(f"[CRIME DETECTED] Input '{msg}' blocked. Integrity failed.\n")
        return jsonify({"text": "ACCESS DENIED: Period missing.", "voice": False})

    # Successful stewardship
    response_text = "Integrity verified. Veritas is listening, Steward."
    
    # Trigger your TTS script
    os.system(f"python3 veritas_tts.py '{response_text}'")
    
    with open(LOG_FILE, "a") as f:
        f.write(f"[STRESS PASS] Input accepted: {msg}\n")
        
    return jsonify({"text": response_text, "voice": True})

@app.route('/voice')
def voice():
    return send_file('veritas_reply.mp3')

@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE): return ""
    with open(LOG_FILE, "r") as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
