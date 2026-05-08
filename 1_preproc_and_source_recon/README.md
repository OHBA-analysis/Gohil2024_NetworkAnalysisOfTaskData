Preprocessing, Source Reconstruction and Parcellation
-----------------------------------------------------

Example scripts for preprocessing, source reconstructing and parcellating the [Wakeman-Henson dataset](https://openfmri.org/dataset/ds000117/) using [osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics).

Scripts:

- `1_preproc.py`: Preprocessing for the sensor-level data (filtering, resampling, bad segment/channel detection, ICA artefact rejection, bad-channel interpolation).
- `2_surfaces.py`: Extract inner skull, outer skull and scalp surfaces from the structural MRI using FSL BET.
- `3_coreg.py`: Coregister MEG to MRI using Polhemus headshape points.
- `4_source_recon_and_parc.py`: Forward model, LCMV beamformer and parcellation.
- `5_sign_flip.py`: Align the sign of each parcel time course across sessions.

Each script processes all sessions in parallel via `osl_dynamics.meeg.parallel.run`. Set `n_workers` at the top of each script to match your machine. Run them in order.

## Inputs

The scripts expect the raw Wakeman-Henson data under `data/ds117/`:

```
data/ds117/sub001/MEG/run_01_sss.fif    # raw MEG
data/ds117/sub001/anatomy/highres001.nii.gz   # structural MRI
data/ds117/sub002/...
```

The parcellation file (`fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz`) and standard brain (`MNI152_T1_8mm_brain.nii.gz`) must be on osl-dynamics' parcellation search path or in the working directory.

## Outputs

```
data/derivatives/
├── preprocessed/                    # <id>_preproc-raw.fif (output of step 1)
├── anat_surfaces/<subject>/         # FSL BET surfaces (output of step 2)
└── osl/<id>/                        # output of steps 3, 4, 5
    ├── bem/
    ├── coreg/
    ├── src/
    ├── lcmv-parc-raw.fif            # parcellated data (step 4)
    └── sflip-lcmv-parc-raw.fif      # sign-flipped parcellated data (step 5)
plots/<id>/                          # per-session QC plots
plots/report.html                    # QC report (regenerated after steps 1, 3, 4)
logs/<step>/<id>.log                 # per-session per-step logs
```

## Dependencies

Beyond [osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics), the surface extraction step (`2_surfaces.py`) requires [FSL](https://fsl.fmrib.ox.ac.uk/) with `FSLDIR` set in the environment.
