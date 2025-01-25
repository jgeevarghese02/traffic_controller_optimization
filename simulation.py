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
        #Vechicles#
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
        
        #Streetlights#
        "streetlight_red_hor": pygame.image.load(""),
        "streetlight_yellow_hor": pygame.image.load(""),
        "streetlight_green_horni": pygame.image.load(""),
        "streetlight_red_vertical": pygame.image.load(""),
        "streetlight_yellow_vertical": pygame.image.load(""),
        "streetlight_green_vertical": pygame.image.load(""),

        "background": pygame.image.load("images/Grid_background.png")
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

<<<<<<< Updated upstream
    cars = []
    for direction, points in car_positions.items():
        for static, ml in points:
            cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
            cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))

    return cars
=======
    while True:  # Continuously generate cars
        direction = random.choice(list(car_positions.keys()))
        static, ml = random.choice(car_positions[direction])

        cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
        cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))

        time.sleep(1)



    # cars = []
    # for _ in range(100):  # Run for 100 seconds
    #     direction = random.choice(list(car_positions.keys()))
    #     static, ml = random.choice(car_positions[direction])

    #     cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
    #     cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))

    #     time.sleep(1)


    # direction = random.choice(list(car_positions.keys()))
    # static , ml = random.choice(car_positions[direction])
    # cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
    # cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))
    # time.sleep(0.5)

    #return cars

    # for direction, points in car_positions.items():
    #     for static, ml in points:
    #         cars.append(Car(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent))
    #         cars.append(Car(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent))

def generate_streetlights(screen, screen_width, screen_height):
    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)
    streetlight_positions = {
        "horizontal": [

            [(int(389 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(430 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(809 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ]
        "vertical": [
            
            [(int(389 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(430 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(809 * width_adjustment_percent), int(1600 * height_adjustment_percent))],
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ]
    }
>>>>>>> Stashed changes

    streetlights = []
    streetlight_images = {
        "red": images["streetlight_red"],
        "yellow": images["streetlight_yellow"],
        "green": images["streetlight_green"]
    }

    for position in positions:
        x, y, orientation = position
        streetlights.append(Streetlight(x, y, orientation, screen, streetlight_images))
    return streetlights

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

<<<<<<< Updated upstream
=======
class streetlight:
    def __init__(self, x, y, orientation, screen, images);
        self.x = x
        self.y = y
        self.orientation = orientation
        self.screen = screen
        self.images = images
        self.state = "red"  # Start with red light
        self.timer = 0  # Timer to track switching
    def switch_state(self)
        """Switch the streetlight state based on the timer."""
        if self.state == "red":
            self.state = "green"
        elif self.state == "green":
            self.state = "yellow"
        elif self.state == "yellow":
            self.state = "red"
    def render(self):
        """Draw the current light on the screen."""
        self.screen.blit(self.images[self.state], (self.x, self.y))

def update_streetlights(streetlights):
     """
    Continuously update the state of all streetlights.
    :param streetlights: List of Streetlight objects.
    """
    while True:
        for light in streetlights:
            light.switch_state()  # Switch to the next state
        time.sleep(5)  # Wait 5 seconds before switching again

def vehicle_vanishing(vehicle,x,y, screen_width, screen_height):
    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)
    vanishing_points = [
        (int(389 * width_adjustment_percent), int(4 * height_adjustment_percent)) , (int(809 * width_adjustment_percent), int(4 * height_adjustment_percent)) ,
        (int(1570 * width_adjustment_percent), int(4 * height_adjustment_percent)) , (int(1990 * width_adjustment_percent), int(4 * height_adjustment_percent)) ,
        (int(430 * width_adjustment_percent), int(4 * height_adjustment_percent)) , (int(851 * width_adjustment_percent), int(4 * height_adjustment_percent)) ,
        (int(1608 * width_adjustment_percent), int(4 * height_adjustment_percent)) , (int(2032 * width_adjustment_percent), int(4 * height_adjustment_percent)) ,
        (int(309 * width_adjustment_percent), int(1600 * height_adjustment_percent)) , (int(730 * width_adjustment_percent), int(1600 * height_adjustment_percent)) ,
        (int(1490 * width_adjustment_percent), int(1600 * height_adjustment_percent)) , (int(1910 * width_adjustment_percent), int(1600 * height_adjustment_percent)) ,
        (int(350 * width_adjustment_percent), int(1600 * height_adjustment_percent)) , (int(770 * width_adjustment_percent), int(1600 * height_adjustment_percent)) ,
        (int(1530 * width_adjustment_percent), int(1600 * height_adjustment_percent)) , (int(1953 * width_adjustment_percent), int(1600 * height_adjustment_percent)) ,
        (int(1127 * width_adjustment_percent), int(552 * height_adjustment_percent)) , (int(1127 * width_adjustment_percent), int(1092 * height_adjustment_percent)) ,
        (int(2317 * width_adjustment_percent), int(552 * height_adjustment_percent)) , (int(2317 * width_adjustment_percent), int(1092 * height_adjustment_percent)) ,
        (int(1127 * width_adjustment_percent), int(591 * height_adjustment_percent)) , (int(1127 * width_adjustment_percent), int(1131 * height_adjustment_percent)) ,
        (int(2317 * width_adjustment_percent), int(591 * height_adjustment_percent)) , (int(2317 * width_adjustment_percent), int(1131 * height_adjustment_percent)) ,
        (int(4 * width_adjustment_percent), int(472 * height_adjustment_percent)) , (int(4 * width_adjustment_percent), int(1011 * height_adjustment_percent)) ,
        (int(1191 * width_adjustment_percent), int(472 * height_adjustment_percent)) , (int(1191 * width_adjustment_percent), int(1011 * height_adjustment_percent)) ,
        (int(4 * width_adjustment_percent), int(510 * height_adjustment_percent)) , (int(4 * width_adjustment_percent), int(1050 * height_adjustment_percent)) ,
        (int(1191 * width_adjustment_percent), int(510 * height_adjustment_percent)) , (int(1191 * width_adjustment_percent), int(1050 * height_adjustment_percent))
    ]

    for vx , vy in vanishing_points:
        if abs(x-vx) <=1 and abs (y - vy) <= 1:
            return True
    return False

>>>>>>> Stashed changes
def main():
    screen = initialize_pygame()
    images = load_images()

    screen_width, screen_height = screen.get_size()
    background = process_background(images["background"], (screen_width, screen_height))

    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    cars = generate_cars(screen_width, screen_height)

    streetlight = []
    streetlight_thread = Thread(target=update_streetlights, args=(streetlights, screen_width, screen_height))
    streetlight_thread.daemon = True
    streetlight_thread.start()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0, 0))

        for car in cars:
            car.render(screen)

        for light in streetlights:
            light.render()

        pygame.display.flip()
        time.sleep(0.02)

    pygame.quit()



if __name__ == "__main__":
    main()