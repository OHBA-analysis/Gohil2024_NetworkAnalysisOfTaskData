"""Plot results.

"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from osl_dynamics.utils import plotting

def get_best_run():
    best_fe = np.Inf
    for run in range(1, 11):
        history = pickle.load(open(f"data/hmm/run{run:02d}/model/history.pkl", "rb"))
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run

os.makedirs("plots", exist_ok=True)

run = get_best_run()

cmap = plt.get_cmap("tab10")

contrasts = ["visual", "faces_vs_scrambled", "famous_vs_unfamiliar", "button"]

t = np.load(f"data/hmm/run{run:02d}/first_level/t.npy") - 34e-3

#%% Plot state probability time course

alp = pickle.load(open(f"data/hmm/run{run:02d}/inf_params/alp.pkl", "rb"))

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
    cope = np.load(f"data/hmm/run{run:02d}/group_level/contrast_{index}.npy")
    pvalues = np.load(f"data/hmm/run{run:02d}/group_level/contrast_{index}_pvalues.npy")

    # Plot
    fig, ax = plt.subplots()
    for state in range(cope.shape[0]):
        ax.plot(
            t,
            cope[state],
            label=f"State {state+1}",
            linewidth=3,
            color=cmap(state),
        )
        sig_t = t[pvalues[state] < 0.05]
        if len(sig_t) > 0:
            dt = t[1] - t[0]
            y = cope.max() * (1.3 + 0.1 * state)
            for st in sig_t:
                ax.plot((st - dt, st + dt), (y, y), color=cmap(state), linewidth=4)

    # Tidy up plot
    ax.set_xlabel("Time (s)", fontsize=16)
    ax.set_ylabel("State Activation", fontsize=16)
    ax.tick_params(axis="both", labelsize=16)
    ax.set_xlim(t[0], t[-1])

    # Save
    filename = f"plots/{name}.png"
    print(f"Saving {filename}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
