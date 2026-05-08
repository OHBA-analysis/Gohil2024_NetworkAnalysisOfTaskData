"""Source reconstruction.

Computes the forward model, fits an LCMV beamformer, applies it and
parcellates the resulting voxel data.
"""

from pathlib import Path
import mne
import matplotlib
matplotlib.use("Agg")
from osl_dynamics.meeg import parallel, rhino, source_recon, parcellation
from osl_dynamics.utils.filenames import OSLFilenames

# ----------------------------------------------------------------------------
output_dir = Path("data/derivatives")
plots_dir = Path("plots")
log_dir = Path("logs/4_source_recon")

sessions = [
    {
        "id": f"sub-{sub:02d}_run-{run:02d}",
        "subject_id": f"sub-{sub:02d}",
    }
    for sub in range(1, 20)
    for run in range(1, 7)
]

gridstep = 8
chantypes = ["mag", "grad"]
rank = {"meg": 60}
frequency_range = [1, 45]
parcellation_file = "fmri_d100_parcellation_with_PCC_reduced_2mm_ss5mm_ds8mm.nii.gz"
parcellation_method = "spatial_basis"
orthogonalisation = "symmetric"
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

    logger.log("Computing forward model...")
    rhino.forward_model(fns, model="Single Layer", gridstep=gridstep)

    logger.log("Computing LCMV beamformer...")
    source_recon.lcmv_beamformer(
        fns,
        chantypes=chantypes,
        rank=rank,
        frequency_range=frequency_range,
    )

    logger.log("Applying LCMV beamformer...")
    voxel_data, voxel_coords = source_recon.apply_lcmv_beamformer(fns)

    logger.log("Parcellating...")
    parcel_data = parcellation.parcellate(
        fns,
        voxel_data,
        voxel_coords,
        method=parcellation_method,
        orthogonalisation=orthogonalisation,
        parcellation_file=parcellation_file,
    )

    logger.log("Saving parcellated data...")
    raw = mne.io.read_raw_fif(str(preproc_file), preload=True)
    parc_fif = str(output_dir / "osl" / session["id"] / "lcmv-parc-raw.fif")
    parcellation.save_as_fif(
        parcel_data,
        raw,
        extra_chans="stim",
        filename=parc_fif,
    )

    logger.log("Saving QC plots...")
    parcellation.save_qc_plots(parc_fif, parcellation_file)

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
