Preprocessing, Source Reconstruction and Parcellation
-----------------------------------------------------

Example scripts for preprocessing, source reconstructing and parcellating the [Wakeman-Henson dataset](https://openneuro.org/datasets/ds000117/versions/1.0.5) using [osl-ephys](https://github.com/OHBA-analysis/osl-ephys).

Scripts:

- `1_preproc.py`: Preprocessing for the sensor-level data.
- `2_coregister.py`: Coregistration.
- `3_source_reconstruct.py`: Beamforming and parcellation.
- `4_sign_flip.py`: Assign the sign of each parcel time course across sessions.
- `5_save_npy.npy`: Save time series data as a vanilla numpy file.

Note, these scripts have been written to preprocess/source reconstruct multiple sessions in parallel.
