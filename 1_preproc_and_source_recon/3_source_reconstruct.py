
"""Source reconstruction.

"""

import numpy as np
from dask.distributed import Client

from osl_ephys import source_recon, utils

if __name__ == "__main__":
    utils.logger.set_up(level="INFO")
    client = Client(n_workers=8, threads_per_worker=1)

    config = """
        source_recon:
        - forward_model:
            model: Single Layer
        - beamform_and_parcellate:
            freq_range: [1, 45]
            chantypes: [mag, grad]
            rank: {meg: 60}
            parcellation_file: fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz
            method: spatial_basis
            orthogonalisation: symmetric
    """

    outdir = "data/preproc"

    subjects = []
    for sub in range(1, 20):
        for run in range(1, 7):
            subjects.append(f"sub-{sub:02d}_run-{run:02d}")

    source_recon.run_src_batch(
        config,
        subjects=subjects,
        outdir=outdir,
        dask_client=True,
    )
