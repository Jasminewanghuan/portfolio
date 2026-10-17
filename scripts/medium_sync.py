"""Import new Medium articles into _posts/.

Reads the Medium RSS feed, and for every article not already on the site
(matched by its Medium link) writes _posts/YYYY-MM-DD-slug.md with the full
article, a short summary and a link back to Medium. Existing posts are never
changed, so edits made in Pages CMS are kept.

Usage: python3 scripts/medium_sync.py [feed-url-or-local-file]
"""
import email.utils
import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = os.environ.get("MEDIUM_FEED", "https://medium.com/feed/@hw2769")
POSTS_DIR = "_posts"
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def fetch(source):
    if os.path.exists(source):
        with open(source, "rb") as f:
            return f.read()
    req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0 (portfolio-sync)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def clean_link(url):
    return url.split("?")[0].strip()


def existing_links():
    links = set()
    if not os.path.isdir(POSTS_DIR):
        return links
    for name in os.listdir(POSTS_DIR):
        with open(os.path.join(POSTS_DIR, name), encoding="utf-8") as f:
            m = re.search(r'^medium_url:\s*"?([^"\n]+)"?', f.read(), re.M)
        if m:
            links.add(clean_link(m.group(1)))
    return links


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60].rstrip("-") or "article"


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def tidy_body(body, title):
    # Drop Medium's tracking pixel.
    body = re.sub(r'<img[^>]+medium\.com/_/stat[^>]*>', "", body)
    # Drop a leading heading that repeats the title.
    m = re.match(r"\s*<h[1-4][^>]*>(.*?)</h[1-4]>", body, re.S)
    if m and text_of(m.group(1)).lower() == title.lower():
        body = body[m.end():]
    # Stop Jekyll treating {{ or {% in the article as template code.
    body = body.replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return body.strip()


def summary_of(body, limit=220):
    for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
        t = re.sub(r"\s+", " ", text_of(p))
        if len(t) > 40:
            if len(t) <= limit:
                return t
            return t[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return ""


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else FEED
    root = ET.fromstring(fetch(source))
    have = existing_links()
    os.makedirs(POSTS_DIR, exist_ok=True)
    added = 0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = clean_link(item.findtext("link") or "")
        if not title or not link or link in have:
            continue
        body = item.findtext("content:encoded", namespaces=NS) or item.findtext("description") or ""
        body = tidy_body(body, title)
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%d")
        tags = [c.text.replace("-", " ").title() for c in item.findall("category") if c.text]
        front = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"date: {date}",
            f"summary: {json.dumps(summary_of(body), ensure_ascii=False)}",
            f"tags: {json.dumps(tags, ensure_ascii=False)}",
            f"medium_url: {json.dumps(link)}",
            "imported_from_medium: true",
            "---",
            "",
        ]
        path = os.path.join(POSTS_DIR, f"{date}-{slugify(title)}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(front) + body + "\n")
        print(f"Added {path}")
        added += 1
    print(f"{added} new article(s).")


if __name__ == "__main__":
    main()
