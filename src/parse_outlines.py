import os
import re
import json
from bs4 import BeautifulSoup

RAW_DIR = "data/raw"
OUT_FILE = "data/processed/courses.json"

def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_prereq(text):
    match = re.search(r"Prerequisite[s]?\s*(.*)", text, re.IGNORECASE)
    return clean(match.group(1)) if match else None

def main():
    os.makedirs("data/processed", exist_ok=True)

    records = []

    for file in os.listdir(RAW_DIR):
        if not file.endswith(".html"):
            continue

        path = os.path.join(RAW_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")
        full_text = soup.get_text("\n")

        title = soup.title.string if soup.title else file
        prereq = extract_prereq(full_text)

        records.append({
            "source_file": file,
            "title": clean(title),
            "prerequisites_raw": prereq
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Saved {len(records)} records to {OUT_FILE}")

if __name__ == "__main__":
    main()