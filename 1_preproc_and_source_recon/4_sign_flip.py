"""Fix the dipole sign ambiguity.

"""

from glob import glob
from dask.distributed import Client

from osl_ephys import source_recon, utils

if __name__ == "__main__":
    utils.logger.set_up(level="INFO")
    client = Client(n_workers=8, threads_per_worker=1)

    outdir = "data/preproc"
    files = sorted(glob(f"{outdir}/*/parc/lcmv-parc-raw.fif"))

    subjects = []
    for path in files:
        subject = path.split("/")[-3]
        subjects.append(subject)

    template = source_recon.find_template_subject(
        outdir,
        subjects,
        n_embeddings=15,
        standardize=True,
    )

    config = f"""
        source_recon:
        - fix_sign_ambiguity:
            template: {template}
            n_embeddings: 15
            standardize: True
            n_init: 3
            n_iter: 3000
            max_flips: 20
    """

    source_recon.run_src_batch(
        config,
        subjects=subjects,
        outdir=outdir,
        dask_client=True,
    )
