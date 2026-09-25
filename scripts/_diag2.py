import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


for word in ["hello", "altogether", "pastry"]:
    print(f"=== dictionaryapi.dev: {word} (attempt) ===")
    try:
        print(get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")[:1200])
    except Exception as e:
        print("ERROR:", e)
    print()
