"""Plot results.

"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from osl_dynamics.inference import modes
from osl_dynamics.utils import plotting

def get_best_run():
    best_fe = np.Inf
    for run in range(1, 11):
        history = pickle.load(open(f"data/dynemo/run{run:02d}/model/history.pkl", "rb"))
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run

os.makedirs("plots", exist_ok=True)

run = get_best_run()

cmap = plt.get_cmap("tab10")

contrasts = ["visual", "faces_vs_scrambled", "famous_vs_unfamiliar", "button"]

t = np.load(f"data/dynemo/run{run:02d}/first_level/t.npy")

#%% Plot mode time courses

alp = pickle.load(open(f"data/dynemo/run{run:02d}/inf_params/alp.pkl", "rb"))
covs = np.load(f"data/dynemo/run{run:02d}/inf_params/covs.npy")
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
    # Load COPEs from the group-level GLM
    cope = np.load(f"data/dynemo/run{run:02d}/group_level/contrast_{index}.npy")
    pvalues = np.load(f"data/dynemo/run{run:02d}/group_level/contrast_{index}_pvalues.npy")

    # Plot
    fig, ax = plt.subplots()
    for mode in range(cope.shape[0]):
        # Plot group mean
        ax.plot(t, cope[mode], label=f"Mode {mode+1}", linewidth=3, color=cmap(mode))

        # Add a bar showing significant time point
        sig_t = t[pvalues[mode] < 0.05]
        if len(sig_t) > 0:
            dt = t[1] - t[0]
            y = cope.max() * (1.3 + 0.1 * mode)
            for st in sig_t:
                ax.plot((st-dt, st+dt), (y, y), color=cmap(mode), linewidth=4)    

    # Tidy up plot
    ax.set_xlabel("Time (s)", fontsize=16)
    ax.set_ylabel("Mode Activation", fontsize=16)
    ax.tick_params(axis="both", labelsize=16)
    ax.set_xlim(t[0], t[-1])

    # Save
    filename = f"plots/{name}.png"
    print(f"Saving {filename}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
