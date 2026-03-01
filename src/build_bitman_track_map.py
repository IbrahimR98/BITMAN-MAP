import json
import os
import matplotlib.pyplot as plt

TAGS_FILE = "data/processed/course_tags.json"
SUMMARY_FILE = "data/processed/track_summary.json"
OUT = "results/bitman_track_map_clean.png"

TRACKS = ["core", "analytics", "ai", "enterprise"]

# Manually define flex learning courses here (edit as needed)
FLEX_COURSES = {
    "BSYS2000",
    "BSYS2065",
    "ECON2100",
    "ECON2200",
    "MKTG1102",
    "OPMT1110",
    "FMGT2152",
    "BLAW3600",
    "OPMT3301",
    "BSYS3000",
    "BSYS4000",
    "BSYS4075",
}

def main():
    os.makedirs("results", exist_ok=True)

    tags = json.load(open(TAGS_FILE, "r", encoding="utf-8"))
    summary = json.load(open(SUMMARY_FILE, "r", encoding="utf-8"))

    unique_analytics = set(summary.get("unique_to_analytics", []))
    unique_ai = set(summary.get("unique_to_ai", []))
    unique_enterprise = set(summary.get("unique_to_enterprise", []))

    groups = {t: [] for t in TRACKS}
    for code, tlist in tags.items():
        for t in tlist:
            if t in groups:
                groups[t].append(code)

    for t in TRACKS:
        groups[t] = sorted(set(groups[t]))

    plt.figure(figsize=(20, 12))
    ax = plt.gca()
    ax.axis("off")

    # 🔥 BIG TITLE
    ax.text(
        0.5,
        1.05,
        "BCIT BITMAN Program 2-Year Map",
        fontsize=22,
        weight="bold",
        ha="center",
        transform=ax.transAxes
    )

    column_positions = {
        "core": 0.05,
        "analytics": 0.30,
        "ai": 0.55,
        "enterprise": 0.80,
    }

    titles = {
        "core": "CORE (Year 1 Mandatory)",
        "analytics": "ANALYTICS",
        "ai": "AI",
        "enterprise": "ENTERPRISE"
    }

    # Draw section titles
    for track in TRACKS:
        ax.text(
            column_positions[track],
            0.98,
            titles[track],
            fontsize=14,
            weight="bold",
            transform=ax.transAxes
        )

    # Draw courses
    def draw_column(track):
        y = 0.94
        for code in groups[track]:

            label = code
            fontweight = "normal"
            color = "black"

            # ⭐ Flexible learning courses (blue)
            if code in FLEX_COURSES:
                label = f"⭐ {label}"
                color = "#1565C0"  # clean professional blue

            # Bold specialization-unique courses
            if track == "analytics" and code in unique_analytics:
                fontweight = "bold"
            elif track == "ai" and code in unique_ai:
                fontweight = "bold"
            elif track == "enterprise" and code in unique_enterprise:
                fontweight = "bold"

            ax.text(
                column_positions[track],
                y,
                label,
                fontsize=10,
                fontweight=fontweight,
                color=color,
                transform=ax.transAxes
            )

            y -= 0.032

    for t in TRACKS:
        draw_column(t)

    # Legend
    ax.text(
        0.05,
        0.01,
        "⭐ Blue = Flexible Learning  |  Bold = Specialization-unique course",
        fontsize=10,
        transform=ax.transAxes
    )

    plt.tight_layout()
    plt.savefig(OUT, dpi=250, bbox_inches="tight")
    print(f"Saved -> {OUT}")

if __name__ == "__main__":
    main()