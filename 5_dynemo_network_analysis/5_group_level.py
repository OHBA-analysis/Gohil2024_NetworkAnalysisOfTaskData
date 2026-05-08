"""Group-level analysis.

"""

import os
import numpy as np
from glob import glob

from osl_dynamics.analysis import statistics

from utils import get_best_run

run = get_best_run()

t = np.load(f"data/dynemo_analysis/run{run:02d}/first_level/t.npy")

os.makedirs(f"data/dynemo_analysis/run{run:02d}/group_level", exist_ok=True)
for contrast in range(4):

    # Load epoched mode time courses for each subject and run
    first_level_files = sorted(glob(f"data/dynemo_analysis/run{run:02d}/first_level/*_contrast_{contrast}.npy"))
    epochs = np.array([np.load(file) for file in first_level_files])

    # Baseline correct
    epochs -= np.mean(epochs[..., t < 0], axis=-1, keepdims=True)

    # Do statistical significance testing
    pvalues = statistics.evoked_response_max_stat_perm(epochs, n_perm=1000, n_jobs=16)

    # Average over subjects and runs
    epochs = np.mean(epochs, axis=0)

    # Save
    np.save(f"data/dynemo_analysis/run{run:02d}/group_level/contrast_{contrast}.npy", epochs)
    np.save(f"data/dynemo_analysis/run{run:02d}/group_level/contrast_{contrast}_pvalues.npy", pvalues)
