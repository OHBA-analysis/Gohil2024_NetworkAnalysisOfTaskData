"""Preprocessing."""

from pathlib import Path
import mne
import matplotlib
matplotlib.use("Agg")
from osl_dynamics.meeg import parallel, preproc

# ----------------------------------------------------------------------------
input_dir = Path("data/ds117")
output_dir = Path("data/derivatives")
plots_dir = Path("plots")
log_dir = Path("logs/1_preproc")

sessions = [
    {
        "id": f"sub-{sub:02d}_run-{run:02d}",
        "subject_id": f"sub-{sub:02d}",
        "raw_dir": f"sub{sub:03d}",
        "raw_file": f"run_{run:02d}_sss.fif",
    }
    for sub in range(1, 20)
    for run in range(1, 7)
]

n_workers = 8
# ----------------------------------------------------------------------------


def process_session(session, logger):
    logger.log("Loading raw data...")
    raw_file = input_dir / session["raw_dir"] / "MEG" / session["raw_file"]
    raw = mne.io.read_raw_fif(raw_file, preload=True)

    # EEG061/EEG062 are EOG and EEG063 is ECG in the Wakeman-Henson dataset
    raw.set_channel_types({"EEG061": "eog", "EEG062": "eog", "EEG063": "ecg"})

    logger.log("Filtering and downsampling...")
    raw = raw.notch_filter([50, 100])
    raw = raw.filter(
        l_freq=0.5,
        h_freq=125,
        method="iir",
        iir_params={"order": 5, "ftype": "butter"},
    )
    raw = raw.resample(sfreq=250)

    logger.log("Detecting bad segments...")
    raw = preproc.detect_bad_segments(raw, picks="mag")
    raw = preproc.detect_bad_segments(raw, picks="mag", mode="diff")
    raw = preproc.detect_bad_segments(raw, picks="grad")
    raw = preproc.detect_bad_segments(raw, picks="grad", mode="diff")

    logger.log("Detecting bad channels...")
    raw = preproc.detect_bad_channels(raw, picks="mag")
    raw = preproc.detect_bad_channels(raw, picks="grad")

    logger.log("Running ICA artefact rejection...")
    raw, ica, ic_labels = preproc.ica_ecg_eog_correlation(
        raw, picks="meg", n_components=40
    )

    logger.log("Interpolating bad channels...")
    raw = raw.interpolate_bads(reset_bads=True)

    logger.log("Saving QC plots...")
    preproc.save_qc_plots(
        raw,
        plots_dir / session["id"],
        ica=ica,
        ic_labels=ic_labels,
    )

    logger.log("Saving preprocessed data...")
    preproc_out_dir = output_dir / "preprocessed"
    preproc_out_dir.mkdir(parents=True, exist_ok=True)
    outfile = preproc_out_dir / f"{session['id']}_preproc-raw.fif"
    raw.save(outfile, overwrite=True)

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
