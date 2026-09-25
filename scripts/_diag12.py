import re
import time
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


print("=== storynory retry ===")
for attempt in range(2):
    try:
        xml = fetch("https://www.storynory.com/feed/")
        print("OK, length:", len(xml))
        break
    except Exception as e:
        print("ERROR:", e)
        time.sleep(2)

print()
print("=== British Council Kids short-stories: find story links ===")
try:
    html_ = fetch("https://learnenglishkids.britishcouncil.org/short-stories")
    links = re.findall(r'href="(/short-stories/[^"]+)"', html_)
    links = list(dict.fromkeys(links))
    print("story links found:", links[:10])
except Exception as e:
    print("ERROR:", e)

print()
print("=== British Council: probe one story page ===")
try:
    html_ = fetch("https://learnenglishkids.britishcouncil.org/short-stories/the-three-little-pigs")
    print("length:", len(html_))
    print("has audio tag:", "<audio" in html_)
    print("has mp3 ref:", ".mp3" in html_)
    imgs = re.findall(r'<img[^>]*src="([^"]+)"', html_)
    print("images:", [i for i in imgs if "story" in i.lower() or "sites/kids" in i.lower()][:5])
    mp3s = re.findall(r'"([^"]+\.mp3)"', html_)
    print("mp3 links:", mp3s[:5])
except Exception as e:
    print("ERROR:", e)

print()
print("=== Unite for Literacy: probe structure ===")
try:
    html_ = fetch("https://www.uniteforliteracy.com/")
    print("title:", re.search(r"<title>([^<]*)</title>", html_).group(1) if re.search(r"<title>([^<]*)</title>", html_) else None)
    for m in re.finditer(r'href="([^"]*book[^"]*)"', html_, re.IGNORECASE):
        print("book link:", m.group(1))
except Exception as e:
    print("ERROR:", e)
