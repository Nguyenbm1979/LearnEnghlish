import re
import urllib.request

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")


OG_RE = re.compile(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', re.IGNORECASE)

pages = {
    "news-in-levels": "https://www.newsinlevels.com/products/are-you-dead-app-level-2/",
    "breaking-news-english": "https://breakingnewsenglish.com/2609/260924-toys-r-us.html",
}
for name, url in pages.items():
    print(f"=== {name} og:image ===")
    try:
        html = fetch(url)
        m = OG_RE.search(html)
        print(m.group(1) if m else "not found")
    except Exception as e:
        print("ERROR:", e)
    print()

print("=== BBC 6min english mp3 redirect check ===")
try:
    req = urllib.request.Request(
        "http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download-rss-low/proto/http/vpid/p0pc618w.mp3",
        headers={"User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        print("final url:", resp.geturl())
        print("status:", resp.status)
        print("content-type:", resp.headers.get("Content-Type"))
        print("content-length:", resp.headers.get("Content-Length"))
except Exception as e:
    print("ERROR:", e)
