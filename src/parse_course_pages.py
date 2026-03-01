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
    lines = [clean(x) for x in text.split("\n") if clean(x)]
    for i, line in enumerate(lines):
        if label.lower() in line.lower():
            # take next 1-3 lines as value
            chunk = []
            for j in range(1, 4):
                if i + j < len(lines):
                    chunk.append(lines[i + j])
            val = clean(" ".join(chunk))
            return val if val else None
    return None

def extract_prereq_snippet(text: str):
    lower_text = text.lower()
    keywords = ["prereq", "pre-req", "pre req", "prerequisite"]

    found_index = None
    for kw in keywords:
        idx = lower_text.find(kw)
        if idx != -1:
            found_index = idx
            break

    if found_index is None:
        return None, []

    start = max(0, found_index - 80)
    end = min(len(text), found_index + 600)
    snippet = text[start:end].strip()

    codes = [c.replace(" ", "") for c in COURSE_CODE_RE.findall(snippet.upper())]
    return snippet, codes

def main():
    os.makedirs("data/processed", exist_ok=True)
    records = []

    for fn in os.listdir(RAW_DIR):
        if not fn.endswith(".html"):
            continue

        code = fn.replace(".html", "")
        path = os.path.join(RAW_DIR, fn)

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")
        page_title = clean(soup.title.get_text(" ", strip=True)) if soup.title else code
        text = soup.get_text("\n", strip=True)

        credits = find_value_near_label(text, "Credits")

        prereq_snippet, prereq_codes = extract_prereq_snippet(text)

        records.append({
            "course_code": code,
            "page_title": page_title,
            "credits_raw": credits,
            "prerequisites_raw": prereq_snippet,
            "prereq_codes": prereq_codes
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Saved {len(records)} parsed courses -> {OUT_FILE}")

if __name__ == "__main__":
    main()