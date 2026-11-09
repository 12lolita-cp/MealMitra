# Final Data Validation Report, NIErnaya Phase 2

## Outcome
All cleaned tables passed structural checks (duplicate full rows 0, infinite values 0; see `data/cleaned/final_validation_summary.csv`). The notebook runs top to bottom with no cell errors. Legitimate missing values are preserved, not filled with zero.

## District linkage (UPAG to NFHS-5)
751 source districts: 644 exact, 19 reviewed fuzzy, 88 unmatched, 0 conflicts. Unsafe aliases Niwari to Tikamgarh and Balotra to Barmer were removed, so Barmer and Tikamgarh keep their own data. The provided crosswalk (sheet 15) agrees with the notebook on 637 of 637 shared districts.

## Analysis sample
653 of 706 NFHS districts in 32 states. The exploratory model matrix has 653 rows and 25 columns, with no missing values.

## Sheet coverage
All 15 data sheets are loaded and profiled in Appendix A (`sheet_coverage_summary.csv`): 5 modelled, 2 in the PDS snapshot, 1 cross-checked, 7 profiled with the reason they cannot enter a district model.

## Model validation (preprocessing fitted inside each training fold)
| Feature set | Random 5-fold R² | Leave-states-out R² |
|---|---:|---:|
| Agriculture only | 0.235 | -0.039 |
| Household & health only | 0.493 | 0.288 |
| Both | 0.506 | 0.290 |

Leave-states-out is the stricter test. Results are associations, not causal.

## Disclose in the presentation
Timing mismatch between sources, boundary changes, preserved missing values, and the observational nature of the analysis.
