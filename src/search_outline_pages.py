import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup

CODES_FILE = "data/processed/all_course_codes.json"
OUT_FILE = "data/processed/outline_links.json"

SEARCH_URL = "https://www.bcit.ca/outlines/?s={code}"
OUTLINE_LINK_RE = re.compile(r"https?://www\.bcit\.ca/outlines/\d{11,}/?")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-CA,en;q=0.9",
    "Connection": "keep-alive",
}

def main(delay=0.8, debug_first_n=3):
    os.makedirs("data/raw_outline_search", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    codes = json.load(open(CODES_FILE, "r", encoding="utf-8"))
    results = {}

    s = requests.Session()

    for i, code in enumerate(codes, start=1):
        url = SEARCH_URL.format(code=code)
        try:
            r = s.get(url, timeout=25, headers=HEADERS, allow_redirects=True)
            r.raise_for_status()
            html = r.text

            # Debug: save first few search pages so we can inspect
            if i <= debug_first_n:
                dbg_path = os.path.join("data/raw_outline_search", f"search_{code}.html")
                with open(dbg_path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"[debug] saved {dbg_path} (status={r.status_code}, len={len(html)})")

            # Extract ANY outlines links we can find
            soup = BeautifulSoup(html, "lxml")
            found = None

            # 1) Try anchors
            for a in soup.select("a[href]"):
                href = a.get("href", "").strip()
                if not href:
                    continue
                m = OUTLINE_LINK_RE.search(href)
                if m:
                    found = m.group(0)
                    break

            # 2) Fallback: regex scan entire HTML
            if not found:
                m2 = OUTLINE_LINK_RE.search(html)
                if m2:
                    found = m2.group(0)

            if found:
                # normalize trailing slash
                if not found.endswith("/"):
                    found += "/"
                results[code] = found
                print(f"[{i}/{len(codes)}] {code} -> FOUND {found}")
            else:
                print(f"[{i}/{len(codes)}] {code} -> no outline link on search page")

        except Exception as e:
            print(f"[{i}/{len(codes)}] {code} -> ERROR {e}")

        time.sleep(delay)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} outline links -> {OUT_FILE}")

if __name__ == "__main__":
    main()