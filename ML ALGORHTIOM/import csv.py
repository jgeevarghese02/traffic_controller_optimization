import csv
from collections import defaultdict


def extract_camera_counts_from_csv(csv_path):
    """
    This function takes in the .csv traffic seed file and returns a list of 32 counts,
    representing how many vehicles came from each entry node. This is used as the input
    to the MLP model.
    """
    counts = defaultdict(int)

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row["NodesSequence"].split(';')
            if path:
                entry_node = path[0]
                counts[entry_node] += 1

    # Map to a fixed vector of size 32
    entry_keys = sorted(counts.keys())[:32]
    x = [counts[k] for k in entry_keys]
    x += [0] * (32 - len(x))  # pad with 0s

    return x



def read_ml_results(filepath="ml_result_metrics.txt"):
    """
    Reads the average elapsed time from the simulation result file.
    This acts as the loss for the model.
    """
    times = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                times.append(float(line.strip()))
            except:
                continue

    if times:
        return sum(times) / len(times), len(times)
    return None, 0
