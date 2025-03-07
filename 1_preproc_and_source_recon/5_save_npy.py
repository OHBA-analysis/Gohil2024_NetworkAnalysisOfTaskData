"""Save training data as npy files.

"""

from glob import glob

from osl_dynamics.data import Data

files = sorted(glob("data/preproc/*/*_sflip_lcmv-parc-raw.fif"))
data = Data(files, picks="misc", reject_by_annotation="omit", n_jobs=8)
data.save("data/preproc/npy")
data.delete_dir()
