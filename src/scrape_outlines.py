import json
import os
import time
from urllib.parse import urlparse

import requests

TARGETS_FILE = "src/targets.json"
RAW_DIR = "data/raw"

def safe_name(url: str) -> str:
    # outlines/20261092135/ -> outlines_20261092135.html
    path = urlparse(url).path.strip("/").replace("/", "_")
    return f"{path}.html"

def main(delay_s: float = 0.7):
    os.makedirs(RAW_DIR, exist_ok=True)

    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    session = requests.Session()

    for i, url in enumerate(urls, start=1):
        try:
            r = session.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()

            fn = safe_name(url)
            out_path = os.path.join(RAW_DIR, fn)

            with open(out_path, "w", encoding="utf-8") as out:
                out.write(r.text)

            print(f"[{i}/{len(urls)}] saved -> {out_path}")

        except Exception as e:
            print(f"[{i}/{len(urls)}] FAILED {url} -> {e}")

        time.sleep(delay_s)

if __name__ == "__main__":
    main()