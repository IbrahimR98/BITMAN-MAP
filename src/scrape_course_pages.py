import json
import os
import time
import requests

CODES_FILE = "data/processed/all_course_codes.json"
RAW_DIR = "data/raw_courses"

def course_url(code: str) -> str:
    # BCIT redirects this to the real course slug page automatically
    return f"https://www.bcit.ca/courses/{code.lower()}/"

def main(delay_s: float = 0.6):
    os.makedirs(RAW_DIR, exist_ok=True)

    with open(CODES_FILE, "r", encoding="utf-8") as f:
        codes = json.load(f)

    s = requests.Session()

    for i, code in enumerate(codes, start=1):
        url = course_url(code)
        try:
            r = s.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
            r.raise_for_status()

            out_path = os.path.join(RAW_DIR, f"{code}.html")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(r.text)

            print(f"[{i}/{len(codes)}] saved {code}")
        except Exception as e:
            print(f"[{i}/{len(codes)}] FAILED {code} -> {e}")

        time.sleep(delay_s)

if __name__ == "__main__":
    main()