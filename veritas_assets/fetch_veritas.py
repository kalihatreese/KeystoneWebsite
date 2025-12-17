import json
with open("all_voices.json","r") as f:
    data=json.load(f)
voices_list = data.get("voices") if isinstance(data,dict) else data
veritas_voice = next((v for v in voices_list if isinstance(v,dict) and v.get("name","")=="Veritas"), None)
print(json.dumps(veritas_voice, indent=4) if veritas_voice else "No Veritas voice found.")
