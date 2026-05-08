"""Plot results.

"""

import os
import pickle
import numpy as np

from osl_dynamics.utils import plotting

from utils import get_best_run

os.makedirs("plots", exist_ok=True)

run = get_best_run()

contrasts = ["visual", "faces_vs_scrambled", "famous_vs_unfamiliar", "button"]

# Shift the time axis to correct for the trigger-to-stimulus projector delay
# in the Wakeman-Henson recording setup
t = np.load(f"data/hmm_analysis/run{run:02d}/first_level/t.npy") - 34e-3

#%% Plot state probability time course

alp = pickle.load(open(f"data/hmm_analysis/run{run:02d}/inf_params/alp.pkl", "rb"))

plotting.plot_alpha(
    alp[0],
    n_samples=2000,
    sampling_frequency=250,
    cmap="tab10",
    filename="plots/alpha.png",
)

#%% Plot network response

for index, name in enumerate(contrasts):
    cope = np.load(f"data/hmm_analysis/run{run:02d}/group_level/contrast_{index}.npy")
    pvalues = np.load(f"data/hmm_analysis/run{run:02d}/group_level/contrast_{index}_pvalues.npy")

    plotting.plot_evoked_response(
        t,
        cope.T,
        pvalues.T,
        x_label="Time (s)",
        y_label="State Activation",
        filename=f"plots/{name}.png",
    )

