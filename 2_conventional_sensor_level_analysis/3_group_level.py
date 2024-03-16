"""Group-level analysis.

Note, the permutation testing can be slow due to the high dimensionality of the data.
"""

import os
import numpy as np
from glob import glob

from osl_dynamics.analysis import statistics

t = np.load("data/sensor_analysis/first_level/t.npy")

def do_stats(tfr, name, contrast):
    tfr = np.copy(tfr)
    tfr -= np.mean(tfr[..., t < 0], axis=-1, keepdims=True)
    pvalues = statistics.evoked_response_max_stat_perm(tfr, n_perm=200, n_jobs=16)
    tfr = np.mean(tfr, axis=0)
    np.save(f"data/sensor_analysis/group_level/{name}_contrast_{contrast}.npy", tfr)
    np.save(f"data/sensor_analysis/group_level/{name}_contrast_{contrast}_pvalues.npy", pvalues)

os.makedirs("data/sensor_analysis/group_level", exist_ok=True)
for contrast in range(4):

    # Total power response
    total = np.array([np.load(file) for file in sorted(glob(f"data/sensor_analysis/first_level/total_*_contrast_{contrast}.npy"))])
    do_stats(total, "total", contrast)

    # Evoked response
    evoked = np.array([np.load(file) for file in sorted(glob(f"data/sensor_analysis/first_level/evoked_*_contrast_{contrast}.npy"))])
    do_stats(evoked, "evoked", contrast)

    # Induced response
    induced = total - evoked
    do_stats(induced, "induced", contrast)
