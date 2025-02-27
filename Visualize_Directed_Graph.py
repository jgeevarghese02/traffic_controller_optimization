import csv
import networkx as nx
import matplotlib.pyplot as plt

def node_type_to_color(node_type: str) -> str:
    """
    Assign a color code based on the node type.
    Adjust as needed.
    """
    lower_type = node_type.lower()
    if "entry" in lower_type:
        return "green"
    elif "exit" in lower_type:
        return "blue"
    elif "traffic_controller" in lower_type or "traffic_contoller" in lower_type:
        return "red"
    elif "middle" in lower_type:
        return "yellow"
    else:
        # "Intermediate" or any unknown
        return "gray"

def visualize_directed_graph(csv_filename: str):
    """
    Reads the specified comma-delimited CSV file,
    builds a directed graph using the node coordinates,
    and plots it with Matplotlib.
    """
    G = nx.DiGraph()
    positions = {}
    node_types = {}

    with open(csv_filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader, None)  # skip the header row

        for row in reader:
            # Each row should have at least:
            # 0: Node Number
            # 1: Node Name
            # 2: Node Type
            # 3: Vehicle Direction
            # 4: X coordinate
            # 5: Y coordinate
            # 6: Neighbor Nodes (optional, might be blank or multiple)
            # 7: possibly an empty column if there's a trailing comma

            if len(row) < 7:
                # If the row doesn't have at least 7 elements, skip
                continue

            node_number = row[0].strip()
            node_name   = row[1].strip()
            node_type   = row[2].strip()
            # vehicle_direction = row[3].strip()  # not used for color, but you could store it

            # Convert X/Y coordinates to floats (or ints)
            try:
                x_coord = float(row[4].strip())
            except ValueError:
                x_coord = 0.0

            try:
                y_coord = float(row[5].strip())
            except ValueError:
                y_coord = 0.0

            # Neighbors might be empty or have multiple entries
            neighbors_raw = row[6].strip()
            neighbors = []
            if neighbors_raw:
                # Could have multiple neighbors separated by spaces (e.g. "M.1.1, M.3.5"?)
                # In your data, each neighbor is typically separated by a semicolon or space.
                # Since your example shows they’re separated by commas, let's try splitting on commas first:
                # But from your data, it looks like the last column might have "M.3.5" with no extra commas.
                # So we’ll just split on whitespace to be safe:
                # e.g., "H.1.7,M.1.5" -> we can replace commas with spaces and then split:

                # 1) Replace commas with spaces
                replaced = neighbors_raw.replace(",", " ")
                # 2) Split on whitespace
                neighbors = replaced.split()

            # Create the node
            G.add_node(node_name)
            positions[node_name] = (x_coord, y_coord)
            node_types[node_name] = node_type

            # Add edges to each neighbor
            for nbr in neighbors:
                nbr = nbr.strip()
                if nbr:
                    G.add_edge(node_name, nbr)

    # Now we have our graph, positions, and node types
    # Color each node based on its type
    node_colors = [node_type_to_color(node_types[n]) for n in G.nodes()]

    # Determine min/max for x, y to set axis limits
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]

    if not all_x or not all_y:
        print("No valid node data found. Please check your CSV contents.")
        return

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Plot the graph
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos=positions, node_color=node_colors, node_size=300)
    nx.draw_networkx_edges(G, pos=positions, arrows=True, arrowstyle="-|>", arrowsize=10)
    nx.draw_networkx_labels(G, pos=positions, font_size=8)

    # Give some margin
    x_margin = (max_x - min_x) * 0.05
    y_margin = (max_y - min_y) * 0.05
    plt.xlim(min_x - x_margin, max_x + x_margin)
    plt.ylim(min_y - y_margin, max_y + y_margin)

    # Keep aspect ratio 1:1
    plt.gca().set_aspect("equal", adjustable="datalim")
    plt.title("Directed Graph Visualization")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Adjust the CSV filename if yours is different
    csv_filename = "Directed_Graph - Static.csv"
    visualize_directed_graph(csv_filename)
