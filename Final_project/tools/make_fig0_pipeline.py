"""Figure 0 -- Pipeline overview for the report.

Standalone script (repo: tools/make_fig0_pipeline.py). Regenerates
figures/fig0_pipeline.png. All counts are the frozen final-run values.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------------- palette
C_INPUT  = "#f0f0f0"   # source data
C_PREP   = "#dce6f1"   # NB1-NB4 preparation
C_CORE   = "#c5d9ed"   # NB5-NB6 structuring
C_MODEL  = "#f4e3c1"   # NB7-NB8 analysis
EDGE     = "#4d4d4d"

fig, ax = plt.subplots(figsize=(12.5, 5.4))
ax.set_xlim(0, 112)
ax.set_ylim(0, 50)
ax.axis("off")

def box(x, y, w, h, title, lines, fc, artifact=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4",
                                facecolor=fc, edgecolor=EDGE, linewidth=0.9))
    ax.text(x + w / 2, y + h - 2.0, title, ha="center", va="center",
            fontsize=8, fontweight="bold")
    for j, line in enumerate(lines):
        ax.text(x + w / 2, y + h - 4.3 - 2.15 * j, line,
                ha="center", va="center", fontsize=6.8)
    if artifact:
        ax.text(x + w / 2, y - 1.5, artifact, ha="center", va="center",
                fontsize=6.2, style="italic", color="#666666")
    return (x, y, w, h)

def arrow(b1, b2, kind="h"):
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    if kind == "h":       # straight left -> right, same lane
        p1 = (x1 + w1 + 0.4, y1 + h1 / 2)
        p2 = (x2 - 0.4, y2 + h2 / 2)
        style = "arc3,rad=0"
    elif kind == "merge":  # right edge -> left edge, different lanes
        p1 = (x1 + w1 + 0.4, y1 + h1 / 2)
        p2 = (x2 - 0.4, y2 + h2 / 2)
        style = "arc3,rad=-0.18" if y1 > y2 else "arc3,rad=0.18"
    ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=style,
                                 arrowstyle="-|>", mutation_scale=11,
                                 linewidth=1.0, color=EDGE))

# ------------------------------------------------------------- lane 1 (events)
src1 = box(1, 31, 13.5, 11, "Monthly extractions",
           ["137 CSV files", "2015-01 \u2192 2026-05", "entry journals"], C_INPUT)
nb1 = box(18.5, 31, 15, 11, "NB1 \u2014 Compilation",
          ["encoding / schema", "harmonisation",
           "863,602 raw rows"], C_PREP, "masterfile_brut.parquet")
nb2 = box(37.5, 31, 15, 11, "NB2 \u2014 Quality audit",
          ["date-format guards,", "deduplication",
           "863,577 events kept"], C_PREP, "masterfile_audited.parquet")
nb3 = box(56.5, 31, 15, 11, "NB3 \u2014 Events & target",
          ["event families,", "departure target",
           "291,763 persons \u00b7 57.1% dep."], C_PREP,
          "masterfile_events / person_target")

# ------------------------------------------------------------- lane 2 (snapshot)
src2 = box(18.5, 7, 15, 11, "BDCH 2014 snapshot",
           ["year-end 2014 stock", "140,228 residents"], C_INPUT)
nb4 = box(37.5, 7, 15, 11, "NB4 \u2014 Snapshot",
          ["normalisation,", "anchor validation",
           "140,003 dwelling seeds"], C_PREP, "population_2014.parquet")

# ------------------------------------------------------------- core
nb5 = box(76, 19, 15.5, 12, "NB5 \u2014 Episodes",
          ["sequential chaining", "493,912 episodes",
           "310,746 persons", "96.5% cont. \u00b7 1.0% unexpl."],
          C_CORE, "episodes / absences")
nb6 = box(95.5, 19, 15.5, 12, "NB6 \u2014 EDA & table",
          ["sedentary reintegration,", "features, Figures 1\u20134",
           "310,746 persons", "48.5% departure"],
          C_CORE, "persons_analytical_enriched")

# ------------------------------------------------------------- models
nb7 = box(95.5, 36, 15.5, 11, "NB7 \u2014 Prediction",
          ["supervised: LR, RF, HGB", "298,915 persons",
           "AUC 0.584 \u2192 0.674 \u2192 0.782"], C_MODEL)
nb8 = box(95.5, 2.5, 15.5, 11, "NB8 \u2014 Clustering",
          ["unsupervised: k-means", "5 trajectory clusters",
           "6 entry-profile clusters"], C_MODEL)

# ------------------------------------------------------------- arrows
arrow(src1, nb1); arrow(nb1, nb2); arrow(nb2, nb3)
arrow(src2, nb4)
arrow(nb3, nb5, kind="merge")
arrow(nb4, nb5, kind="merge")
arrow(nb5, nb6)
# NB6 -> NB7 / NB8 (vertical forks from top/bottom edges)
x, y, w, h = nb6
for tgt in (nb7, nb8):
    tx, ty, tw, th = tgt
    p1 = (x + w / 2, y + h + 0.4) if ty > y else (x + w / 2, y - 0.4)
    p2 = (tx + tw / 2, ty - 0.4) if ty > y else (tx + tw / 2, ty + th + 0.4)
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11,
                                 linewidth=1.0, color=EDGE))

# ------------------------------------------------------------- phase labels
ax.text(35, 47.5, "Data preparation", fontsize=8.5, color="#555555",
        style="italic", ha="center")
ax.text(85, 47.5, "Structuring & analysis", fontsize=8.5, color="#555555",
        style="italic", ha="center")

fig.tight_layout()
fig.savefig("fig0_pipeline.png", dpi=220, bbox_inches="tight",
            facecolor="white")
print("saved fig0_pipeline.png")
