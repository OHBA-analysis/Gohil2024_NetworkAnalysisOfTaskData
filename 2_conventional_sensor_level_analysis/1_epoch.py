"""Epoch sensor data.

"""

import os
import mne
import numpy as np

def find_events(raw):
    new_event_ids = {"famous": 1, "unfamiliar": 2, "scrambled": 3, "button": 4}
    old_event_ids = {
        "famous": [5, 6, 7],
        "unfamiliar": [13, 14, 15],
        "scrambled": [17, 18, 19],
        "button": [
            256, 261, 262, 263, 269, 270, 271, 273, 274, 275,
            4096, 4101, 4102, 4103, 4109, 4110, 4111, 4114, 4114, 4115,
            4352, 4357, 4359, 4365, 4369,
        ],
    }
    events = mne.find_events(raw, min_duration=0.005, verbose=False)
    for old_event_codes, new_event_codes in zip(old_event_ids.values(), new_event_ids.values()):
        events = mne.merge_events(events, old_event_codes, new_event_codes)
    return events, new_event_ids

def standardize(data):
    data -= np.mean(data, axis=-1, keepdims=True)
    data /= np.std(data, axis=-1, keepdims=True)
    return data

os.makedirs("data/sensor_analysis/epochs", exist_ok=True)
files = []
for sub in range(1, 20):
    for run in range(1, 7):
        # Load preprocessed data
        file = "data/preproc/sub{sub:02d}/run_{run:02d}_sss/run_{run:02d}_sss_preproc_raw.fif".format(sub=sub, run=run)
        raw = mne.io.read_raw_fif(file, preload=True)

        # Standardise
        raw.apply_function(standardize, picks="meg")

        # Find event timings
        events, event_ids = find_events(raw)

        # Epoch and save
        epochs = mne.Epochs(raw, events, event_ids, tmin=-0.1, tmax=1)
        filename = "data/sensor_analysis/epochs/sub{0:02d}_run{1:02d}-epo.fif".format(sub, run)
        epochs.save(filename, overwrite=True)
