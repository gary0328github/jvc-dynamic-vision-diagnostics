# Numerical source data

All unlabelled F1/accuracy values are fractions in [0,1]. The plotting scripts convert F1 fractions to percentages. Delta values in pump_paired.csv are fractions; plotted deltas are percentage-point differences. Columns explicitly named percent contain percentages.

| CSV | Rows | Content |
| --- | --- | --- |
| main_endpoints.csv | 270 | Pump 180 and Rotor 90 task/method/seed recording and window scores |
| main_method_comparison.csv | 10 | Manuscript-precision main method means and recomputed means |
| pump_endpoints.csv | 72 | Full and calibrated DARM, 36 endpoints per method, for Figure 5 |
| pump_paired.csv | 36 | Matched Pump full/calibrated scores and differences |
| rotor_endpoints.csv | 36 | Full and calibrated DARM, 18 endpoints per method, for Figure 6 |
| pump_component_calibration.csv | 192 | Pump components and coefficient candidates |
| coefficient_comparison.csv | 4 | Full DARM and PtP coefficients 0.25, 0.50 and 0.75 |

Figure 4 uses three 30 Hz groups (ItP, ItP+ItI and full DARM) and two 40 Hz groups (ItP+ItI and full DARM), with 12 task/seed endpoints per group. The additional 12 ItP-only 40 Hz entries are preserved in the component CSV and are outside the Figure 4 panels.

The 192 component/calibration endpoints overlap the main panel in 72 full/calibrated Pump endpoints. Pump uses 72 physical recordings and Rotor uses 24. Seeds and leave-one-domain-out tasks reuse those recordings. The CSV files contain frozen numerical scores previously checked against the archived recording predictions. The lightweight verifier checks CSV consistency and hashes.
