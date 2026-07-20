import json
import requests

def search_wikipedia(query):
    """ Search Wikipedia and return a summary."""

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return json.dumps({
                "title": data.get("title", ""),
                "summary": data.get("extract", "NO summary found")[:8000]
            })
        return json.dumps({
            "error": f"Page not found for '{query}'. try a different term"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})