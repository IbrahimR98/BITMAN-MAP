import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

COURSE_CODES_FILE = "data/processed/program_course_codes.json"
TARGETS_OUT = "src/targets.json"

OUTLINE_RE = re.compile(r"^https://www\.bcit\.ca/outlines/\d+/?$")
COURSE_SLUG_RE = re.compile(r"^https://www\.bcit\.ca/courses/[a-z0-9\-]+/?$")

def fetch(url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def build_course_code_url(code):
    return f"https://www.bcit.ca/courses/{code.lower()}/"

def find_outline_in_html(base_url, html):
    soup = BeautifulSoup(html, "lxml")
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        full = urljoin(base_url, href).split("#")[0]
        if OUTLINE_RE.match(full):
            return full.rstrip("/") + "/"
    return None

def find_course_slug_links(base_url, html):
    """Find links like /courses/dqm-with-python-babi-4005/"""
    soup = BeautifulSoup(html, "lxml")
    slugs = []
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        full = urljoin(base_url, href).split("#")[0]
        if COURSE_SLUG_RE.match(full):
            full = full.rstrip("/") + "/"
            if full not in slugs:
                slugs.append(full)
    return slugs

def get_outline_for_code(code):
    code_url = build_course_code_url(code)

    # 1) check the code page
    try:
        html = fetch(code_url)
    except Exception:
        return None

    outline = find_outline_in_html(code_url, html)
    if outline:
        return outline

    # 2) follow any course slug pages linked from it (often the real page)
    slug_links = find_course_slug_links(code_url, html)

    for slug in slug_links[:5]:  # limit to avoid going wild
        try:
            slug_html = fetch(slug)
        except Exception:
            continue

        outline = find_outline_in_html(slug, slug_html)
        if outline:
            return outline

    return None

def main():
    with open(COURSE_CODES_FILE, "r", encoding="utf-8") as f:
        course_codes = json.load(f)

    outlines = []
    misses = []

    for code in course_codes:
        outline = get_outline_for_code(code)
        if outline:
            outlines.append(outline)
            print(f"{code} -> Found outline")
        else:
            misses.append(code)
            print(f"{code} -> no outline found")

    # de-duplicate while keeping order
    seen = set()
    uniq_outlines = []
    for o in outlines:
        if o not in seen:
            uniq_outlines.append(o)
            seen.add(o)

    with open(TARGETS_OUT, "w", encoding="utf-8") as f:
        json.dump(uniq_outlines, f, indent=2)

    with open("data/processed/outline_misses.json", "w", encoding="utf-8") as f:
        json.dump(misses, f, indent=2)

    print(f"\nSaved {len(uniq_outlines)} outline URLs -> {TARGETS_OUT}")
    print(f"Misses saved -> data/processed/outline_misses.json ({len(misses)} courses)")

if __name__ == "__main__":
    main()