#!/usr/bin/env python3
"""Fetch real VOA Learning English RSS feeds and write data/voa-news.json.

Standard-library only (urllib + xml.etree) so it needs no pip install
on the GitHub Actions runner.
"""
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

PROGRAMS = [
    {"id": "voa-news", "name": "Tin tức & Chuyện đời sống Mỹ", "zone_id": 1689},
    {"id": "everyday-grammar", "name": "Everyday Grammar (Ngữ pháp)", "zone_id": 4456},
    {"id": "words-stories", "name": "Words and Their Stories (Thành ngữ)", "zone_id": 987},
    {"id": "as-it-is", "name": "As It Is (Thời sự)", "zone_id": 3521},
]

FEED_URL = "https://learningenglish.voanews.com/podcast/?zoneId={zone_id}&format=RSS"
ITEMS_PER_PROGRAM = 8
TIMEOUT = 20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0; "
                  "+https://github.com/Nguyenbm1979/learnenghlish)",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text):
    if not text:
        return ""
    text = TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def parse_feed(xml_bytes):
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
            item.findtext("description", "") or item.findtext("summary", "")
        )
        if len(description) > 400:
            description = description[:397].rstrip() + "..."
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        duration = item.findtext(f"{ns_itunes}duration", "")
        if not title or not audio_url:
            continue
        items.append({
            "title": title,
            "link": link,
            "pubDate": pub_date,
            "summary": description,
            "audio": audio_url,
            "duration": duration.strip() if duration else "",
        })
    return items


def main():
    programs_out = []
    any_success = False
    for prog in PROGRAMS:
        url = FEED_URL.format(zone_id=prog["zone_id"])
        try:
            xml_bytes = fetch(url)
            items = parse_feed(xml_bytes)
        except (urllib.error.URLError, ET.ParseError, TimeoutError) as e:
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

    if not any_success:
        print("ERROR: every VOA feed failed, refusing to overwrite existing data file", file=sys.stderr)
        sys.exit(1)

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "VOA Learning English (learningenglish.voanews.com)",
        "programs": programs_out,
    }

    with open("data/voa-news.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total_items = sum(len(p["items"]) for p in programs_out)
    print(f"Wrote data/voa-news.json with {total_items} items across {len(programs_out)} programs.")


if __name__ == "__main__":
    main()
