import json
import os
import re
import requests
from bs4 import BeautifulSoup

PAGES = {
    "core": "https://www.bcit.ca/programs/business-information-technology-management-diploma-full-time-6235dipma/#courses",
    "analytics": "https://www.bcit.ca/programs/business-information-technology-management-analytics-data-management-option-diploma-full-time-623cdipma/#courses",
    "ai": "https://www.bcit.ca/programs/business-information-technology-management-artificial-intelligence-management-option-diploma-full-time-623adipma/#courses",
    "enterprise": "https://www.bcit.ca/programs/business-information-technology-management-enterprise-systems-management-option-diploma-full-time-623bdipma/#courses",
}

COURSE_CODE_RE = re.compile(r"\b[A-Z]{3,5}\s?\d{4}\b")

def fetch(url: str) -> str:
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def extract_codes_from_courses_section(url: str):
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    section = soup.select_one("#courses")
    if not section:
        # fallback: grab whole page text if #courses isn't found
        text = soup.get_text(" ", strip=True).upper()
    else:
        text = section.get_text(" ", strip=True).upper()

    codes = {c.replace(" ", "") for c in COURSE_CODE_RE.findall(text)}
    return sorted(codes)

def main():
    os.makedirs("data/processed", exist_ok=True)

    track_codes = {}
    for track, url in PAGES.items():
        codes = extract_codes_from_courses_section(url)
        track_codes[track] = codes
        print(f"{track}: {len(codes)} codes")

    # Save per-track lists
    with open("data/processed/core_course_codes.json", "w", encoding="utf-8") as f:
        json.dump(track_codes["core"], f, indent=2)

    option_dict = {k: v for k, v in track_codes.items() if k != "core"}
    with open("data/processed/option_course_codes.json", "w", encoding="utf-8") as f:
        json.dump(option_dict, f, indent=2)

    # Build tags: each course -> which tracks it belongs to
    tags = {}
    for track, codes in track_codes.items():
        for code in codes:
            tags.setdefault(code, []).append(track)

    with open("data/processed/course_tags.json", "w", encoding="utf-8") as f:
        json.dump(dict(sorted(tags.items())), f, indent=2)

    # Helpful summary for your writeup
    all_courses = set(tags.keys())
    core = set(track_codes["core"])
    analytics = set(track_codes["analytics"])
    ai = set(track_codes["ai"])
    enterprise = set(track_codes["enterprise"])

    summary = {
        "total_unique_courses": len(all_courses),
        "core_courses": len(core),
        "analytics_courses": len(analytics),
        "ai_courses": len(ai),
        "enterprise_courses": len(enterprise),
        "shared_by_all_three_options": len(analytics & ai & enterprise),
        "unique_to_analytics": sorted(list(analytics - (ai | enterprise))),
        "unique_to_ai": sorted(list(ai - (analytics | enterprise))),
        "unique_to_enterprise": sorted(list(enterprise - (analytics | ai))),
    }

    with open("data/processed/track_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Saved: core_course_codes.json, option_course_codes.json, course_tags.json, track_summary.json")

if __name__ == "__main__":
    main()