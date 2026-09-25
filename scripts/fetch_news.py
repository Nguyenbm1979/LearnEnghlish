#!/usr/bin/env python3
"""Fetch real English-news RSS feeds (VOA Learning English, Breaking News
English, News in Levels) and write data/news.json.

Standard-library only (urllib + xml.etree) so it needs no pip install on
the GitHub Actions runner.
"""
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# VOA Learning English's own "podcast" RSS feeds. Note: as of this writing
# these haven't published a new episode since around March 2025 (VOA's
# 2025 funding/staffing disruption) — kept here because the content and
# audio are still real and the workflow will pick up new episodes the
# moment VOA resumes publishing, with zero code changes needed.
VOA_PROGRAMS = [
    {"id": "voa-news", "name": "VOA: Tin tức & Chuyện đời sống Mỹ", "zone_id": 1689},
    {"id": "everyday-grammar", "name": "VOA: Everyday Grammar (Ngữ pháp)", "zone_id": 4456},
    {"id": "words-stories", "name": "VOA: Words and Their Stories (Thành ngữ)", "zone_id": 987},
    {"id": "as-it-is", "name": "VOA: As It Is (Thời sự)", "zone_id": 3521},
]
VOA_FEED_URL = "https://learningenglish.voanews.com/podcast/?zoneId={zone_id}&format=RSS"

OTHER_FEEDS = [
    {
        "id": "breaking-news-english",
        "name": "Breaking News English (tin thật, audio thật, đa cấp độ)",
        "url": "https://breakingnewsenglish.com/bne.xml",
        "source_url": "https://breakingnewsenglish.com/",
        "require_audio": True,
        "strip_wp_boilerplate": False,
    },
    {
        "id": "news-in-levels",
        "name": "News in Levels (tin hằng ngày, 3 cấp độ đọc)",
        "url": "https://www.newsinlevels.com/feed/",
        "source_url": "https://www.newsinlevels.com/",
        "require_audio": False,
        "strip_wp_boilerplate": True,
    },
]

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


def parse_feed(xml_bytes, require_audio, strip_wp_boilerplate=False):
    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")
    if channel is None:
        return []
    ns_itunes = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
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
        items.append({
            "title": title,
            "link": link,
            "pubDate": pub_date,
            "summary": description,
            "audio": audio_url or "",
            "duration": duration.strip() if duration else "",
        })
    return items


def fetch_program(url, require_audio, strip_wp_boilerplate=False):
    xml_bytes = fetch(url)
    return parse_feed(xml_bytes, require_audio, strip_wp_boilerplate)


def main():
    programs_out = []
    any_success = False

    for prog in VOA_PROGRAMS:
        url = VOA_FEED_URL.format(zone_id=prog["zone_id"])
        try:
            items = fetch_program(url, require_audio=True)
        except (urllib.error.URLError, ET.ParseError, TimeoutError, OSError) as e:
            print(f"WARN: failed to fetch/parse {prog['id']} ({url}): {e}", file=sys.stderr)
            items = []
        if items:
            any_success = True
        programs_out.append({
            "id": prog["id"],
            "name": prog["name"],
            "source_url": f"https://learningenglish.voanews.com/podcast/?zoneId={prog['zone_id']}",
            "items": items,
        })

    for feed in OTHER_FEEDS:
        try:
            items = fetch_program(
                feed["url"],
                require_audio=feed["require_audio"],
                strip_wp_boilerplate=feed["strip_wp_boilerplate"],
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
        "source": "VOA Learning English, Breaking News English, News in Levels",
        "programs": programs_out,
    }

    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total_items = sum(len(p["items"]) for p in programs_out)
    print(f"Wrote data/news.json with {total_items} items across {len(programs_out)} programs.")


if __name__ == "__main__":
    main()
