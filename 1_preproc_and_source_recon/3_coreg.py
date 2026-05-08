"""Coregistration.

"""

from pathlib import Path
from osl_dynamics.meeg import parallel, rhino
from osl_dynamics.utils.filenames import OSLFilenames

# ----------------------------------------------------------------------------
output_dir = Path("data/derivatives")
plots_dir = Path("plots")
log_dir = Path("logs/3_coreg")

sessions = [
    {
        "id": f"sub-{sub:02d}_run-{run:02d}",
        "subject_id": f"sub-{sub:02d}",
    }
    for sub in range(1, 20)
    for run in range(1, 7)
]

use_nose = False
n_workers = 8
# ----------------------------------------------------------------------------


def process_session(session, logger):
    preproc_file = output_dir / "preprocessed" / f"{session['id']}_preproc-raw.fif"
    surfaces_dir = output_dir / "anat_surfaces" / session["subject_id"]

    fns = OSLFilenames(
        outdir=str(output_dir / "osl"),
        id=session["id"],
        preproc_file=str(preproc_file),
        surfaces_dir=str(surfaces_dir),
    )

    logger.log("Extracting fiducials and headshape...")
    rhino.extract_fiducials_and_headshape_from_fif(fns)

    logger.log("Removing stray headshape points (nose, neck, far points)...")
    rhino.remove_stray_headshape_points(fns, nose=True)

    logger.log("Coregistering MEG to MRI...")
    rhino.coregister_head_and_mri(
        fns,
        use_headshape=True,
        use_nose=use_nose,
    )

    logger.log("Done.")


if __name__ == "__main__":
    parallel.run(
        process_session,
        items=sessions,
        n_workers=n_workers,
        log_dir=log_dir,
        output_dir=output_dir,
        plots_dir=plots_dir,
    )
