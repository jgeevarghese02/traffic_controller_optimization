import random
import time
import threading
import pygame
import sys
import tkinter as tk

# Function to get dynamic screen size
def get_screen_size():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height

# Function to calculate scaling percentages
def calculate_scaling_percentages(screen_width, screen_height):
    original_width, original_height = 2360, 1640
    width_adjustment_percent = screen_width / original_width
    height_adjustment_percent = screen_height / original_height
    return width_adjustment_percent, height_adjustment_percent

def initialize_pygame():
    pygame.init()
    screen_width, screen_height = get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Traffic Simulation")
    return screen

def load_images():
    images = {
        #Map
        "background": pygame.image.load("images/Grid_background.png"),
        #Vechicles
        "car_north": pygame.image.load("images/car_northside.png"),
        "car_south": pygame.image.load("images/car_southside.png"),
        "car_east": pygame.image.load("images/car_eastside.png"),
        "car_west": pygame.image.load("images/car_westside.png"),
        "motorcycle_north": pygame.image.load("images/motorcycle_northside.png"),
        "motorcycle_south": pygame.image.load("images/motorcycle_southside.png"),
        "motorcycle_east": pygame.image.load("images/motorcycle_eastside.png"),
        "motorcycle_west": pygame.image.load("images/motorcycle_westside.png"),
        "truck_north": pygame.image.load("images/truck_northside.png"),
        "truck_south": pygame.image.load("images/truck_southside.png"),
        "truck_east": pygame.image.load("images/truck_eastside.png"),
        "truck_west": pygame.image.load("images/truck_westside.png"),
        #Traffic signals
        "traffic_light_red_vertical": pygame.image.load("images\Traffic_light_red_vert.png"),
        "traffic_light_yellow_vertical": pygame.image.load("images\Traffic_light_yellow_vert.png"),
        "traffic_light_green_vertical": pygame.image.load("images\Traffic_light_green_vert.png"),
        "traffic_light_red_horizontal": pygame.image.load("images\Traffic_light_red_hor.png"),
        "traffic_light_yellow_horizontal": pygame.image.load("images\Traffic_light_yellow_hor.png"),
        "traffic_light_green_horizontal": pygame.image.load("images\Traffic_light_green_hor.png"),
        #ML Traffic signals
        "ML_traffic_light_red_vertical": pygame.image.load("images\Traffic_light_red_vert.png"),
        "ML_traffic_light_yellow_vertical": pygame.image.load("images\Traffic_light_yellow_vert.png"),
        "ML_traffic_light_green_vertical": pygame.image.load("images\Traffic_light_green_vert.png"),
        "ML_traffic_light_red_horizontal": pygame.image.load("images\Traffic_light_red_hor.png"),
        "ML_traffic_light_yellow_horizontal": pygame.image.load("images\Traffic_light_yellow_hor.png"),
        "ML_traffic_light_green_horizontal": pygame.image.load("images\Traffic_light_green_hor.png"),
    }
    return images

