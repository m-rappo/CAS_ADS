# --- Table 2 (report): analytical population characteristics -----------------
# Composition of the analytical population and raw departure rate per group.
# Paste this cell at the end of NB6 (or run standalone after NB6).
import pandas as pd

pers = pd.read_parquet(DATA_DIR / "persons_analytical_enriched.parquet")
assert len(pers) == 310_746

rows = []

def add_block(series, label, order=None):
    g = (pers.groupby(series, dropna=False, observed=True)["target_depart"]
             .agg(n="size", taux="mean"))
    g = g.loc[order] if order is not None else g.sort_values("n", ascending=False)
    for cat, r in g.iterrows():
        rows.append({"Variable": label, "Category": str(cat), "n": int(r["n"]),
                     "share_pct": 100 * r["n"] / len(pers),
                     "departure_rate_pct": 100 * r["taux"]})

add_block(pers["sexe"], "Sex")
add_block(pers["nat_groupe"], "Nationality group")
add_block(pers["permis_groupe"], "Permit group")
add_block(pers["menage_type"], "Household type")
add_block(pers["debut_type_premier"], "Entry type",
          order=["arrivee", "snapshot", "naissance", "reprise", "transition"])

age_bands = pd.cut(pers["age_entree"], [0, 18, 30, 45, 65, 120], right=False,
                   labels=["0-17", "18-29", "30-44", "45-64", "65+"])
add_block(age_bands, "Age at entry",
          order=["0-17", "18-29", "30-44", "45-64", "65+"])

table2 = pd.DataFrame(rows).round({"share_pct": 1, "departure_rate_pct": 1})
print(f"Analytical population: {len(pers):,} | "
      f"overall departure rate: {pers['target_depart'].mean():.1%}\n")
print(table2.to_string(index=False))
