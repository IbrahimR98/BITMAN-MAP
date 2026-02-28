import json
import os
import networkx as nx
import matplotlib.pyplot as plt

COURSES_FILE = "data/processed/bitman_courses.json"
TAGS_FILE = "data/processed/course_tags.json"

OUT_ALL = "results/prereq_graph_all.png"
OUT_CORE = "results/prereq_graph_core.png"

def main():
    os.makedirs("results", exist_ok=True)

    courses = json.load(open(COURSES_FILE, "r", encoding="utf-8"))
    tags = json.load(open(TAGS_FILE, "r", encoding="utf-8"))

    # Build graph
    G = nx.DiGraph()

    for c in courses:
        code = c["course_code"]
        prereqs = c.get("prereq_codes", []) or []
        G.add_node(code)

        for p in prereqs:
            G.add_node(p)
            G.add_edge(p, code)

    # Save ALL graph
    plt.figure(figsize=(16, 10))
    pos = nx.spring_layout(G, seed=42, k=0.8)
    nx.draw(G, pos, with_labels=True, node_size=1400, font_size=8, arrows=True)
    plt.title("BITMAN Prerequisite Map (Core + Options)")
    plt.tight_layout()
    plt.savefig(OUT_ALL, dpi=200)
    print(f"Saved -> {OUT_ALL}")

    # Save CORE-only subgraph
    core_nodes = [code for code, t in tags.items() if "core" in t]
    core_sub = G.subgraph(core_nodes).copy()

    plt.figure(figsize=(14, 9))
    pos2 = nx.spring_layout(core_sub, seed=42, k=0.9)
    nx.draw(core_sub, pos2, with_labels=True, node_size=1600, font_size=9, arrows=True)
    plt.title("BITMAN Core Prerequisite Map (Year 1 Mandatory)")
    plt.tight_layout()
    plt.savefig(OUT_CORE, dpi=200)
    print(f"Saved -> {OUT_CORE}")

if __name__ == "__main__":
    main()