"""Plot results.

"""

import mne
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

plot_sensors = False
plot_sig_sensors = False
plot_visual = True
plot_faces_vs_scrambled = True
plot_famous_vs_unfamiliar = True
plot_button = True

preproc_file = (
    "/well/woolrich/projects/wakeman_henson/spring23/preproc"
    "/sub{sub:02d}/run_{run:02d}_sss/run_{run:02d}_sss_preproc_raw.fif"
)

t = np.load("data/first_level/t.npy")
f = np.load("data/first_level/f.npy")

def load(contrast, sensor="all", name="total"):
    raw = mne.io.read_raw_fif(preproc_file.format(sub=1, run=1)).pick("meg")
    if sensor == "all":
        mask = [True] * len(raw.ch_names)
    else:
        mask = np.array(raw.ch_names) == sensor
    tfr = np.load(f"data/group_level/{name}_contrast_{contrast}.npy")
    pvalues = np.load(f"data/group_level/{name}_contrast_{contrast}_pvalues.npy")
    return np.squeeze(tfr[mask]), np.squeeze(pvalues[mask])

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

def save(filename):
    print(f"Saving {filename}")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

if plot_sensors:
    raw = mne.io.read_raw_fif(preproc_file.format(sub=1, run=1)).pick("meg")
    fig = raw.plot_sensors(show_names=True, show=False, sphere=(0, -0.02, 0, 0.09))
    save("plots/sensors_with_names.png")
    fig = raw.plot_sensors(show_names=False, show=False, sphere=(0, -0.02, 0, 0.09))
    save("plots/sensors.png")

if plot_sig_sensors:
    # Contrasts:
    # - 0 = ButtonPress
    # - 1 = Visual
    # - 2 = Faces_vs_Scrambled
    # - 3 = Famous_vs_Unfamiliar
    for contrast in range(4):
        # What sensors have at least one time point with p-values < 0.05
        _, pvalues = load(contrast)
        sig_sensors = np.any(pvalues < 0.05, axis=(-1, -2))

        if not any(sig_sensors):
            print(f"no significant sensors for contrast {contrast}")
        else:
            raw = mne.io.read_raw_fif(preproc_file.format(sub=1, run=1)).pick("meg")
            ch_names = np.array(raw.ch_names)
            print(ch_names[sig_sensors])
            raw = raw.pick(list(ch_names[sig_sensors]))
            fig = raw.plot_sensors(show_names=True, show=False, sphere=(0, -0.02, 0, 0.09))
            save(f"plots/sig_sensors_constrast_{contrast}.png")

if plot_visual:
    contrast = 0
    sensor = "MEG2111" #"MEG1911"

    # Total power response
    visual, p_visual = load(contrast, sensor, name="total")
    plot_tfr(visual, p_visual, "plots/visual_total.png")

    # Evoked response
    visual, p_visual = load(contrast, sensor, name="evoked")
    plot_tfr(visual, p_visual, "plots/visual_evoked.png")

    # Induced response
    visual, p_visual = load(contrast, sensor, name="induced")
    plot_tfr(visual, p_visual, "plots/visual_induced.png")

if plot_faces_vs_scrambled:
    contrast = 1
    sensor = "MEG2111" #"MEG1911"

    # Total power response
    faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, sensor, name="total")
    plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_total.png")

    # Evoked response
    faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, sensor, name="evoked")
    plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_evoked.png")

    # Induced response
    faces_vs_scrambled, p_faces_vs_scrambled = load(contrast, sensor, name="induced")
    plot_tfr(faces_vs_scrambled, p_faces_vs_scrambled, "plots/faces_vs_scrambled_induced.png")

if plot_famous_vs_unfamiliar:
    contrast = 2
    sensor = "MEG2111" #"MEG2033"

    # Total power response
    famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, sensor, name="total")
    plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_total.png")

    # Evoked response
    famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, sensor, name="evoked")
    plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_evoked.png")

    # Induced response
    famous_vs_unfamiliar, p_famous_vs_unfamiliar = load(contrast, sensor, name="induced")
    plot_tfr(famous_vs_unfamiliar, p_famous_vs_unfamiliar, "plots/famous_vs_unfamiliar_induced.png")

if plot_button:
    contrast = 3
    sensor = "MEG0721"

    # Total power response
    button, p_button = load(contrast, sensor, name="total")
    plot_tfr(button, p_button, "plots/button_total.png")

    # Evoked response
    button, p_button = load(contrast, sensor, name="evoked")
    plot_tfr(button, p_button, "plots/button_evoked.png")

    # Induced response
    button, p_button = load(contrast, sensor, name="induced")
    plot_tfr(button, p_button, "plots/button_induced.png")

