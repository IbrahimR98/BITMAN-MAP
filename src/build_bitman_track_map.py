import json
import os
import matplotlib.pyplot as plt

TAGS_FILE = "data/processed/course_tags.json"
SUMMARY_FILE = "data/processed/track_summary.json"
OUT = "results/bitman_track_map_clean.png"

TRACKS = ["core", "analytics", "ai", "enterprise"]

# ⭐ Flexible Learning courses (blue)
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

# ✱ Half-semester courses
HALF_SEMESTER = {
    "BSYS2065",
    "BABI4005",
    "BSYS4905",
    "BSYS4005",
    "BSYS4205",
}

def main():
    os.makedirs("results", exist_ok=True)

    tags = json.load(open(TAGS_FILE, "r", encoding="utf-8"))
    summary = json.load(open(SUMMARY_FILE, "r", encoding="utf-8"))

    unique_analytics = set(summary.get("unique_to_analytics", []))
    unique_ai = set(summary.get("unique_to_ai", []))
    unique_enterprise = set(summary.get("unique_to_enterprise", []))

    # Group course codes per track
    groups = {t: [] for t in TRACKS}
    for code, tlist in tags.items():
        for t in tlist:
            if t in groups:
                groups[t].append(code)

    for t in TRACKS:
        groups[t] = sorted(set(groups[t]))

    plt.figure(figsize=(22, 13))
    ax = plt.gca()
    ax.axis("off")

    # BIG TITLE
    ax.text(
        0.5, 1.06,
        "BCIT BITMAN Program 2-Year Map",
        fontsize=26, weight="bold", ha="center",
        transform=ax.transAxes
    )

    # Slightly adjusted column positions for better balance
    column_positions = {
        "core": 0.05,
        "analytics": 0.30,
        "ai": 0.57,
        "enterprise": 0.82,
    }

    titles = {
        "core": "CORE (Year 1 Mandatory)",
        "analytics": "ANALYTICS",
        "ai": "ARTIFICIAL INTELLIGENCE MANAGEMENT",
        "enterprise": "ENTERPRISE"
    }

    # Section titles (make AI title slightly smaller so it doesn't look weird)
    for track in TRACKS:
        title_font = 16
        if track == "ai":
            title_font = 16  # smaller so it fits nicely

        ax.text(
            column_positions[track],
            0.98,
            titles[track],
            fontsize=title_font,
            weight="bold",
            transform=ax.transAxes
        )

    def draw_column(track):
        y = 0.94

        # If a column is truly empty, show it clearly
        if len(groups[track]) == 0:
            ax.text(
                column_positions[track],
                y,
                "(no courses detected)",
                fontsize=11,
                style="italic",
                transform=ax.transAxes
            )
            return

        for code in groups[track]:
            label = code
            fontweight = "normal"
            color = "black"

            # ⭐ Flexible Learning (blue)
            if code in FLEX_COURSES:
                label = f"⭐ {label}"
                color = "#1565C0"

            # ✱ Half-semester
            if code in HALF_SEMESTER:
                label = f"{label} ✱"

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
                fontsize=12,
                fontweight=fontweight,
                color=color,
                transform=ax.transAxes
            )
            y -= 0.036

    for t in TRACKS:
        draw_column(t)

    # Legend
    ax.text(
        0.05,
        0.015,
        "⭐ Blue = Flexible Learning  |  ✱ = Half Semester  |  Bold = Specialization-unique course",
        fontsize=11,
        transform=ax.transAxes
    )

    plt.tight_layout()
    plt.savefig(OUT, dpi=300, bbox_inches="tight")
    print(f"Saved -> {OUT}")

if __name__ == "__main__":
    main()