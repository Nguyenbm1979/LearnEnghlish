import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"
url = "https://www.newsinlevels.com/products/are-you-dead-app-level-2/"
req = urllib.request.Request(url, headers={"User-Agent": UA})
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")

# look for soundcloud iframe / player URLs
for m in re.finditer(r'(https?://(?:w\.)?soundcloud\.com/[^"\'\s]+)', html):
    print("SC URL:", m.group(1))

for m in re.finditer(r'<iframe[^>]*soundcloud[^>]*>', html):
    print("IFRAME:", m.group(0)[:400])

print("--- any api.soundcloud.com/tracks ref ---")
for m in re.finditer(r'api\.soundcloud\.com/tracks/\d+', html):
    print(m.group(0))
