import json
import os
import matplotlib.pyplot as plt

TAGS_FILE = "data/processed/course_tags.json"
OUT = "results/bitman_track_map_clean.png"

TRACKS = ["core", "analytics", "ai", "enterprise"]
XPOS = {"core": 0, "analytics": 4, "ai": 8, "enterprise": 12}

def main():
    os.makedirs("results", exist_ok=True)

    tags = json.load(open(TAGS_FILE, "r", encoding="utf-8"))

    # Group course codes per track
    groups = {t: [] for t in TRACKS}
    for code, tlist in tags.items():
        for t in tlist:
            if t in groups:
                groups[t].append(code)

    for t in TRACKS:
        groups[t] = sorted(set(groups[t]))

    # Figure out which courses are shared across multiple option tracks
    option_tracks = {"analytics", "ai", "enterprise"}
    shared_all_three = []
    shared_two = []

    for code, tlist in tags.items():
        tset = set(tlist) & option_tracks
        if len(tset) == 3:
            shared_all_three.append(code)
        elif len(tset) == 2:
            shared_two.append(code)

    shared_all_three = set(shared_all_three)
    shared_two = set(shared_two)

    # Plot
    plt.figure(figsize=(18, 10))
    ax = plt.gca()
    ax.axis("off")

    # Titles
    ax.text(XPOS["core"], 1.02, "CORE (Year 1 Mandatory)", fontsize=14, weight="bold", transform=ax.transAxes)
    ax.text(XPOS["analytics"]/16, 1.02, "ANALYTICS", fontsize=14, weight="bold", transform=ax.transAxes)
    ax.text(XPOS["ai"]/16, 1.02, "AI", fontsize=14, weight="bold", transform=ax.transAxes)
    ax.text(XPOS["enterprise"]/16, 1.02, "ENTERPRISE", fontsize=14, weight="bold", transform=ax.transAxes)

    # Helper to place a column
    def draw_column(track, x, y_start=0.95, step=0.035):
        y = y_start
        for code in groups[track]:
            label = code

            # Tag shared courses (only for option columns)
            if track in option_tracks:
                if code in shared_all_three:
                    label = f"{code}  (shared by all 3 options)"
                elif code in shared_two:
                    label = f"{code}  (shared by 2 options)"

            ax.text(x, y, label, fontsize=10, transform=ax.transAxes)
            y -= step

            # If too long, start a second mini column (wrap)
            if y < 0.05:
                x += 0.18  # move right a bit (within same track)
                y = y_start

    # Draw columns (x in Axes coords 0..1)
    draw_column("core", 0.02)
    draw_column("analytics", 0.27)
    draw_column("ai", 0.52)
    draw_column("enterprise", 0.77)

    ax.text(0.02, 0.01,
            "Note: This map shows track membership + overlap. Prerequisite relationships were not reliably available in static HTML.",
            fontsize=9, transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(OUT, dpi=220)
    print(f"Saved -> {OUT}")

if __name__ == "__main__":
    main()