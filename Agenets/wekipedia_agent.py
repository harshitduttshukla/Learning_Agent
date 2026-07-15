from asyncio import timeout
from httpcore import request
def search_wikipedia(query):
    """ Search Wikipedia and return a summary."""

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    try:
        r = request.get(url,timeout=10)
        if r.status_code == 200:
            data  = r.json()
            return json.dumps({
                "title": data.get("title",""),
                "summary": data.get("extract","NO summary found")[:8000]
            })
        return json.dumps({
            "error":f"Page not found for '{query}'. try a different term"
        })
    except Exception as e:
        return json.dumps({"error":str(e)})