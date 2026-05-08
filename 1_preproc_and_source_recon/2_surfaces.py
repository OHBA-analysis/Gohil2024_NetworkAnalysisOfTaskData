"""Surface extraction from structural MRI.

"""

from pathlib import Path
from osl_dynamics.meeg import parallel, rhino

# ----------------------------------------------------------------------------
input_dir = Path("data/ds117")
output_dir = Path("data/derivatives")
log_dir = Path("logs/2_surfaces")

subjects = [
    {
        "id": f"sub-{sub:02d}",
        "raw_dir": f"sub{sub:03d}",
    }
    for sub in range(1, 20)
]

include_nose = False
n_workers = 8
# ----------------------------------------------------------------------------


def process_subject(subject, logger):
    logger.log("Extracting surfaces...")

    mri_file = input_dir / subject["raw_dir"] / "anatomy" / "highres001.nii.gz"
    outdir = output_dir / "anat_surfaces" / subject["id"]

    rhino.extract_surfaces(
        mri_file=str(mri_file),
        outdir=str(outdir),
        include_nose=include_nose,
    )

    logger.log("Done.")


if __name__ == "__main__":
    parallel.run(
        process_subject,
        items=subjects,
        n_workers=n_workers,
        log_dir=log_dir,
    )
