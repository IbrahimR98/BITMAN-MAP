import json
import os

CORE = "data/processed/core_course_codes.json"
OPTIONS = "data/processed/option_course_codes.json"
OUT = "data/processed/all_course_codes.json"

def main():
    os.makedirs("data/processed", exist_ok=True)

    with open(CORE, "r", encoding="utf-8") as f:
        core = set(json.load(f))

    with open(OPTIONS, "r", encoding="utf-8") as f:
        opts = json.load(f)

    all_codes = set(core)
    for track, codes in opts.items():
        all_codes.update(codes)

    all_codes = sorted(all_codes)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(all_codes, f, indent=2)

    print(f"Saved {len(all_codes)} unique course codes -> {OUT}")

if __name__ == "__main__":
    main()