# simulate_with_model.py

import torch
import pandas as pd
import numpy as np
from simulation import run_simulation_with_custom_timings  # ← make sure your simulation exposes this
from train_model import TimingNet

# Load camera snapshot vector (cam1–cam32 row)
data = pd.read_csv("camera_vector_snapshot.csv")
camera_vector = data["vehicle_count"].values[:32]  # assuming vertical format

# Normalize (same way as training)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(pd.read_csv("ml_dataset.csv").iloc[:, 1:33])  # cam1–cam32
camera_vector_scaled = scaler.transform([camera_vector])

# Load model
model = TimingNet()
model.load_state_dict(torch.load("best_model.pt"))
model.eval()

# Predict timing vector
with torch.no_grad():
    input_tensor = torch.tensor(camera_vector_scaled, dtype=torch.float32)
    timing_vector = model(input_tensor).numpy().flatten()

print("Predicted Timing Vector (16D):")
print(np.round(timing_vector, 2))

# OPTIONAL: Run the simulation using this timing vector
# Note: You'll need to implement run_simulation_with_custom_timings(timings: list[float])
# inside your simulation.py if not already
#
# result = run_simulation_with_custom_timings(timing_vector)
# print("Simulation Result:", result)

