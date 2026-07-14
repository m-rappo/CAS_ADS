# Residential mobility in Lausanne: predicting departures and finding trajectory types

Final project for the CAS in Applied Data Science, University of Bern.

This project turns eleven years of monthly extraction journals from the Lausanne
population register (863,577 consolidated events) and a 2014 year-end snapshot
into 493,912 residential episodes for 310,746 persons, with a measured
reconstruction uncertainty of 1.0% of transitions. Two questions are addressed.
A supervised model predicts eventual departure from entry-time attributes
alone, reaching an AUC of 0.782; trajectory features are deliberately excluded,
and a contaminated model (AUC 0.947) demonstrates why: in a censored window,
the unfolding trajectory encodes the outcome itself. An unsupervised analysis
yields five trajectory types and six entry profiles whose departure rates,
never used in the clustering, span 80% to 31% and 66% to 34%. Crossing the
profiles with geography explains the city's most anomalous district figure.

The full report is available in [`report/`](report/).

## Data availability

**The register data are confidential and are not included in this repository.**
The source files (137 monthly extraction journals, the BDCH 2014 snapshot, and
the building-to-district correspondence table) contain individual-level
population register records of the City of Lausanne. All processing was carried
out inside the secure environment of the city's statistical office; the paths
in the notebook headers point to that environment and will not resolve
elsewhere. The notebooks are published with their outputs, which are aggregate
counts, rates, and figures only; no individual-level record is displayed. A
column-level description of the source files is given in Annex A of the report.

Consequently, the pipeline cannot be re-executed outside the secure
environment. The notebooks document every processing decision and every
reported number so that the analysis can be audited without the data.

## Repository structure

```
notebooks/   The eight pipeline notebooks (see execution order below)
tools/       Standalone scripts generating the schematic report figures
figures/     Final figures as included in the report
report/      The project report (PDF)
requirements.txt
```

## Pipeline

The notebooks form a sequential pipeline: each one reads the Parquet artifacts
written by the previous one. Run order (Restart Kernel & Run All, one notebook
at a time):

| # | Notebook | Role | Main output |
|---|----------|------|-------------|
| 1 | `1_Data_compilation_cleaning`  | Compilation of the 137 monthly journals, encoding and schema harmonisation, corpus completeness guards | `masterfile_brut.parquet` |
| 2 | `2_Data_quality_audit`         | Date-format guards, cancellation matching, last-write-wins deduplication | `masterfile_audited.parquet` |
| 3 | `3_Data_event_classification_target` | Event families and person-level departure target | `masterfile_events.parquet`, `person_target.parquet` |
| 4 | `4_Data_population_2014_snapshot` | Normalisation and validation of the 2014 snapshot (anchor) | `population_2014.parquet` |
| 5 | `5_Episodes_residentiels`      | Sequential chaining into residential episodes, continuity validation, rupture classification | `episodes.parquet`, `absences.parquet` |
| 6 | `6_EDA`                        | Analytical table, sedentary reintegration, exploratory analysis and report figures | `persons_analytical_enriched.parquet` |
| 7 | `7_Departure_prediction`       | Supervised departure prediction, leakage demonstration, error analysis | model comparison, ROC figures |
| 8 | `8_Clustering`                 | Trajectory and entry-profile typologies, stability analysis, spatial contingency | cluster tables and figures |

Notebook 7 creates the stratified 75/25 train/test split on first run (seed 42)
and persists it, so that all models and reruns share the exact same test set.

## Requirements

Python 3.14, with the packages pinned in `requirements.txt` (main stack:
pandas, scikit-learn, lifelines, matplotlib). To reproduce the environment:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Report

The report (PDF, in `report/`) follows the CAS project outline: data and
episode reconstruction (Section 2), exploratory analysis (Section 3), methods
(Section 4), results (Section 5), discussion of significance and uncertainty
(Section 6). Annex A documents every column of the two source file types.

## Author

[Name], [office / affiliation], CAS in Applied Data Science, University of
Bern. Contact: [email].
