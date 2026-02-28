import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PROGRAM_URL = "https://www.bcit.ca/programs/business-information-technology-management-diploma-full-time-6235dipma/"

COURSE_PAGE_RE = re.compile(r"^https://www\.bcit\.ca/courses/[a-z0-9\-]+/?$")
OUTLINE_RE = re.compile(r"^https://www\.bcit\.ca/outlines/\d+/?$")

def fetch(url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def get_course_pages():
    html = fetch(PROGRAM_URL)
    soup = BeautifulSoup(html, "lxml")

    course_pages = set()

    for a in soup.select("a[href]"):
        href = a.get("href", "")
        full = urljoin(PROGRAM_URL, href).split("#")[0]

        if COURSE_PAGE_RE.match(full):
            course_pages.add(full.rstrip("/") + "/")

    return sorted(course_pages)

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
    course_pages = get_course_pages()
    print(f"Found {len(course_pages)} course pages")

    outline_urls = set()

    for cp in course_pages:
        outline = get_outline_from_course(cp)
        if outline:
            outline_urls.add(outline)
            print(f"Found outline: {outline}")

    with open("src/targets.json", "w", encoding="utf-8") as f:
        json.dump(sorted(outline_urls), f, indent=2)

    print(f"\nSaved {len(outline_urls)} outline URLs -> src/targets.json")

if __name__ == "__main__":
    main()