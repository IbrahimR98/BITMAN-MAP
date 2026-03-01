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

# ✱ Half-semester courses (EDIT this list as needed)
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
        0.5,
        1.06,
        "BCIT BITMAN Program 2-Year Map",
        fontsize=26,
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

    # Section titles (larger)
    for track in TRACKS:
        ax.text(
            column_positions[track],
            0.98,
            titles[track],
            fontsize=16,
            weight="bold",
            transform=ax.transAxes
        )

    def draw_column(track):
        y = 0.94
        for code in groups[track]:

            label = code
            fontweight = "normal"
            color = "black"

            # Flexible Learning (⭐ + blue)
            if code in FLEX_COURSES:
                label = f"⭐ {label}"
                color = "#1565C0"

            # Half-semester (✱)
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
                fontsize=12,      # 🔠 increased
                fontweight=fontweight,
                color=color,
                transform=ax.transAxes
            )

            y -= 0.036  # slightly more spacing

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