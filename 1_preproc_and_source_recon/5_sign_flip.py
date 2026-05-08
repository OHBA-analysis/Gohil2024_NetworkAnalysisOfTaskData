"""Fix the dipole sign ambiguity.

Aligns the sign of each parcel time course across sessions using the
covariance-based search in :code:`Data.align_channel_signs`, then writes
the sign-flipped data back to a fif file alongside the original.
"""

from glob import glob
import mne
import numpy as np

from osl_dynamics.data import Data
from osl_dynamics.meeg import parcellation

input_dir = "data/derivatives/osl"
n_jobs = 8

# ----------------------------------------------------------------------------

files = sorted(glob(f"{input_dir}/*/lcmv-parc-raw.fif"))

data = Data(files, picks="misc", reject_by_annotation="omit", n_jobs=n_jobs)
data.align_channel_signs(
    n_init=3,
    n_iter=3000,
    max_flips=20,
    n_embeddings=15,
    standardize=True,
)

# Recover the per-channel flip vector for each session by comparing the
# pre- and post-flip arrays. Channel-wise sum of the elementwise product
# is positive when the flip is +1 and negative when the flip is -1.
flips_per_session = [
    np.sign((aligned * raw_arr).sum(axis=0)).astype(np.float32)
    for aligned, raw_arr in zip(data.arrays, data.raw_data_arrays)
]

# Apply the flips to a fresh load of each fif so annotations, stim channel
# and full timing are preserved, then save out as sflip-lcmv-parc-raw.fif.
for src_file, flips in zip(files, flips_per_session):
    print(f"Sign-flipping {src_file}")
    raw = mne.io.read_raw_fif(src_file, preload=True)
    parcel_data = raw.get_data(picks="misc") * flips[:, None]
    out_file = src_file.replace("lcmv-parc-raw.fif", "sflip-lcmv-parc-raw.fif")
    parcellation.save_as_fif(
        parcel_data,
        raw,
        filename=out_file,
        extra_chans="stim",
    )
