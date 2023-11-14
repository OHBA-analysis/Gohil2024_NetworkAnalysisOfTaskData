"""Train DyNeMo on the Wakeman-Henson dataset.

"""

from sys import argv

if len(argv) != 2:
    print("Please pass the run id, e.g. python run.py 1")
    exit()
id = int(argv[1])

from osl_dynamics import run_pipeline

config = """
    load_data:
        inputs: /well/woolrich/projects/wakeman_henson/spring23/training
        kwargs:
            sampling_frequency: 250
            mask_file: MNI152_T1_8mm_brain.nii.gz
            parcellation_file: fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz
            n_jobs: 4
        prepare:
            tde_pca: {n_embeddings: 15, n_pca_components: 80}
            standardize: {}
    train_dynemo:
        config_kwargs:
            n_modes: 6
            learn_means: False
            learn_covariances: True
            n_kl_annealing_epochs: 10
            n_epochs: 20
        init_kwargs:
            n_init: 10
    regression_spectra:
        kwargs:
            frequency_range: [1, 45]
            n_jobs: 4
    plot_group_tde_dynemo_networks:
        power_save_kwargs:
            plot_kwargs: {views: [lateral]}
"""

run_pipeline(config, output_dir=f"results/run{id:02d}")
