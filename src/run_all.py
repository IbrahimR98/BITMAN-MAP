import subprocess
import sys

STEPS = [
    ["py", "src/extract_tracks.py"],
    ["py", "src/build_all_courses_list.py"],
    ["py", "src/scrape_course_pages.py"],
    ["py", "src/parse_course_pages.py"],
    ["py", "src/build_bitman_track_map.py"],
]

def main():
    for cmd in STEPS:
        print("\n=== Running:", " ".join(cmd), "===")
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print("FAILED:", cmd)
            sys.exit(r.returncode)
    print("\n✅ Done. Check /results folder.")

if __name__ == "__main__":
    main()