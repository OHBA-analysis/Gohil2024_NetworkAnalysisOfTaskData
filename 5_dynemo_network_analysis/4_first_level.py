"""First-level analysis."""

import os
import mne
import numpy as np
from glob import glob

from utils import get_best_run

def save_contrasts(name, famous, unfamiliar, scrambled, button):
    contrasts = [
        (famous + unfamiliar + scrambled) / 3,
        famous + unfamiliar - 2 * scrambled,
        famous - unfamiliar,
        button,
    ]
    for i, contrast in enumerate(contrasts):
        filename = f"data/dynemo_analysis/run{run:02d}/first_level/{name}_contrast_{i}.npy"
        np.save(filename, contrast)

run = get_best_run()

os.makedirs(f"data/dynemo_analysis/run{run:02d}/first_level", exist_ok=True)
for file in sorted(glob(f"data/dynemo_analysis/run{run:02d}/epochs/*_epo.fif")):
    id = file.split("/")[-1].replace("_epo.fif", "")
    print(id)

    # Load data
    epochs = mne.read_epochs(file, verbose=False).pick("misc")

    # Get trials for each event type
    trials = {}
    for name in epochs.event_id:
        trials[name] = epochs[name].get_data()
        print("{}: {} trials".format(name, trials[name].shape[0]))

    # Evoked response
    famous = np.mean(trials["famous"], axis=0)
    unfamiliar = np.mean(trials["unfamiliar"], axis=0)
    scrambled = np.mean(trials["scrambled"], axis=0)
    button = np.mean(trials["button"], axis=0)
    save_contrasts(id, famous, unfamiliar, scrambled, button)

# Save time axis
np.save(f"data/dynemo_analysis/run{run:02d}/first_level/t.npy", epochs.times)
