import torch
import pandas as pd
from train_model import TimingNet
from sklearn.preprocessing import StandardScaler

def get_latest_ml_timings():
    data = pd.read_csv("camera_vector_snapshot.csv")
    cam_vector = data["vehicle_count"].values[:32]

    scaler = StandardScaler()
    scaler.fit(pd.read_csv("ml_dataset_synthetic.csv").iloc[:, 1:33])
    cam_vector_scaled = scaler.transform([cam_vector])

    model = TimingNet()
    model.load_state_dict(torch.load("best_model.pt"))
    model.eval()

    with torch.no_grad():
        input_tensor = torch.tensor(cam_vector_scaled, dtype=torch.float32)
        output = model(input_tensor).numpy().flatten()

    return output.tolist()
