"""Plot results.

"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from osl_dynamics.inference import modes
from osl_dynamics.utils import plotting

from utils import get_best_run

os.makedirs("plots", exist_ok=True)

run = get_best_run()

contrasts = ["visual", "faces_vs_scrambled", "famous_vs_unfamiliar", "button"]

t = np.load(f"data/dynemo_analysis/run{run:02d}/first_level/t.npy")

#%% Plot mode time courses

alp = pickle.load(open(f"data/dynemo_analysis/run{run:02d}/inf_params/alp.pkl", "rb"))
covs = np.load(f"data/dynemo_analysis/run{run:02d}/inf_params/covs.npy")
alp = modes.reweight_alphas(alp, covs)

plotting.plot_alpha(
    alp[0],
    n_samples=2000,
    sampling_frequency=250,
    cmap="tab10",
    filename="plots/alpha.png",
)

#%% Plot network response

for index, name in enumerate(contrasts):
    cope = np.load(f"data/dynemo_analysis/run{run:02d}/group_level/contrast_{index}.npy")
    pvalues = np.load(f"data/dynemo_analysis/run{run:02d}/group_level/contrast_{index}_pvalues.npy")

    plotting.plot_evoked_response(
        t,
        cope.T,
        pvalues.T,
        x_label="Time (s)",
        y_label="Mode Activation",
        filename=f"plots/{name}.png",
    )
