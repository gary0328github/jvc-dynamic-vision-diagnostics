# Dynamic-vision machinery diagnosis

Numerical source data and plotting tools for **Domain Generalization for Non-Contact Dynamic Vision-Based Machinery Fault Diagnosis via Component-Guided Prototype-Regularization Calibration**, prepared for Journal of Vibration and Control.

## Included materials

- `source_data/` contains 270 main task/method/seed endpoints, 192 component/coefficient endpoints, matched differences and table summaries. The panels overlap on shared physical recordings. Units and aggregation are described in `source_data/README.md`.
- `scripts/verify_source_data.py` checks the numerical files and their SHA-256 manifest using the Python standard library.
- `scripts/plot_figures.py` exports quantitative Figures 4–6. The current Figure 5 layout uses `scripts/export_figure5_compact.py`.
- `scripts/support/` supplies the plotting alignment helper.
- `CITATION.cff` records the manuscript authors and supporting-material citation.

The study-specific training implementation, preprocessing builders, model weights and raw recordings are held outside this public repository. Implementation references and preprocessing registrations accompany the manuscript as materials for peer review. The public repository supports inspection of the reported numbers and recreation of the quantitative figures.

## Verify and plot

From the repository root, use Python 3.10 or later for the standard-library verifier.

```bash
python scripts/verify_source_data.py
```

For plotting, use Python 3.10 or 3.11 with the reference dependencies.

```bash
python -m pip install -r requirements.txt
python scripts/plot_figures.py
python scripts/export_figure5_compact.py
```

Outputs are written to `outputs/`. The compact Figure 5 exporter preserves the current spacing above the shared legend. Font availability affects label geometry. The numerical verifier checks file integrity and numerical consistency. Full cache construction and model training require the separately retained implementation and original data.

## Data and evaluation

The original XJTU-DV recordings are available from their creators at https://doi.org/10.5281/zenodo.17447083. Cite the original dataset and associated papers when reusing those recordings. Their source terms continue to apply.

Pump held-out scores participated in learning-rate and coefficient development. Unlabeled full-record event projections supplied ROI localization. Rotor reuses the selected coefficient during source-domain retraining for each task. Physical recordings are the diagnostic units, and task/seed endpoint counts describe repeated evaluations of shared recordings.

Compared with full DARM, the manuscript reports Pump Bottom-25% recording-level Macro-F1 of 21.30% and 30.99%, worst-speed means of 43.06% and 45.37%, and Rotor means of 25.93% and 28.80%.

## Attribution

The manuscript authors are Chengrui Yang, Peng Yu, Hongtao Hao and Xiang Li. Citation information is available in `CITATION.cff` and should be updated when article metadata become available. The manuscript is in submission preparation.

The included plotting and verification software uses the existing MIT license. Its copyright and license notice must accompany reuse as specified in `LICENSE`. The original DARM implementation is available from https://github.com/mozhenling/doge-darm (manuscript reference commit `8cc9174`).
