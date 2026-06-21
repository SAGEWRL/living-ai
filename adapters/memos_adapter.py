# adapters/memos_adapter.py

import requests
from core.event_bus import bus

URL = "https://memos-api-ahnh.onrender.com/analyze_text"

def memos_adapter(text):
    try:
        r = requests.post(URL, data={"text": text})
        return {"memos": r.json()}
    except Exception as e:
        return {"memos_error": str(e)}

bus.subscribe("input", memos_adapter)