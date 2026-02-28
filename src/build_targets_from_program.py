import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

COURSE_CODES_FILE = "data/processed/program_course_codes.json"

OUTLINE_RE = re.compile(r"^https://www\.bcit\.ca/outlines/\d+/?$")

def fetch(url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def build_course_url(code):
    return f"https://www.bcit.ca/courses/{code.lower()}/"

def get_outline_from_course(course_url):
    try:
        html = fetch(course_url)
        soup = BeautifulSoup(html, "lxml")

        for a in soup.select("a[href]"):
            href = a.get("href", "")
            full = urljoin(course_url, href).split("#")[0]

            if OUTLINE_RE.match(full):
                return full.rstrip("/") + "/"
    except:
        pass

    return None

def main():
    with open(COURSE_CODES_FILE, "r", encoding="utf-8") as f:
        course_codes = json.load(f)

    outline_urls = set()

    for code in course_codes:
        course_url = build_course_url(code)
        outline = get_outline_from_course(course_url)

        if outline:
            outline_urls.add(outline)
            print(f"{code} -> Found outline")

    with open("src/targets.json", "w", encoding="utf-8") as f:
        json.dump(sorted(outline_urls), f, indent=2)

    print(f"\nSaved {len(outline_urls)} outline URLs -> src/targets.json")

if __name__ == "__main__":
    main()