import pygame
import sys
import csv

def load_nodes_from_csv(csv_filename):
    """
    Reads a CSV file, returning a dict:
        { node_name: {"x": float, "y": float, "direction": str}, ... }

    The CSV is expected to have columns in this order:
      0: Node Number
      1: Node Name
      2: Node Type
      3: vehicle direction (e.g. 'southside', 'northside', 'eastside', 'westside')
      4: X coordinate
      5: Y coordinate
      6: Neighbor Nodes (not used here)

    This function ignores unused columns. It extracts only node_name, direction, x, y.
    """
    nodes_dict = {}

    with open(csv_filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        header = next(reader, None)  # Skip header row if present

        for row in reader:
            if len(row) < 6:
                # If the row doesn't have at least 6 columns (0..5), skip it
                continue

            node_name  = row[1].strip()     # e.g. "V.1.1"
            direction  = row[3].strip().lower()  # e.g. "southside"
            x_str      = row[4].strip()
            y_str      = row[5].strip()

            # Convert to float (or int). If there's an error, default to 0.0
            try:
                x_coord = float(x_str)
            except ValueError:
                x_coord = 0.0

            try:
                y_coord = float(y_str)
            except ValueError:
                y_coord = 0.0

            nodes_dict[node_name] = {
                "x": x_coord,
                "y": y_coord,
                "direction": direction
            }

    return nodes_dict


class Vehicle:
    def __init__(self, image, x, y):
        """
        A simple vehicle class to store a position and image.
        No movement logic: it's completely stationary.
        """
        self.image = image
        self.pos = (x, y)   # (x,y) center for the image
        self.active = True  # If needed to toggle visibility

    def update(self):
        pass  # No movement

    def draw(self, surface):
        if not self.active:
            return
        rect = self.image.get_rect(center=self.pos)
        surface.blit(self.image, rect)


def main():
    pygame.init()

    # 1) Load the CSV data
    csv_filename = "Directed_Graph - Static.csv"  # Adjust if needed
    node_data = load_nodes_from_csv(csv_filename)

    # 2) Load the raw background image (do NOT convert yet)
    background_path = "images/Grid_Sim_Background.jpg"
    background_img_raw = pygame.image.load(background_path)
    bg_width, bg_height = background_img_raw.get_size()

    # 3) Now that we have the background size, create the display
    screen = pygame.display.set_mode((bg_width, bg_height))
    pygame.display.set_caption("Stationary Trucks (Background-Sized)")

    # 4) Convert the background after setting the display mode
    background_img = background_img_raw.convert()

    # 5) Load truck images for each direction
    #    (Make sure these files exist; remove or comment out any you don't have.)
    truck_southside_img = pygame.image.load("images/truck_southside.png").convert_alpha()
    truck_northside_img = pygame.image.load("images/truck_northside.png").convert_alpha()
    truck_eastside_img  = pygame.image.load("images/truck_eastside.png").convert_alpha()
    truck_westside_img  = pygame.image.load("images/truck_westside.png").convert_alpha()

    # 6) Map direction keywords to images
    TRUCK_IMAGES = {
        "southside": truck_southside_img,
        "northside": truck_northside_img,
        "eastside":  truck_eastside_img,
        "westside":  truck_westside_img,
    }

    # 7) Create a Vehicle for each node in the CSV
    vehicles = []
    for node_name, info in node_data.items():
        direction = info["direction"]
        x, y = info["x"], info["y"]

        # Get the truck image based on direction; fallback to southside if unknown
        truck_image = TRUCK_IMAGES.get(direction, truck_southside_img)

        v = Vehicle(truck_image, x, y)
        vehicles.append(v)

    clock = pygame.time.Clock()
    running = True

    # 8) Main loop
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update vehicles (stationary)
        for veh in vehicles:
            veh.update()

        # Draw everything
        screen.blit(background_img, (0, 0))
        for veh in vehicles:
            veh.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
