"""Train DyNeMo.

"""

from sys import argv

if len(argv) != 2:
    print("Please pass the run id, e.g. python 1_train.py 1")
    exit()
run = int(argv[1])

from osl_dynamics import run_pipeline

config = """
    load_data:
        inputs: data/preproc/npy
        kwargs:{n_jobs: 8}
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
        save_inf_params: False
"""

run_pipeline(config, output_dir=f"data/dynemo_analysis/run{run:02d}")
