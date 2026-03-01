import os
import json
from bs4 import BeautifulSoup

RAW_COURSE_DIR = "data/raw_courses"
OUT_FILE = "data/processed/outline_links.json"

def main():
    outline_links = {}

    for fn in os.listdir(RAW_COURSE_DIR):
        if not fn.endswith(".html"):
            continue

        code = fn.replace(".html", "")
        path = os.path.join(RAW_COURSE_DIR, fn)

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")

        link = None
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            if "/outlines/" in href:
                link = href
                break

        if link:
            if link.startswith("/"):
                link = "https://www.bcit.ca" + link
            outline_links[code] = link

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(outline_links, f, indent=2)

    print(f"Saved {len(outline_links)} outline links -> {OUT_FILE}")

if __name__ == "__main__":
    main()