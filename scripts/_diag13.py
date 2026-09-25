import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


print("=== Wikimedia Commons: check reachability + a classic fairy tale image category ===")
try:
    html_ = fetch("https://commons.wikimedia.org/wiki/Category:Three_Little_Pigs")
    print("OK, length:", len(html_))
    imgs = re.findall(r'src="(//upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png))"', html_, re.IGNORECASE)
    print("sample images:", imgs[:5])
except Exception as e:
    print("ERROR:", e)

print()
print("=== unite for literacy books-cloud probe ===")
for url in [
    "https://books-cloud.uniteforliteracy.com/",
    "https://www.uniteforliteracy.com/api/books",
    "https://www.uniteforliteracy.com/books",
]:
    print(f"--- {url} ---")
    try:
        html_ = fetch(url)
        print("OK, length:", len(html_), "snippet:", html_[:200].replace(chr(10), " "))
    except Exception as e:
        print("ERROR:", e)
