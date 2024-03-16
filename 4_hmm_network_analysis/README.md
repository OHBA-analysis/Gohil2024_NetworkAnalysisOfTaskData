HMM Network Analysis (Parcel Level)
-----------------------------------

Scripts:

- `1_train.py`: Train a model.
- `2_calc_post_hoc.py`: Calculate post-hoc spectra and networks for HMM states.
- `3_epoch.py`: Epoch the state time courses to give 'trials'.
- `4_first_level.py`: Calculate trial averages for different events types (famous faces, unfamiliar faces, scrambled faces and button presses) for each session. These trial averages correspond to the 'network response'. This script also calculates the difference between event types (contrasts).
- `5_group_level.py`: Do statistical testing at the group-level to identify significant responses.
- `6_plot.py`: Plot results.
