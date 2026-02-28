import os
import re
import json
from bs4 import BeautifulSoup

RAW_DIR = "data/raw_courses"
OUT_FILE = "data/processed/bitman_courses.json"

COURSE_CODE_RE = re.compile(r"\b[A-Z]{3,5}\s?\d{4}\b")

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def find_value_near_label(text: str, label: str):
    # best-effort: find a line containing label then take next chunk
    lines = [clean(x) for x in text.split("\n") if clean(x)]
    for i, line in enumerate(lines):
        if label.lower() in line.lower():
            # take next 1-2 lines as value
            nxt = []
            if i + 1 < len(lines):
                nxt.append(lines[i+1])
            if i + 2 < len(lines):
                nxt.append(lines[i+2])
            val = clean(" ".join(nxt))
            return val if val else None
    return None

def main():
    os.makedirs("data/processed", exist_ok=True)
    records = []

    for fn in os.listdir(RAW_DIR):
        if not fn.endswith(".html"):
            continue

        code = fn.replace(".html", "")
        html = open(os.path.join(RAW_DIR, fn), "r", encoding="utf-8").read()
        soup = BeautifulSoup(html, "lxml")

        page_title = clean(soup.title.get_text(" ", strip=True)) if soup.title else code
        text = soup.get_text("\n", strip=True)

        prereq = find_value_near_label(text, "Prerequisite")
        credits = find_value_near_label(text, "Credits")

        # Try extract course codes mentioned in prereq field
        prereq_codes = []
        if prereq:
            prereq_codes = [c.replace(" ", "") for c in COURSE_CODE_RE.findall(prereq.upper())]

        records.append({
            "course_code": code,
            "page_title": page_title,
            "credits_raw": credits,
            "prerequisites_raw": prereq,
            "prereq_codes": prereq_codes
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Saved {len(records)} parsed courses -> {OUT_FILE}")

if __name__ == "__main__":
    main()