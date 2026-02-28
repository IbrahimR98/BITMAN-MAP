import json
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PROGRAM_URLS = [
    "https://www.bcit.ca/programs/business-information-technology-management-diploma-full-time-6235dipma/",
    # option pages linked on the program page:
    "https://www.bcit.ca/programs/business-information-technology-management-analytics-data-management-option-diploma-full-time-623cdipma/",
    "https://www.bcit.ca/programs/business-information-technology-management-artificial-intelligence-management-option-diploma-full-time-623adipma/",
    "https://www.bcit.ca/programs/business-information-technology-management-enterprise-systems-management-option-diploma-full-time-623bdipma/",
]

OUTLINE_RE = re.compile(r"^https?://www\.bcit\.ca/outlines/\d+/?$")
COURSE_CODE_RE = re.compile(r"\b[A-Z]{3,5}\s?\d{4}\b")

def fetch(url: str) -> str:
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def extract_from_page(url: str):
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")

    outlines = set()
    course_codes = set()

    # grab outline links
    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        if not href:
            continue
        full = urljoin(url, href).split("#")[0]
        if OUTLINE_RE.match(full):
            outlines.add(full.rstrip("/") + "/")

    # grab course codes from visible text (helps with documentation)
    text = soup.get_text(" ", strip=True)
    for m in COURSE_CODE_RE.findall(text.upper()):
        course_codes.add(m.replace(" ", ""))

    return sorted(outlines), sorted(course_codes)

def main():
    all_outlines = set()
    all_codes = set()
    per_page = []

    for u in PROGRAM_URLS:
        outlines, codes = extract_from_page(u)
        per_page.append({"url": u, "outlines_found": len(outlines), "course_codes_found": len(codes)})
        all_outlines.update(outlines)
        all_codes.update(codes)

    # write targets.json for your existing scraper
    with open("src/targets.json", "w", encoding="utf-8") as f:
        json.dump(sorted(all_outlines), f, indent=2)

    # write a helpful reference file for your writeup
    with open("data/processed/program_course_codes.json", "w", encoding="utf-8") as f:
        json.dump(sorted(all_codes), f, indent=2)

    with open("data/processed/program_scrape_summary.json", "w", encoding="utf-8") as f:
        json.dump(per_page, f, indent=2)

    print(f"Saved {len(all_outlines)} outline URLs -> src/targets.json")
    print(f"Saved {len(all_codes)} course codes -> data/processed/program_course_codes.json")
    print("Summary -> data/processed/program_scrape_summary.json")

if __name__ == "__main__":
    main()