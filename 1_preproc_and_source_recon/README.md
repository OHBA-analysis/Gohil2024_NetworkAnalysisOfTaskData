Preprocessing, Source Reconstruction and Parcellation
-----------------------------------------------------

Example scripts for preprocessing, source reconstructing and parcellating the [Wakeman-Henson dataset](https://openneuro.org/datasets/ds000117/versions/1.0.5) using [osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics).

Scripts:

- `1_preproc.py`: Preprocessing for the sensor-level data (filtering, resampling, bad segment/channel detection, ICA artefact rejection, bad-channel interpolation).
- `2_surfaces.py`: Extract inner skull, outer skull and scalp surfaces from the structural MRI using FSL BET.
- `3_coreg.py`: Coregister MEG to MRI using Polhemus headshape points.
- `4_source_recon.py`: Forward model, LCMV beamformer and parcellation.
- `5_sign_flip.py`: Align the sign of each parcel time course across sessions.

Each script processes all sessions in parallel via `osl_dynamics.meeg.parallel.run`. Set `n_workers` at the top of each script to match your machine.

Run them in order. Outputs land under `data/derivatives/`, plots under `plots/`, and per-session logs under `logs/`. A QC report (`plots/report.html`) is regenerated after steps 1, 3 and 4.
