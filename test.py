import pygame
import sys
import math

# -----------------------------
# 1. DEFINE THE DIRECTED GRAPH
# -----------------------------
graph_nodes = {
    'A': (226, 784),
    'B': (224, 296),
    'C': (519, 299),
    'D': (519, 538)
}

graph_edges = {
    'A': 'B',
    'B': 'C',
    'C': 'D',
    # 'D': no next node, car disappears when it arrives
}

# -----------------------------
# 2. DEFINE THE CAR CLASS
# -----------------------------
class Car:
    def __init__(self, image, start_node, speed=2):
        """
        :param image: A loaded pygame image (Surface) for the car.
        :param start_node: The name of the node to start on (e.g., 'A').
        :param speed: Pixels moved per frame toward next node.
        """
        self.image = image
        self.current_node = start_node
        self.current_pos = list(graph_nodes[start_node])  # x, y
        self.next_node = graph_edges.get(start_node, None)
        self.speed = speed
        self.active = True  # When we reach D, set False to remove car

    def update(self):
        """Move the car toward the next node if there is one."""
        if not self.active or self.next_node is None:
            return

        target_pos = graph_nodes[self.next_node]
        dx = target_pos[0] - self.current_pos[0]
        dy = target_pos[1] - self.current_pos[1]
        dist = math.hypot(dx, dy)

        if dist > self.speed:
            # Move a fraction of the distance toward the target each frame
            self.current_pos[0] += (dx / dist) * self.speed
            self.current_pos[1] += (dy / dist) * self.speed
        else:
            # We've arrived at the next node exactly
            self.current_pos = list(target_pos)
            self.current_node = self.next_node
            self.next_node = graph_edges.get(self.current_node, None)

            # If we've arrived at D, deactivate
            if self.current_node == 'D':
                self.active = False

    def draw(self, surface):
        """Blit the car onto the given surface if active."""
        if self.active:
            rect = self.image.get_rect(center=(self.current_pos[0], self.current_pos[1]))
            surface.blit(self.image, rect)

# -----------------------------
# 3. MAIN PYGAME LOOP
# -----------------------------
def main():
    pygame.init()

    # STEP A: Load background image (RAW), don't convert yet.
    background_img_raw = pygame.image.load("images/Grid_Sim_Background.jpg")

    # STEP B: Get dimensions from the raw surface
    bg_width, bg_height = background_img_raw.get_size()

    # STEP C: Now set the display mode to that size
    screen = pygame.display.set_mode((bg_width, bg_height))
    pygame.display.set_caption("City Grid with Moving Car")

    # STEP D: Now it is safe to convert the background
    background_img = background_img_raw.convert()

    # Load and convert the car image AFTER the display mode is set
    car_img_raw = pygame.image.load("images/car_eastside.png")
    car_img = car_img_raw.convert_alpha()

    # We'll keep multiple cars in a list so they can spawn every 10 seconds
    cars = []

    clock = pygame.time.Clock()
    running = True

    # Track time between spawns
    time_since_last_spawn = 0
    spawn_interval = 10_000  # 10 seconds in ms

    while running:
        dt = clock.tick(60)  # dt = time since last frame in ms
        time_since_last_spawn += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn a new car every 10 seconds
        if time_since_last_spawn >= spawn_interval:
            new_car = Car(car_img, start_node='A', speed=2)
            cars.append(new_car)
            time_since_last_spawn = 0

        # Update and remove inactive cars
        for car in cars:
            car.update()
        cars = [car for car in cars if car.active]

        # Draw background
        screen.blit(background_img, (0, 0))

        # Draw each car
        for car in cars:
            car.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
