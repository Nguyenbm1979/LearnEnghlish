import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


print("=== storynory.com/feed/ ===")
try:
    xml = fetch("https://www.storynory.com/feed/")
    print("OK, length:", len(xml))
    titles = re.findall(r"<title>([^<]*)</title>", xml)[:5]
    print("titles:", titles)
    first_item = xml.split("<item>")[1].split("</item>")[0] if "<item>" in xml else ""
    for tag in ["enclosure", "itunes:image", "media:thumbnail"]:
        m = re.findall(rf'<{re.escape(tag)}[^>]*>', first_item, re.IGNORECASE)
        if m:
            print(f"  {tag}:", m[:2])
except Exception as e:
    print("ERROR:", e)

print()
print("=== learnenglishkids.britishcouncil.org homepage ===")
try:
    html_ = fetch("https://learnenglishkids.britishcouncil.org/short-stories")
    print("OK, length:", len(html_))
    for m in re.finditer(r'href="([^"]*rss[^"]*)"', html_, re.IGNORECASE):
        print("rss link:", m.group(1))
except Exception as e:
    print("ERROR:", e)

print()
print("=== uniteforliteracy.com homepage ===")
try:
    html_ = fetch("https://www.uniteforliteracy.com/")
    print("OK, length:", len(html_))
except Exception as e:
    print("ERROR:", e)

print()
print("=== storyberries.com/feed/ ===")
try:
    xml = fetch("https://www.storyberries.com/feed/")
    print("OK, length:", len(xml))
    titles = re.findall(r"<title>([^<]*)</title>", xml)[:5]
    print("titles:", titles)
except Exception as e:
    print("ERROR:", e)