def generate_cars(screen_width, screen_height):
    # Calculate scaling percentages using the function
    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    # Adjusted car positions after scaling
    car_positions = {
        "east": [
            [(int(4 * width_adjustment_percent), int(552 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(552 * height_adjustment_percent))],
            [(int(4 * width_adjustment_percent), int(591 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(591 * height_adjustment_percent))],
            [(int(4 * width_adjustment_percent), int(1092 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(1092 * height_adjustment_percent))],
            [(int(4 * width_adjustment_percent), int(1131 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(1131 * height_adjustment_percent))]
        ],
        "south": [
            [(int(309 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1490 * width_adjustment_percent), int(4 * height_adjustment_percent))],
            [(int(350 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1530 * width_adjustment_percent), int(4 * height_adjustment_percent))],
            [(int(730 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1910 * width_adjustment_percent), int(4 * height_adjustment_percent))],
            [(int(770 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1953 * width_adjustment_percent), int(4 * height_adjustment_percent))]
        ],
        "west": [
            [(int(1127 * width_adjustment_percent), int(472 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(472 * height_adjustment_percent))],
            [(int(1127 * width_adjustment_percent), int(510 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(510 * height_adjustment_percent))],
            [(int(1127 * width_adjustment_percent), int(1011 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(1011 * height_adjustment_percent))],
            [(int(1127 * width_adjustment_percent), int(1050 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(1050 * height_adjustment_percent))]
        ],
        "north": [
            [(int(389 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1570 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(430 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1608 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(809 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1990 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(2032 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ]
    }

    cars = []
    for direction, points in car_positions.items():
        for static, ml in points:
            cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
            cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))
    return cars

class TrafficLight:
    def __init__(self, x, y, orientation, screen, images, width_percent, height_percent):
        """
        Initialize a TrafficLight object.
        :param x: X-coordinate of the traffic light.
        :param y: Y-coordinate of the traffic light.
        :param orientation: 'vertical' or 'horizontal' to determine the light's orientation.
        :param screen: Pygame screen object where the light will be drawn.
        :param images: Dictionary containing images for 'red', 'yellow', and 'green' states.
        """
        self.x = x
        self.y = y
        self.orientation = orientation
        self.screen = screen
        self.images = images
        self.state = "red"  # Default state

        self.images = {state: img.copy() for state, img in images.items()}

        for state in self.images:
            self.images[state] = self.images[state].convert_alpha()  # Convert to 32-bit surface
            original_width, original_height = self.images[state].get_size()
            scaled_width = int(original_width * width_percent)
            scaled_height = int(original_height * height_percent)
            self.images[state] = pygame.transform.smoothscale(self.images[state], (scaled_width, scaled_height))


    def switch_state(self, next_state):
        """Change the traffic light to a new state."""
        self.state = next_state

    def render(self):
        """Draw the traffic light on the screen based on its current state."""
        self.screen.blit(self.images[self.state], (self.x, self.y))

def generate_traffic_lights(screen_width, screen_height, images, screen):
    """
    Generate TrafficLight objects for vertical and horizontal lights based on screen dimensions.
    :param screen_width: The width of the screen.
    :param screen_height: The height of the screen.
    :param images: Dictionary containing all loaded images.
    :param screen: Pygame screen object where traffic lights will be drawn.
    :return: Two lists - vertical_lights and horizontal_lights.
    """
    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    traffic_light_positions = {
        "vertical": [
            #static northside lights
            (int( 282* width_adjustment_percent), int( 464* height_adjustment_percent)),
            (int( 459* width_adjustment_percent), int( 539* height_adjustment_percent)),
            (int( 702* width_adjustment_percent), int( 464* height_adjustment_percent)),
            (int( 880* width_adjustment_percent), int( 539* height_adjustment_percent)),
            
            #static southside lights
            (int( 282* width_adjustment_percent), int( 1003* height_adjustment_percent)),
            (int( 459* width_adjustment_percent), int( 1079* height_adjustment_percent)),
            (int( 702* width_adjustment_percent), int( 1003* height_adjustment_percent)),
            (int( 880* width_adjustment_percent), int( 1079* height_adjustment_percent)),
        ],
        "horizontal": [
            #static northside lights
            (int( 379* width_adjustment_percent), int( 443* height_adjustment_percent)),
            (int( 302* width_adjustment_percent), int( 620* height_adjustment_percent)),
            (int( 799* width_adjustment_percent), int( 443* height_adjustment_percent)),
            (int( 722* width_adjustment_percent), int( 620* height_adjustment_percent)),

            #static southside lights
            (int( 379* width_adjustment_percent), int( 983* height_adjustment_percent)),
            (int( 302* width_adjustment_percent), int( 1161* height_adjustment_percent)),
            (int( 799* width_adjustment_percent), int( 983* height_adjustment_percent)),
            (int( 722* width_adjustment_percent), int( 1161* height_adjustment_percent)),
        ]
    }

    vertical_images = {
        "red": images["traffic_light_red_vertical"],
        "yellow": images["traffic_light_yellow_vertical"],
        "green": images["traffic_light_green_vertical"]
    }

    horizontal_images = {
        "red": images["traffic_light_red_horizontal"],
        "yellow": images["traffic_light_yellow_horizontal"],
        "green": images["traffic_light_green_horizontal"]
    }

    vertical_lights = []
    horizontal_lights = []

    for x, y in traffic_light_positions["vertical"]:
        vertical_lights.append(TrafficLight(x, y, "vertical", screen, vertical_images, width_adjustment_percent, height_adjustment_percent))

    for x, y in traffic_light_positions["horizontal"]:
        horizontal_lights.append(TrafficLight(x, y, "horizontal", screen, horizontal_images, width_adjustment_percent, height_adjustment_percent))

    return vertical_lights, horizontal_lights

def traffic_light_timer(vertical_lights, horizontal_lights):
    """
    Control the state of traffic lights with alternating timers.
    :param vertical_lights: List of vertical TrafficLight objects.
    :param horizontal_lights: List of horizontal TrafficLight objects.
    """
    # Durations for each light state (in seconds)
    durations = {"green": 5, "yellow": 2, "red": 7}

    while True:
        # Vertical lights green, horizontal lights red
        for light in vertical_lights:
            light.switch_state("green")
        for light in horizontal_lights:
            light.switch_state("red")
        time.sleep(durations["green"])

        # Vertical lights yellow, horizontal lights still red
        for light in vertical_lights:
            light.switch_state("yellow")
        time.sleep(durations["yellow"])

        # Vertical lights red, horizontal lights green
        for light in vertical_lights:
            light.switch_state("red")
        for light in horizontal_lights:
            light.switch_state("green")
        time.sleep(durations["green"])

        # Horizontal lights yellow, vertical lights still red
        for light in horizontal_lights:
            light.switch_state("yellow")
        time.sleep(durations["yellow"])

def process_background(background, screen_size):
    rotated_background = pygame.transform.rotate(background, 90)
    scaled_background = pygame.transform.smoothscale(rotated_background, screen_size)
    return scaled_background

class Car:
    def __init__(self, x, y, direction, width_percent, height_percent):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = pygame.image.load(f"images/car_{direction}side.png")
        original_width , original_height = self.image.get_size()
        scaled_width = int(original_width * width_percent)
        scaled_height = int(original_height * height_percent)
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    screen = initialize_pygame()
    images = load_images()

    screen_width, screen_height = screen.get_size()
    background = process_background(images["background"], (screen_width, screen_height))

    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    cars = generate_cars(screen_width, screen_height)

    # Generate TrafficLight objects
    vertical_lights, horizontal_lights = generate_traffic_lights(screen_width, screen_height, images, screen)

    # Start traffic light timer thread
    timer_thread = threading.Thread(target=traffic_light_timer, args=(vertical_lights, horizontal_lights))
    timer_thread.daemon = True
    timer_thread.start()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))

         # Render vertical traffic lights
        for light in vertical_lights:
            light.render()

        # Render horizontal traffic lights
        for light in horizontal_lights:
            light.render()

        for car in cars:
            car.render(screen)

        pygame.display.flip()
        time.sleep(0.02)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()