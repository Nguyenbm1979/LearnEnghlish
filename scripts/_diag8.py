import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


feeds = {
    "breaking-news-english": "https://breakingnewsenglish.com/bne.xml",
    "news-in-levels": "https://www.newsinlevels.com/feed/",
    "voa-news": "https://learningenglish.voanews.com/podcast/?zoneId=1689&format=RSS",
}

for name, url in feeds.items():
    print(f"=== {name} ===")
    try:
        xml = fetch(url)
    except Exception as e:
        print("  ERROR:", e)
        continue
    first_item = xml.split("<item>")[1].split("</item>")[0] if "<item>" in xml else xml[:3000]
    for tag in ["media:thumbnail", "media:content", "enclosure", "itunes:image", "<img", "thumbnail"]:
        matches = re.findall(rf'<{re.escape(tag)}[^>]*>', first_item, re.IGNORECASE) if not tag.startswith("<img") else re.findall(r'<img[^>]*>', first_item, re.IGNORECASE)
        if matches:
            print(f"  {tag}: {matches[:2]}")
    print()

print("### Candidate new sources ###")
candidates = {
    "bbc-learning-english": "https://www.bbc.co.uk/learningenglish/english/course/lower-intermediate/rss.xml",
    "bbc-6min-english": "https://podcasts.files.bbci.co.uk/p02pc9tn.rss",
    "britishcouncil": "https://learnenglish.britishcouncil.org/rss.xml",
}
for name, url in candidates.items():
    print(f"=== {name} ({url}) ===")
    try:
        xml = fetch(url)
        print("  OK, length:", len(xml))
        titles = re.findall(r"<title>([^<]*)</title>", xml)[:4]
        print("  titles:", titles)
        first_item = xml.split("<item>")[1].split("</item>")[0] if "<item>" in xml else ""
        for tag in ["media:thumbnail", "enclosure", "itunes:image", "<img"]:
            matches = re.findall(rf'<{re.escape(tag)}[^>]*>', first_item, re.IGNORECASE) if not tag.startswith("<img") else re.findall(r'<img[^>]*>', first_item, re.IGNORECASE)
            if matches:
                print(f"  {tag}: {matches[:2]}")
    except Exception as e:
        print("  ERROR:", e)
    print()
