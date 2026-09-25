import sys
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (compatible; LearnEnglishAppBot/1.0)"


def dump(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=20).read()
    root = ET.fromstring(data)
    item = root.find("./channel/item")
    print(ET.tostring(item, encoding="unicode"))


if __name__ == "__main__":
    print("=== breakingnewsenglish raw (first item) ===")
    dump("https://breakingnewsenglish.com/bne.xml")
    print("=== newsinlevels raw (first item) ===")
    dump("https://www.newsinlevels.com/feed/")
