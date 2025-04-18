import csv
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from collections import defaultdict

# --- Configuration ---
BATCH_SIZE = 32
EPOCHS = 100
PATIENCE = 5

# --- Neural Network Model ---
class TrafficMLP(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, input_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x) * 60  # Scale to 0-60 seconds

# --- Dataset Class ---
class TrafficDataset(Dataset):
    def __init__(self, features, targets):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.float32)
        
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]

# --- Data Loading Functions ---
def extract_camera_counts_from_csv(csv_path):
    """Matches your simulation's node counting logic"""
    counts = defaultdict(int)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sequence = row["NodesSequence"].split(";")
            if sequence:
                counts[sequence[0]] += 1
    return [counts[k] for k in sorted(counts.keys())]

def load_training_data():
    """Generates training data from simulation results"""
    features = []
    targets = []
    
    # Collect data from all seed files
    seed_files = [
        "Seed_Night_WorkRushHours_ExtremeHeat.csv",
        # Add other seed files here
    ]
    
    for seed_file in seed_files:
        # Get vehicle counts (features)
        features.append(extract_camera_counts_from_csv(seed_file))
        
        # Get optimal timings (targets) from ML results
        timing_file = "ml_timings.txt"
        with open(timing_file) as f:
            targets.append([float(line.strip()) for line in f])
    
    return np.array(features), np.array(targets)

# --- Training Function ---
def train_supervised(model, train_loader, val_loader, epochs):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    best_val_loss = float('inf')
    patience_counter = 0
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for features, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for features, targets in val_loader:
                outputs = model(features)
                val_loss += criterion(outputs, targets).item()
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        
        print(f'Epoch {epoch+1}/{epochs}')
        print(f'Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}')
        
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            patience_counter = 0
            torch.save(model.state_dict(), 'best_model.pt')
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(f'Early stopping at epoch {epoch+1}')
                break

# --- Main Execution ---
if __name__ == "__main__":
    # Load and prepare data
    features, targets = load_training_data()
    INPUT_SIZE = len(features[0]) if len(features) > 0 else 0
    
    if INPUT_SIZE == 0:
        raise ValueError("No training data found! Run the simulation first to generate data.")
    
    # Split into train/validation
    split_idx = int(0.8 * len(features))
    train_dataset = TrafficDataset(features[:split_idx], targets[:split_idx])
    val_dataset = TrafficDataset(features[split_idx:], targets[split_idx:])
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
    
    # Initialize model
    model = TrafficMLP(INPUT_SIZE)
    
    # Train
    train_supervised(model, train_loader, val_loader, EPOCHS)
    
    # Save final model
    torch.save(model.state_dict(), 'traffic_mlp.pt')