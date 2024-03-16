"""Plot results.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from osl_dynamics.analysis import power

os.makedirs("plots", exist_ok=True)

t = np.load("data/parcel_analysis/first_level/t.npy")
f = np.load("data/parcel_analysis/first_level/f.npy")

def load(contrast, parcel="all", name="total"):
    if parcel == "all":
        parcel = range(38)
    tfr = np.load(f"data/parcel_analysis/group_level/{name}_contrast_{contrast}.npy")
    pvalues = np.load(f"data/parcel_analysis/group_level/{name}_contrast_{contrast}_pvalues.npy")
    return np.squeeze(tfr[parcel]), np.squeeze(pvalues[parcel])

def plot_tfr(data, pvalues, filename):
    # Create figure
    fig, ax =  plt.subplots()

    # Plot time-frequency response
    vmax = np.max([data, -data])
    im = ax.imshow(
        data,
        cmap="RdBu_r",
        origin="lower",
        aspect="auto",
        extent=[t[0], t[-1], f[0], f[-1]],
        vmin=-vmax,
        vmax=vmax,
    )

    # Highlight significant clusters
    X, Y = np.meshgrid(t, f)
    ax.contour(X, Y, pvalues, [0.05], colors="black", linewidths=5)

    # Add colour bar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax, orientation="vertical")
    cbar.ax.tick_params(labelsize=16)

    # Tidy up
    ax.set_xlabel("Time (s)", fontsize=16)
    ax.set_ylabel("Frequency (Hz)", fontsize=16)
    ax.set_xlim(t[0], t[-1])
    ax.set_ylim(f[0], f[-1])
    ax.tick_params(axis="both", labelsize=16)

    # Save
    print(f"Saving {filename}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

#%% Plot parcel locations

# Highlight the location of particular parcels
for parcel in [9, 25]:
    vector = np.zeros(38)
    vector[parcel] = 1
    power.save(
        vector,
        mask_file="MNI152_T1_8mm_brain.nii.gz",
        parcellation_file="fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz",
        plot_kwargs={
            "views": ["lateral"],
            "colorbar": False,
            "symmetric_cbar": True,
            "cmap": "RdBu_r",
            "bg_on_data": 1,
            "darkness": 1,
            "alpha": 1,
        },
        filename=f"plots/parcel_{parcel}_.png",
    )

# Plot p-value of each parcel for the different contrasts
for contrast in range(4):

    # What parcels have at least one time point with p-values < 0.05
    _, pvalues = load(contrast, name="total")
    sig_parcels = np.any(pvalues < 0.05, axis=(-1, -2))
    sig_parcels_indices = sig_parcels.nonzero()[0]

    if not any(sig_parcels):
        print(f"no significant parcels for contrast {contrast}")
    else:
        print(f"significant parcels for contrast {contrast}: {sig_parcels_indices}")
        vector = np.zeros(pvalues.shape[0])
        vector[sig_parcels] = 1
        power.save(
            vector,
            mask_file="MNI152_T1_8mm_brain.nii.gz",
            parcellation_file="fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz",
            plot_kwargs={
                "views": ["lateral"],
                "colorbar": False,
                "symmetric_cbar": True,
                "cmap": "RdBu_r",
                "bg_on_data": 1,
                "darkness": 1,
                "alpha": 1,
            },
            filename=f"plots/sig_parcels_contrast_{contrast}_.png",
        )

#%% Plot visual (all) response

contrast = 0
parcel = 25

# Total power response
visual, p_visual = load(contrast, parcel, name="total")
plot_tfr(visual, p_visual, "plots/visual_total.png")

# Evoked response
visual, p_visual = load(contrast, parcel, name="evoked")
plot_tfr(visual, p_visual, "plots/visual_evoked.png")

# Induced response
visual, p_visual = load(contrast, parcel, name="induced")
plot_tfr(visual, p_visual, "plots/visual_induced.png")

#%% Plot faces vs scrambled response

contrast = 1
parcel = 25

# Total power response
faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, parcel, name="total")
plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_total.png")

# Evoked response
faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, parcel, name="evoked")
plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_evoked.png")

# Induced response
faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, parcel, name="induced")
plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_induced.png")

#%% Plot famous vs unfamiliar response

contrast = 2
parcel = 25

# Total power response
famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, parcel, name="total")
plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_total.png")

# Evoked response
famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, parcel, name="evoked")
plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_evoked.png")

# Induced response
famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, parcel, name="induced")
plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_induced.png")

#%% Plot button press response

contrast = 3
parcel = 9

# Total power response
button, p_button = load(contrast, parcel, name="total")
plot_tfr(button, p_button, "plots/button_total.png")

# Evoked response
button, p_button = load(contrast, parcel, name="evoked")
plot_tfr(button, p_button, "plots/button_evoked.png")

# Induced response
button, p_button = load(contrast, parcel, name="induced")
plot_tfr(button, p_button, "plots/button_induced.png")
