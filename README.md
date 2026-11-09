# NIErnaya 2026 Phase 2: SDG 2 Zero Hunger
**Team DAV-26-046, Pixel Pioneers (NIE Mysuru)**

Question: where does high agricultural output coexist with poor child nutrition, and what explains it?

## How to open
Open `NIErnaya_Phase2_EDA_Preprocessing_FINAL.ipynb`. It is already executed (every output and chart is stored in it, no cell errors). To re-run, keep the notebook, `helpers.py` and `data/` together, use Python 3.10+, and run all cells.

## Folder map
- `NIErnaya_Phase2_EDA_Preprocessing_FINAL.ipynb`: cleaning, matching, feature engineering, EDA, tests, PCA, leakage-safe models, Appendix A (all 15 data sheets) and Appendix B (PDS).
- `helpers.py`: state/district normalisation and matching.
- `data/raw/`: Phase 1 inputs, untouched (duplicates and missing values kept). `data/raw/other_sheets/` holds the 10 sheets not used in the district model.
- `data/cleaned/`: `district_master_table.csv` (706 districts), `nfhs5_district_clean.csv`, `crop_production_1997_2022_clean.csv.gz`, `upag_district_foodgrains_clean.csv.gz`, `state_context.csv`, `model_matrix_exploratory_scaled_imputed.csv` (653 rows), `district_match_table_upag.csv`, `fuzzy_district_matches_reviewed.csv`, `unmatched_districts_for_documentation.csv`, `sheet_coverage_summary.csv`, `final_validation_summary.csv`, `cleaning_log.csv`.
- `figures/`: 20 charts used in the notebook.

## Every Phase 1 sheet is accounted for
| Status | Sheets |
|---|---|
| Used in the analysis | 01 crop production, 02 NFHS-5, 03 Agmarknet state monthly, 05 UPAG district food grains, 09 FCI procurement |
| Food-distribution snapshot (Appendix B) | 12 PDS monthly national, 13 PDS state portability |
| Cross-checked | 15 district crosswalk: agrees with our own matching on 637 of 637 shared districts |
| Profiled, not modelled (reason in Appendix A) | 04, 06, 07, 08, 10, 11, 14: national, state-total or off-period data that cannot be linked to a district |

## Key results
- 653 of 706 NFHS districts linked to agriculture data (UPAG: 644 exact, 19 reviewed fuzzy, 88 unmatched and left unmatched).
- Yield vs stunting: rho = -0.13; partial rho = -0.05 (p = 0.21) after education, sanitation and clean fuel.
- 59 paradox districts (9%): Uttar Pradesh 19, Bihar 14, Madhya Pradesh 8.
- Leave-states-out R²: agriculture only -0.04, household and health 0.29, both 0.29. Random 5-fold: 0.24, 0.49, 0.51.
- OLS with state fixed effects: yield -1.05 (p = 0.005), women's schooling -3.2, sanitation -2.2; R² = 0.58.
- PCA: PC1 holds 52% of outcome variance; principal-component regression (4 components) R² = 0.35 vs 0.25 with all features.

## Limitations to state openly
- NFHS-5 is 2019-21; agriculture is averaged over 2017-18 to 2021-22.
- District boundaries changed; new districts (for example Niwari, Balotra) are not forced onto old ones.
- District results are associations, not causes (ecological fallacy).
- The cross-source check (rho 0.9996) is not independent: both files come from state agriculture departments.
- Missing values stay where the source suppressed them; nothing was set to zero.
