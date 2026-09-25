import json
import urllib.error
import urllib.request

d = json.load(open("data/news.json"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def probe(url, headers):
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print("  status:", resp.status)
            for k in ["Content-Type", "Content-Length", "Access-Control-Allow-Origin", "Accept-Ranges", "Location"]:
                if resp.headers.get(k):
                    print(f"  {k}:", resp.headers.get(k))
    except urllib.error.HTTPError as e:
        print("  HTTPError:", e.code, e.reason)
        print("  body:", e.read(300))
    except Exception as e:
        print("  ERROR:", e)


for p in d["programs"]:
    if not p["items"] or not p["items"][0].get("audio"):
        continue
    url = p["items"][0]["audio"]
    print("===", p["id"], "->", url)
    print(" -- no referer, browser UA --")
    probe(url, {"User-Agent": UA})
    print(" -- with referer = source site --")
    probe(url, {"User-Agent": UA, "Referer": p["source_url"]})
    print(" -- with referer = github pages (simulating our app) --")
    probe(url, {"User-Agent": UA, "Referer": "https://nguyenbm1979.github.io/LearnEnghlish/"})
    print()
