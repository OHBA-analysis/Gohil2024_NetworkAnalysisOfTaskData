"""Submit jobs to the BMRC cluster.

"""

import os

def write_job_script(run):
    with open("job.sh", "w") as file:
        name = f"wh-6-{run}"
        file.write("#!/bin/bash\n")
        file.write(f"#SBATCH -J {name}\n")
        file.write(f"#SBATCH -o logs/{name}.out\n")
        file.write(f"#SBATCH -e logs/{name}.err\n")
        file.write("#SBATCH -p gpu_short\n")
        file.write("#SBATCH --gres gpu:1\n")
        file.write("#SBATCH --constraint a100\n")
        file.write("source activate osld\n")
        file.write(f"python run.py {run}\n")

os.makedirs("logs", exist_ok=True)

for run in range(1, 31):
    write_job_script(run)
    os.system("sbatch job.sh")
    os.system("rm job.sh")
