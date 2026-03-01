import json
import os
import matplotlib.pyplot as plt
import networkx as nx

TAGS_FILE = "data/processed/course_tags.json"
OUT = "results/bitman_track_map.png"

TRACK_ORDER = ["core", "analytics", "ai", "enterprise"]

def main():
    os.makedirs("results", exist_ok=True)

    tags = json.load(open(TAGS_FILE, "r", encoding="utf-8"))

    # Group nodes by track label
    groups = {t: [] for t in TRACK_ORDER}
    shared = []

    for code, tlist in tags.items():
        tset = set(tlist)
        # "core" group
        if "core" in tset:
            groups["core"].append(code)
        # options
        if "analytics" in tset:
            groups["analytics"].append(code)
        if "ai" in tset:
            groups["ai"].append(code)
        if "enterprise" in tset:
            groups["enterprise"].append(code)

        # mark shared across all 3 options
        if {"analytics", "ai", "enterprise"}.issubset(tset):
            shared.append(code)

    # Build graph: connect tracks -> courses (a "map" layout)
    G = nx.DiGraph()
    for t in TRACK_ORDER:
        G.add_node(t.upper())

    for code, tlist in tags.items():
        G.add_node(code)
        for t in tlist:
            G.add_edge(t.upper(), code)

    # Manual layout (makes it readable)
    pos = {}
    pos["CORE"] = (-2, 0)
    pos["ANALYTICS"] = (0, 1.5)
    pos["AI"] = (0, 0)
    pos["ENTERPRISE"] = (0, -1.5)

    # Spread courses near their track label
    def place_codes(codes, x_base, y_base):
        codes = sorted(codes)
        for i, code in enumerate(codes):
            pos[code] = (x_base + 2 + (i % 10) * 0.6, y_base - (i // 10) * 0.35)

    place_codes(groups["core"], -2, 0)
    place_codes(groups["analytics"], 0, 1.5)
    place_codes(groups["ai"], 0, 0)
    place_codes(groups["enterprise"], 0, -1.5)

    plt.figure(figsize=(18, 10))
    nx.draw(G, pos, with_labels=True, node_size=1200, font_size=8, arrows=False)
    plt.title("BITMAN Map: Core + Options (track membership + overlaps)")
    plt.tight_layout()
    plt.savefig(OUT, dpi=200)
    print(f"Saved -> {OUT}")

if __name__ == "__main__":
    main()