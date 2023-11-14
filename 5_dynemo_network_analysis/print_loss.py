import pickle
import numpy as np

best_fe = np.Inf
for i in range(1, 11):
    try:
        history = pickle.load(open(f"results/run{i:02d}/model/history.pkl", "rb"))
        fe = history["free_energy"]
        print(f"run{i:02d}: {fe}")
        if fe < best_fe:
            best_run = i
            best_fe = fe
    except:
        print(f"run{i:02d} missing")
print(f"Best run: {best_run}")
