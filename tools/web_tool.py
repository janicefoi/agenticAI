import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def web_tool(query: str):
    """
    Perform a real web search using Serper.dev API.
    """
    if not SERPER_API_KEY:
        print("[WEB TOOL] Missing SERPER_API_KEY, returning mock result.")
        return [{"title": "Mock result", "snippet": "No API key provided.", "url": ""}]

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 3}  # fetch 3 results

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "organic" not in data:
        return [{"title": "No results", "snippet": "Could not retrieve data", "url": ""}]

    results = []
    for item in data["organic"][:3]:
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link"),
        })

    return results
