"""Group-level analysis.

"""

import os
import pickle
import numpy as np
from glob import glob

from osl_dynamics.analysis import statistics

def get_best_run():
    best_fe = np.Inf
    for run in range(1, 11):
        history = pickle.load(open(f"data/dynemo/run{run:02d}/model/history.pkl", "rb"))
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run

run = get_best_run()

t = np.load(f"data/dynemo/run{run:02d}/first_level/t.npy")

os.makedirs(f"data/dynemo/run{run:02d}/group_level", exist_ok=True)
for contrast in range(4):

    # Load epoched mode time courses for each subject and run
    first_level_files = sorted(glob(f"data/dynemo/run{run:02d}/first_level/*_contrast_{contrast}.npy"))
    epochs = np.array([np.load(file) for file in first_level_files])

    # Baseline correct
    epochs -= np.mean(epochs[..., t < 0], axis=-1, keepdims=True)

    # Do statistical significance testing
    pvalues = statistics.evoked_response_max_stat_perm(epochs, n_perm=1000, n_jobs=16)

    # Average over subjects and runs
    epochs = np.mean(epochs, axis=0)

    # Save
    np.save(f"data/dynemo/run{run:02d}/group_level/contrast_{contrast}.npy", epochs)
    np.save(f"data/dynemo/run{run:02d}/group_level/contrast_{contrast}_pvalues.npy", pvalues)
