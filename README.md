# Network-Level Oscillatory Response Analysis with Electrophysiological Task Data

Example scripts for reproducing the results in **Gohil, et al. "Network-Level Oscillatory Response Analysis with Electrophysiological Task Data"**.

## Pipeline Overview

![Overview](images/sfig1.png)

## Preprocessing and Source Reconstruction

To run the preprocessnig and source reconstruction:

- `1_preproc.py`.
- `2_source_reconstruct.py`.
- `3_sign_flip.py`.
- `4_save_npy.npy`.

Note, you need to install [OSL](https://github.com/OHBA-analysis/osl) to run these scripts.

## Oscillatory Response Analysis

To run the static analysis:

- `5_sensor_level.py`.
- `6_parcel_level.py`.

To run the dynamic network analysis:

- `7_hmm.py`.
- `8_dynemo.py`.

Note, you need to install [osl-dynamics](https://github.com/OHBA-analysis/osl-dynamics) to run the analysis scripts.
