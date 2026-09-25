import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


def search_commons_image(query):
    q = urllib.parse.quote(query)
    url = (
        "https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={q}&gsrnamespace=6&gsrlimit=3&prop=imageinfo&iiprop=url|extmetadata"
        "&iiurlwidth=800&format=json"
    )
    data = json.loads(fetch(url))
    pages = data.get("query", {}).get("pages", {})
    results = []
    for p in pages.values():
        info = p.get("imageinfo", [{}])[0]
        results.append({
            "title": p.get("title"),
            "thumburl": info.get("thumburl"),
            "url": info.get("url"),
        })
    return results


queries = [
    "Three Little Pigs illustration",
    "Cinderella illustration",
    "Tortoise and the Hare illustration",
    "Little Red Riding Hood illustration",
    "Ugly Duckling illustration",
    "Goldilocks illustration",
]
for q in queries:
    print(f"=== {q} ===")
    try:
        for r in search_commons_image(q):
            print(" ", r["title"], "->", r["thumburl"])
    except Exception as e:
        print("ERROR:", e)
    print()
