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
        f"&gsrsearch={q}&gsrnamespace=6&gsrlimit=4&prop=imageinfo&iiprop=url"
        "&iiurlwidth=800&format=json"
    )
    data = json.loads(fetch(url))
    pages = data.get("query", {}).get("pages", {})
    return [
        {"title": p.get("title"), "thumburl": p.get("imageinfo", [{}])[0].get("thumburl")}
        for p in pages.values()
    ]


queries = [
    "Three Little Pigs Rackham",
    "Ugly Duckling Andersen illustration",
    "Hansel and Gretel Rackham",
    "Puss in Boots Rackham",
    "Jack and the Beanstalk illustration",
    "Snow White Rackham",
]
for q in queries:
    print(f"=== {q} ===")
    try:
        for r in search_commons_image(q):
            if r["thumburl"]:
                print(" ", r["title"], "->", r["thumburl"])
    except Exception as e:
        print("ERROR:", e)
    print()
