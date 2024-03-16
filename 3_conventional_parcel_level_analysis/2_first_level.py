"""First-level analysis.

"""

import os
import mne
import numpy as np
from glob import glob

def calc_tfr(x, evoked=False):
    if evoked:
        x = np.mean(x, axis=0, keepdims=True)
    tfr = mne.time_frequency.tfr_array_morlet(
        x,
        sfreq=250,
        freqs=np.arange(6, 30, 0.5),
        n_cycles=4,
        output="power",
        decim=3,
        n_jobs=16,
    )
    return np.mean(tfr, axis=0).astype(np.float32)

def save_contrasts(name, famous, unfamiliar, scrambled, button):
    contrasts = [
        (famous + unfamiliar + scrambled) / 3,
        famous + unfamiliar - 2 * scrambled,
        famous - unfamiliar,
        button,
    ]
    for i, contrast in enumerate(contrasts):
        filename = f"data/parcel_analysis/first_level/{name}_contrast_{i}.npy"
        np.save(filename, contrast)

os.makedirs("data/parcel_analysis/first_level", exist_ok=True)
for file in sorted(glob("data/parcel_analysis/epochs/*-epo.fif")):
    id = file.split("/")[-1].split("-")[0]
    print(id)

    # Load data
    epochs = mne.read_epochs(file, verbose=False).pick("misc")

    # Get trials for each event type
    trials = {}
    for name in epochs.event_id:
        trials[name] = epochs[name].get_data()
        print("{}: {} trials".format(name, trials[name].shape[0]))

    # Total power response
    famous = calc_tfr(trials["famous"])
    unfamiliar = calc_tfr(trials["unfamiliar"])
    scrambled = calc_tfr(trials["scrambled"])
    button = calc_tfr(trials["button"])
    save_contrasts("total_" + id, famous, unfamiliar, scrambled, button)

    # Evoked response
    famous = calc_tfr(trials["famous"], evoked=True)
    unfamiliar = calc_tfr(trials["unfamiliar"], evoked=True)
    scrambled = calc_tfr(trials["scrambled"], evoked=True)
    button = calc_tfr(trials["button"], evoked=True)
    save_contrasts("evoked_" + id, famous, unfamiliar, scrambled, button)

# Save time and frequency axis
np.save("data/parcel_analysis/first_level/t.npy", epochs.times[::3])  # need to account for decim=3
np.save("data/parcel_analysis/first_level/f.npy", np.arange(6, 30, 0.5))
