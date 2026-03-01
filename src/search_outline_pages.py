import os
import json
import time
import requests
from bs4 import BeautifulSoup

CODES_FILE = "data/processed/all_course_codes.json"
OUT_FILE = "data/processed/outline_links.json"

SEARCH_URL = "https://www.bcit.ca/outlines/?s={code}"

def main(delay=0.7):
    os.makedirs("data/processed", exist_ok=True)

    codes = json.load(open(CODES_FILE, "r", encoding="utf-8"))
    results = {}

    session = requests.Session()

    for i, code in enumerate(codes, start=1):
        url = SEARCH_URL.format(code=code)
        try:
            r = session.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "lxml")

            link = None
            for a in soup.select("a[href]"):
                href = a.get("href", "")
                if "/outlines/" in href and code.lower() in a.get_text().lower():
                    link = href
                    break

            if link:
                results[code] = link
                print(f"[{i}/{len(codes)}] Found outline for {code}")
            else:
                print(f"[{i}/{len(codes)}] No outline found for {code}")

        except Exception as e:
            print(f"[{i}/{len(codes)}] ERROR {code} -> {e}")

        time.sleep(delay)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} outline links -> {OUT_FILE}")

if __name__ == "__main__":
    main()