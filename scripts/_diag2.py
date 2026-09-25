import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


print("=== dictionaryapi.dev: altogether ===")
try:
    print(get("https://api.dictionaryapi.dev/api/v2/entries/en/altogether")[:1500])
except Exception as e:
    print("ERROR:", e)

print("\n=== dictionaryapi.dev: pastries (plural, may miss) ===")
try:
    print(get("https://api.dictionaryapi.dev/api/v2/entries/en/pastries")[:1500])
except Exception as e:
    print("ERROR:", e)

print("\n=== google translate free endpoint: sentence EN->VI ===")
try:
    q = urllib.parse.quote("Can I get a medium iced latte with oat milk, please?")
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q={q}"
    print(get(url)[:1500])
except Exception as e:
    print("ERROR:", e)

print("\n=== google translate free endpoint: single word EN->VI ===")
try:
    q = urllib.parse.quote("altogether")
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q={q}"
    print(get(url)[:500])
except Exception as e:
    print("ERROR:", e)
