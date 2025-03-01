"""Epoch state time courses.

"""

import os
import mne
import pickle
import numpy as np
from glob import glob

from osl_dynamics.inference import modes

def get_best_run():
    best_fe = np.Inf
    for run in range(1, 11):
        history = pickle.load(open(f"data/hmm_analysis/run{run:02d}/model/history.pkl", "rb"))
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run

run = get_best_run()

# Calculate state time course
alp = pickle.load(open(f"data/hmm_analysis/run{run:02d}/inf_params/alp.pkl", "rb"))
stc = modes.argmax_time_courses(alp)

# Parcel data files
parc_files = sorted(glob("data/preproc/*/*_sflip_lcmv-parc-raw.fif"))

# Event IDs
new_event_ids = {"famous": 1, "unfamiliar": 2, "scrambled": 3, "button": 4}
old_event_ids = {
    "famous": [5, 6, 7],
    "unfamiliar": [13, 14, 15],
    "scrambled": [17, 18, 19],
    "button": [
        256, 261, 262, 263, 269, 270, 271, 273, 274, 275,
        4096, 4101, 4102, 4103, 4109, 4110, 4111, 4113, 4114, 4115,
        4352, 4357, 4359, 4365, 4369,
    ],
}

os.makedirs(f"data/hmm_analysis/run{run:02d}/epochs", exist_ok=True)
for s, p in zip(stc, parc_files):

    # Create an MNE raw object
    raw = modes.convert_to_mne_raw(s, p, n_embeddings=15)

    # Find events
    events = mne.find_events(raw, min_duration=0.005, verbose=False)
    for old_event_codes, new_event_codes in zip(old_event_ids.values(), new_event_ids.values()):
        events = mne.merge_events(events, old_event_codes, new_event_codes)

    # Epoch
    epochs = mne.Epochs(
        raw,
        events,
        new_event_ids,
        tmin=-0.1,
        tmax=1.0,
    )

    # Save
    id = p.split("/")[-2]
    filename = f"data/hmm_analysis/run{run:02d}/epochs/{id}_epo.fif"
    epochs.save(filename, overwrite=True)
