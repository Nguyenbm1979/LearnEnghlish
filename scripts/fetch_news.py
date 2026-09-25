#!/usr/bin/env python3
"""Fetch real English-news RSS feeds (Breaking News English, News in
Levels) and write data/news.json.

Standard-library only (urllib + xml.etree) so it needs no pip install on
the GitHub Actions runner.

Note: VOA Learning English and BBC Learning English were tried and
dropped — both learningenglish.voanews.com and bbc.co.uk (including
their audio CDNs) are blocked on Vietnamese networks, confirmed with a
real user there. Keeping only sources whose website AND audio both
work end-to-end from Vietnam.
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Server-side translation so every visitor sees Vietnamese without needing
# their own API key. Uses the free, unofficial Google Translate endpoint
# (no key required) — set SKIP_TRANSLATE=1 to skip during local testing.
TRANSLATE_ENABLED = os.environ.get("SKIP_TRANSLATE") != "1"
TRANSLATE_DELAY_SECONDS = 0.2

FEEDS = [
    {
        "id": "breaking-news-english",
        "name": "Breaking News English (tin thật, audio thật, đa cấp độ)",
        "url": "https://breakingnewsenglish.com/bne.xml",
        "source_url": "https://breakingnewsenglish.com/",
        "require_audio": True,
        "strip_wp_boilerplate": False,
        "fetch_og_image": True,
    },
    {
        "id": "news-in-levels",
        "name": "News in Levels (tin hằng ngày, 3 cấp độ đọc)",
        "url": "https://www.newsinlevels.com/feed/",
        "source_url": "https://www.newsinlevels.com/",
        "require_audio": False,
        "strip_wp_boilerplate": True,
        "fetch_soundcloud_embed": True,
        "fetch_og_image": True,
    },
]

SOUNDCLOUD_IFRAME_RE = re.compile(r'<iframe[^>]*\bsrc="(https://w\.soundcloud\.com/player/\?[^"]+)"[^>]*>')
OG_IMAGE_RE = re.compile(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', re.IGNORECASE)


def extract_soundcloud_embed(article_url):
    """News in Levels articles embed real audio via a SoundCloud widget
    (not exposed in their RSS enclosure) — scrape it from the article page."""
    try:
        page_html = fetch(article_url).decode("utf-8", "replace")
        m = SOUNDCLOUD_IFRAME_RE.search(page_html)
        return html.unescape(m.group(1)) if m else ""
    except Exception as e:
        print(f"WARN: soundcloud embed lookup failed for {article_url}: {e}", file=sys.stderr)
        return ""


def extract_og_image(article_url):
    """Feeds without a usable image tag (Breaking News English, News in
    Levels) still have a real article photo via the standard og:image meta
    tag on the article page itself."""
    try:
        page_html = fetch(article_url).decode("utf-8", "replace")
        m = OG_IMAGE_RE.search(page_html)
        return html.unescape(m.group(1)) if m else ""
    except Exception as e:
        print(f"WARN: og:image lookup failed for {article_url}: {e}", file=sys.stderr)
        return ""

ITEMS_PER_PROGRAM = 8
TIMEOUT = 20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0; "
                  "+https://github.com/Nguyenbm1979/learnenghlish)",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

TAG_RE = re.compile(r"<[^>]+>")
WP_BOILERPLATE_RE = re.compile(r"\s*The post .*$", re.DOTALL)


def strip_html(text, strip_wp_boilerplate=False):
    if not text:
        return ""
    if strip_wp_boilerplate:
        text = WP_BOILERPLATE_RE.sub("", text)
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 400:
        text = text[:397].rstrip() + "..."
    return text


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def translate_to_vi(text):
    if not TRANSLATE_ENABLED or not text:
        return ""
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q={q}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        segments = data[0] if data and data[0] else []
        translated = "".join(seg[0] for seg in segments if seg and seg[0])
        time.sleep(TRANSLATE_DELAY_SECONDS)
        return translated
    except Exception as e:
        print(f"WARN: translate failed for {text[:60]!r}: {e}", file=sys.stderr)
        return ""


def parse_feed(xml_bytes, require_audio, strip_wp_boilerplate=False, fetch_soundcloud=False, fetch_og_image=False):
    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")
    if channel is None:
        return []
    ns_itunes = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
    channel_image_el = channel.find(f"{ns_itunes}image")
    channel_image = channel_image_el.get("href") if channel_image_el is not None else ""
    items = []
    for item in channel.findall("item")[:ITEMS_PER_PROGRAM]:
        title = strip_html(item.findtext("title", ""))
        link = (item.findtext("link", "") or "").strip()
        pub_date = (item.findtext("pubDate", "") or "").strip()
        description = strip_html(
            item.findtext("description", "") or item.findtext("summary", ""),
            strip_wp_boilerplate=strip_wp_boilerplate,
        )
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        duration = item.findtext(f"{ns_itunes}duration", "")
        if not title or (require_audio and not audio_url):
            continue
        embed_url = extract_soundcloud_embed(link) if (fetch_soundcloud and link) else ""
        item_image_el = item.find(f"{ns_itunes}image")
        image_url = item_image_el.get("href") if item_image_el is not None else channel_image
        if not image_url and fetch_og_image and link:
            image_url = extract_og_image(link)
        items.append({
            "title": title,
            "title_vi": translate_to_vi(title),
            "link": link,
            "pubDate": pub_date,
            "summary": description,
            "summary_vi": translate_to_vi(description),
            "audio": audio_url or "",
            "embed": embed_url,
            "image": image_url or "",
            "duration": duration.strip() if duration else "",
        })
    return items


def fetch_program(url, require_audio, strip_wp_boilerplate=False, fetch_soundcloud=False, fetch_og_image=False):
    xml_bytes = fetch(url)
    return parse_feed(xml_bytes, require_audio, strip_wp_boilerplate, fetch_soundcloud, fetch_og_image)


def main():
    programs_out = []
    any_success = False

    for feed in FEEDS:
        try:
            items = fetch_program(
                feed["url"],
                require_audio=feed["require_audio"],
                strip_wp_boilerplate=feed["strip_wp_boilerplate"],
                fetch_soundcloud=feed.get("fetch_soundcloud_embed", False),
                fetch_og_image=feed.get("fetch_og_image", False),
            )
        except (urllib.error.URLError, ET.ParseError, TimeoutError, OSError) as e:
            print(f"WARN: failed to fetch/parse {feed['id']} ({feed['url']}): {e}", file=sys.stderr)
            items = []
        if items:
            any_success = True
        programs_out.append({
            "id": feed["id"],
            "name": feed["name"],
            "source_url": feed["source_url"],
            "items": items,
        })

    if not any_success:
        print("ERROR: every feed failed, refusing to overwrite existing data file", file=sys.stderr)
        sys.exit(1)

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Breaking News English, News in Levels",
        "programs": programs_out,
    }

    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total_items = sum(len(p["items"]) for p in programs_out)
    print(f"Wrote data/news.json with {total_items} items across {len(programs_out)} programs.")


if __name__ == "__main__":
    main()
