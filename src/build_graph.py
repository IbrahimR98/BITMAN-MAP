import json
import os
import re
import networkx as nx
import matplotlib.pyplot as plt

IN_FILE = "data/processed/courses.json"
OUT_IMG = "results/prereq_graph.png"

COURSE_CODE_RE = re.compile(r"\b[A-Z]{2,4}\s?\d{4}\b")

def find_codes(text):
    if not text:
        return []
    codes = COURSE_CODE_RE.findall(text.upper())
    return [c.replace(" ", "") for c in codes]

def main():
    os.makedirs("results", exist_ok=True)

    with open(IN_FILE, "r", encoding="utf-8") as f:
        courses = json.load(f)

    G = nx.DiGraph()

    for c in courses:
        title = c.get("title", "Unknown")
        title_codes = find_codes(title)

        course_node = title_codes[0] if title_codes else title
        G.add_node(course_node)

        prereq_raw = c.get("prerequisites_raw")
        prereq_codes = find_codes(prereq_raw)

        for p in prereq_codes:
            G.add_node(p)
            G.add_edge(p, course_node)

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=1500, font_size=8, arrows=True)
    plt.title("BCIT Course Prerequisite Map")
    plt.tight_layout()
    plt.savefig(OUT_IMG, dpi=200)

    print(f"Graph saved to {OUT_IMG}")

if __name__ == "__main__":
    main()