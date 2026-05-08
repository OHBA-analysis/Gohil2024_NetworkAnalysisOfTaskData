"""Shared helpers for the HMM analysis scripts."""

import pickle
import numpy as np


def get_best_run(n_runs=10, results_dir="data/hmm_analysis"):
    """Return the run id with the lowest free energy."""
    best_fe = np.inf
    best_run = None
    for run in range(1, n_runs + 1):
        history_file = f"{results_dir}/run{run:02d}/model/history.pkl"
        with open(history_file, "rb") as f:
            history = pickle.load(f)
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run
