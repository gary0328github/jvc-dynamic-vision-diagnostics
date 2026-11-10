# Dynamic-vision machinery diagnosis

Supporting numerical data and plotting scripts for the manuscript **Domain Generalization for Non-Contact Dynamic Vision-Based Machinery Fault Diagnosis via Component-Guided Prototype-Regularization Calibration**, prepared for Journal of Vibration and Control.

## Study overview

Event cameras provide non-contact observations of machinery motion. The study examines how prototype-to-prototype regularization in DARM affects diagnosis across acquisition configurations, and calibrates a shared regularization coefficient from component analysis. The selected coefficient is reused during task-specific source-domain training on Rotor.

On Pump, the Bottom-25% recording-level Macro-F1 increases from 21.30% to 30.99%. The worst-speed mean improves from 43.06% to 45.37%. On Rotor, the mean recording-level Macro-F1 increases from 25.93% to 28.80%.

## Repository status

This repository is privately maintained during submission preparation. It contains project documentation, numerical figure/table source CSVs, and plotting/data-checking scripts. Review access can be arranged by the corresponding author. The planned public release after acceptance will be coordinated with the accepted manuscript.

## Files

| Path | Purpose |
| --- | --- |
| source_data/ | Numerical sources for Figures 4–6 and the main comparison/calibration tables |
| scripts/verify_source_data.py | File-integrity and numerical consistency checks using the Python standard library |
| scripts/plot_figures.py | Recreate quantitative Figures 4, 5 and 6 |
| scripts/support/ | Multi-panel alignment helper supplied with the plotting source |
| requirements.txt | Reference plotting dependencies |
| MANIFEST_SHA256.csv | File fingerprints |

## Check the source data

With Python 3.10 or later, run from the repository root.

```bash
python scripts/verify_source_data.py
```

This verifies the 270 primary endpoint scores, main method means, 192 component/calibration scores, and the plotted numerical data. It requires the Python standard library. See source_data/README.md for units and overlapping panels.

## Recreate the numerical figures

Use a Python 3.10 or 3.11 environment, then run the following commands.

```bash
python -m pip install -r requirements.txt
python scripts/plot_figures.py
```

PNG, PDF, SVG and TIFF outputs are written to outputs/. Delta annotations use a neutral color for both positive and negative values. A Liberation Sans font is used when installed, with DejaVu Sans as the fallback for Figures 5/6. Figure 4 follows the manuscript's serif-style component comparison. Font availability can affect rendering geometry. The numerical sources preserve the manuscript values.

## Data and evaluation

The original XJTU-DV data are provided by the dataset creators at https://doi.org/10.5281/zenodo.17447083. Cite the original dataset and associated papers when reusing those data.

Pump held-out scores participated in learning-rate and coefficient development. Unlabeled per-recording event projections were used for ROI localization. Rotor applies the selected coefficient during source-domain retraining for each task. Recording-level votes are the primary diagnostic unit. Task/seed endpoint counts refer to repeated evaluations of shared physical recordings.

## Software reuse

The included plotting/data-checking software is provided under the MIT license. The alignment helper accompanies the supplied figure-source archive. The original dataset retains its creators' rights and source terms. Citation metadata will be synchronized with the accepted manuscript.
