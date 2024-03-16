"""Calculate post-hoc spectra and networks.

"""

import pickle
import numpy as np

from osl_dynamics import run_pipeline

def get_best_run():
    best_fe = np.Inf
    for run in range(1, 11):
        history = pickle.load(open(f"data/dynemo/run{run:02d}/model/history.pkl", "rb"))
        if history["free_energy"] < best_fe:
            best_run = run
            best_fe = history["free_energy"]
    print("Best run:", best_run)
    return best_run

config = """
    load_data:
        inputs: data/src/npy
        kwargs:
            sampling_frequency: 250
            mask_file: MNI152_T1_8mm_brain.nii.gz
            parcellation_file: fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz
            n_jobs: 8
        prepare:
            tde_pca: {n_embeddings: 15, n_pca_components: 80}
            standardize: {}
    get_inf_params: {}
    regression_spectra:
        kwargs:
            frequency_range: [1, 45]
            n_jobs: 8
    plot_group_tde_dynemo_networks:
        power_save_kwargs:
            plot_kwargs: {views: [lateral]}
"""

run = get_best_run()

run_pipeline(config, output_dir=f"data/dynemo/run{run:02d}")
