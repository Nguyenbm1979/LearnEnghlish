import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


print("=== usahello.org homepage probe ===")
try:
    html = fetch("https://usahello.org/")
    print("OK, length:", len(html))
    print("has 'Learn English' link:", "learn-english" in html.lower() or "learn english" in html.lower())
    for m in re.finditer(r'href="([^"]*rss[^"]*)"', html, re.IGNORECASE):
        print("rss link found:", m.group(1))
    for m in re.finditer(r'href="([^"]*feed[^"]*)"', html, re.IGNORECASE):
        print("feed link found:", m.group(1))
except Exception as e:
    print("ERROR:", e)

print()
print("=== usahello.org/feed/ ===")
try:
    xml = fetch("https://usahello.org/feed/")
    print("OK, length:", len(xml))
    titles = re.findall(r"<title>([^<]*)</title>", xml)[:5]
    print("titles:", titles)
except Exception as e:
    print("ERROR:", e)

print()
print("=== News in Levels: re-check for image in content:encoded ===")
try:
    html = fetch("https://www.newsinlevels.com/products/are-you-dead-app-level-2/")
    imgs = re.findall(r'<img[^>]*src="([^"]+)"[^>]*>', html)
    print("images found on article page:", imgs[:5])
except Exception as e:
    print("ERROR:", e)

print()
print("=== BBC 6 Minute English: full first item dump ===")
try:
    xml = fetch("https://podcasts.files.bbci.co.uk/p02pc9tn.rss")
    first_item = xml.split("<item>")[2].split("</item>")[0]
    print(first_item[:1500])
except Exception as e:
    print("ERROR:", e)
