
"""Coregistration.

"""

import numpy as np
from dask.distributed import Client

from osl_ephys import source_recon, utils

def fix_headshape_points(outdir, subject):
    filenames = source_recon.rhino.get_coreg_filenames(outdir, subject)

    # Load saved headshape and nasion files
    hs = np.loadtxt(filenames["polhemus_headshape_file"])
    nas = np.loadtxt(filenames["polhemus_nasion_file"])
    lpa = np.loadtxt(filenames["polhemus_lpa_file"])
    rpa = np.loadtxt(filenames["polhemus_rpa_file"])

    # Remove headshape points on the nose
    remove = np.logical_and(hs[1] > max(lpa[1], rpa[1]), hs[2] < nas[2])
    hs = hs[:, ~remove]

    # Overwrite headshape file
    utils.logger.log_or_print(f"overwritting {filenames['polhemus_headshape_file']}")
    np.savetxt(filenames["polhemus_headshape_file"], hs)

if __name__ == "__main__":
    utils.logger.set_up(level="INFO")
    client = Client(n_workers=8, threads_per_worker=1)

    config = """
        source_recon:
        - extract_polhemus_from_info: {}
        - fix_headshape_points: {}
        - compute_surfaces:
            include_nose: False
        - coregister:
            use_nose: False
            use_headshape: True
    """

    rawdir = "data/ds117"
    outdir = "data/preproc"

    subjects = []
    smri_files = []
    for sub in range(1, 20):
        for run in range(1, 7):
            smri_files.append(f"{rawdir}/sub{sub:03d}/anatomy/highres001.nii.gz")
            subjects.append(f"sub-{sub:02d}_run-{run:02d}")

    source_recon.run_src_batch(
        config,
        subjects=subjects,
        smri_files=smri_files,
        outdir=outdir,
        extra_funcs=[fix_headshape_points],
        dask_client=True,
    )
