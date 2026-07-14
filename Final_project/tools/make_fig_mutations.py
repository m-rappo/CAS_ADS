"""Figure -- Episode chaining: how register events build and validate episodes.

Integrates the elements described in report Section 2.4 (snapshot seeds,
amendment rules with counts, continuity check, announced departures,
absences, censoring). Repo: tools/make_fig_mutations.py.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

EDGE = "#4d4d4d"
C_EP = "#c5d9ed"
C_ABS = "#f4e3c1"

fig, ax = plt.subplots(figsize=(14, 4.8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 40)
ax.axis("off")

Y, H = 20, 6          # episode bars occupy y in [20, 26]

def episode(x0, x1, label):
    ax.add_patch(FancyBboxPatch((x0, Y), x1 - x0, H, boxstyle="round,pad=0.25",
                                facecolor=C_EP, edgecolor=EDGE, linewidth=1.0))
    ax.text((x0 + x1) / 2, Y + H / 2, label, ha="center", va="center",
            fontsize=12, fontweight="bold")

episode(10, 44, "Episode 0   (dwelling A: EGID\u2013EWID)")
episode(48, 84, "Episode 1   (dwelling B)")

# ---- lifecycle markers above ----
def marker(x, text):
    ax.plot([x, x], [Y - 1.2, Y + H + 1.2], color=EDGE, linewidth=2.0)
    ax.plot([x], [Y + H + 1.2], marker="v", color=EDGE, markersize=7)
    ax.text(x, Y + H + 2.6, text, ha="center", va="bottom", fontsize=10,
            linespacing=1.35)

marker(10, "Opens an episode:\narrival, birth, or 2014\nsnapshot seed (140,003\nresidents anchor episode 0)")
marker(46, "Move within the city:\ncloses episode 0,\nopens episode 1")
marker(84, "Departure / death closes\n(announced departures close\nat their own date); otherwise\ncensored at the window end")

# announced departure: dotted line + dotted arrow to the closure
ax.plot([74, 74], [Y - 1.2, Y + H + 1.2], color=EDGE, linewidth=1.2, linestyle=":")
ax.add_patch(FancyArrowPatch((74.6, Y - 1.6), (83.2, Y - 0.3),
                             arrowstyle="-|>", mutation_scale=9,
                             linewidth=0.9, linestyle=":", color=EDGE))

# ---- below-bar annotations (Section 2.4 mechanics) ----
def below(x, text, arrow_xs=(), y_anchor=None):
    ya = (Y - 4.6) if y_anchor is None else y_anchor
    ax.text(x, ya, text, ha="center", va="top", fontsize=9.5, linespacing=1.3)
    for axr in arrow_xs:
        ax.add_patch(FancyArrowPatch((axr, ya + 0.6), (axr, Y - 0.3),
                                     arrowstyle="-|>", mutation_scale=10,
                                     linewidth=1.0, color=EDGE))

# temporary absence interval under episode 0
ax.add_patch(Rectangle((21, Y - 2.6), 9, 1.6, facecolor=C_ABS,
                       edgecolor=EDGE, linewidth=0.8))
below(20, "Temporary absence:\nabsence interval,\nthe episode continues", y_anchor=Y - 4.0)

# continuity check at the junction
ax.text(42, Y - 4.6, "\u2713", ha="center", va="top", fontsize=13,
        color="#2e6b2e", fontweight="bold")
below(42, "\nContinuity check at each move:\ndwelling left = dwelling A?\n96.5% of 133,408 transitions;\nresidual 1.0% unexplained")

# in-place amendments into episode 1
below(64, "In-place amendments, no split:\nsame-dwelling transition (33,206),\nretroactive EWID attribution (5,298)",
      arrow_xs=(59, 69))

# announced departure label
below(84, "Announced departure:\nschedules the closure")

# ---- time axis and footnote ----
ax.add_patch(FancyArrowPatch((6, 3.2), (96, 3.2), arrowstyle="-|>",
                             mutation_scale=12, linewidth=1.0, color="#888888"))
ax.text(95, 4.2, "time (effective dates)", fontsize=10, ha="right",
        color="#888888", style="italic")
ax.text(6, 0.8, "Cancellations (Suppression codes) are matched to the entries "
                "they cancel and removed before chaining; they never act on episodes.",
        fontsize=9, style="italic", color="#666666")

fig.tight_layout()
fig.savefig("fig_mutations.png", dpi=220, bbox_inches="tight", facecolor="white")
print("saved")
