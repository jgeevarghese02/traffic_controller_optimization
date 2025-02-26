import random
import time
import threading
import pygame
import sys
import tkinter as tk
from threading import Thread

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

def save_time_to_file(filename, time_value):
    with open(filename, "a") as file:
        file.write(f"{time_value}\n")
        file.close()

def initialize_pygame():
    pygame.init()
    screen_width, screen_height = get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Traffic Simulation")
    return screen

def load_images():
    images = {
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

        "background": pygame.image.load("images/Grid_background.png")
    }
    return images

vehicle_timers = {}
################################################################################################################################################
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
########################################################################################################################################################

def generate_vehicles(vehicles, screen_width, screen_height):
    # Calculate scaling percentages using the function
    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    # Adjusted car positions after scaling
    car_positions = {
        "east_1": [
            [(int(4 * width_adjustment_percent), int(552 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(552 * height_adjustment_percent))]
        ],
        "east_2": [
            [(int(4 * width_adjustment_percent), int(591 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(591 * height_adjustment_percent))]
        ],
        "east_3": [
            [(int(4 * width_adjustment_percent), int(1092 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(1092 * height_adjustment_percent))]
        ],
        "east_4": [
            [(int(4 * width_adjustment_percent), int(1131 * height_adjustment_percent)), 
             (int(1191 * width_adjustment_percent), int(1131 * height_adjustment_percent))]
        ],
        "south_1":[
            [(int(309 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1490 * width_adjustment_percent), int(4 * height_adjustment_percent))]
        ],
        "south_2":[
            [(int(350 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1530 * width_adjustment_percent), int(4 * height_adjustment_percent))]
        ],
        "south_3":[
            [(int(730 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1910 * width_adjustment_percent), int(4 * height_adjustment_percent))]
        ],
        "south_4":[
            [(int(770 * width_adjustment_percent), int(4 * height_adjustment_percent)), 
             (int(1953 * width_adjustment_percent), int(4 * height_adjustment_percent))]
        ],
        "west_1":[
            [(int(1127 * width_adjustment_percent), int(472 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(472 * height_adjustment_percent))]
        ],
        "west_2":[
            [(int(1127 * width_adjustment_percent), int(510 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(510 * height_adjustment_percent))]
        ],
        "west_3":[
            [(int(1127 * width_adjustment_percent), int(1011 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(1011 * height_adjustment_percent))]
        ],
        "west_4":[
            [(int(1127 * width_adjustment_percent), int(1050 * height_adjustment_percent)), 
             (int(2317 * width_adjustment_percent), int(1050 * height_adjustment_percent))]
        ],
        "north_1":[
            [(int(389 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1570 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ],
        "north_2":[
            [(int(430 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1608 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ],
        "north_3":[
            [(int(809 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(1990 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ],
        "north_4":[
            [(int(851 * width_adjustment_percent), int(1600 * height_adjustment_percent)), 
             (int(2032 * width_adjustment_percent), int(1600 * height_adjustment_percent))]
        ]
    }

    while True:  # Continuously generate cars
        direction = random.choice(list(car_positions.keys()))
        static, ml = random.choice(car_positions[direction])

        #vehicle_type = random.choice([Car, Truck, Motorcycle])
        vehicle_type = random.choice([Car])
        path = random.choice([1,2,3,4])


        static_vehicle = (vehicle_type(static[0], static[1], direction, width_adjustment_percent, height_adjustment_percent, "static", path))
        ml_vehicle = (vehicle_type(ml[0], ml[1], direction, width_adjustment_percent, height_adjustment_percent, "ml", path))

        vehicles.append(static_vehicle)
        vehicles.append(ml_vehicle)

        #start timers
        vehicle_timers[static_vehicle] = time.time()
        vehicle_timers[ml_vehicle] = time.time()
        time.sleep(1)

def process_background(background, screen_size):
    rotated_background = pygame.transform.rotate(background, 90)
    scaled_background = pygame.transform.smoothscale(rotated_background, screen_size)
    return scaled_background
###################################################################################################################################
class Car:
    car_speed = 2
    def __init__(self, x, y, direction, width_percent, height_percent, vehicle_side, path):
        self.x = x
        self.y = y
        self.x_scaled = int(x * width_percent)
        self.y_scaled = int(x * height_percent)
        self.inital_direction = direction
        self.vehicle_side = vehicle_side
        self.path = path

        trim_direction = str(direction[:-2])
        self.image = pygame.image.load(f"images/car_{trim_direction}side.png")
        original_width , original_height = self.image.get_size()
        scaled_width = int(original_width * width_percent)
        scaled_height = int(original_height * height_percent)
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

    def change_image_direcion(self, direction, width_percent, height_percent):
        trim_direction = str(direction[:-2])
        self.image = pygame.image.load(f"images/car_{direction}side.png")
        original_width , original_height = self.image.get_size()
        scaled_width = int(original_width * width_percent)
        scaled_height = int(original_height * height_percent)
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

    def move(self, car_speed, width_percent, height_percent):
        temp = 1


    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Truck:
    def __init__(self, x, y, direction, width_percent, height_percent):
        self.x = x
        self.y = y
        self.inital_direction = direction
        self.image = pygame.image.load(f"images/truck_{direction}side.png")
        original_width , original_height = self.image.get_size()
        scaled_width = int(original_width * width_percent)
        scaled_height = int(original_height * height_percent)
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

    def move(self):
        if self.inital_direction == "east":
            self.x += 1
        elif self.inital_direction == "south":
            self.y += 1
        elif self.inital_direction == "west":
            self.x -= 1
        elif self.inital_direction == "north":
            self.y -= 1

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Motorcycle:
    def __init__(self, x, y, direction, width_percent, height_percent):
        self.x = x
        self.y = y
        self.inital_direction = direction
        self.image = pygame.image.load(f"images/motorcycle_{direction}side.png")
        original_width , original_height = self.image.get_size()
        scaled_width = int(original_width * width_percent)
        scaled_height = int(original_height * height_percent)
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

    def move(self):
        if self.inital_direction == "east":
            self.x += 1.5
        elif self.inital_direction == "south":
            self.y += 1.5
        elif self.inital_direction == "west":
            self.x -= 1.5
        elif self.inital_direction == "north":
            self.y -= 1.5

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
##################################################################################################################################

def main():
    screen = initialize_pygame()
    images = load_images()

    screen_width, screen_height = screen.get_size()
    background = process_background(images["background"], (screen_width, screen_height))

    width_adjustment_percent, height_adjustment_percent = calculate_scaling_percentages(screen_width, screen_height)

    #cars = generate_cars(screen_width, screen_height)

    vehicles = []
    car_thread = Thread(target=generate_vehicles, args=(vehicles, screen_width, screen_height))
    car_thread.daemon = True
    car_thread.start()

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(background, (0, 0))
            
            for vehicle in vehicles[:]:
                if vehicle_vanishing(vehicle, vehicle.x, vehicle.y, screen_width, screen_height):
                    #gets time in simulation
                    end_time = time.time()
                    time_in_simulation = end_time - vehicle_timers.pop(vehicle, end_time)
                    if vehicle.x > screen_width / 2:
                        file_name = "ml_result_metrics.txt"
                    else:
                        file_name = "static_result_metrics.txt"
                    save_time_to_file(file_name, time_in_simulation)
                    #Remove Vehicle
                    vehicles.remove(vehicle)

                else:
                    vehicle.move(vehicle.car_speed, width_adjustment_percent, height_adjustment_percent)
                    vehicle.render(screen)
            pygame.display.flip()
            time.sleep(0.02)
    finally:
        vehicle_timers.clear()
        pygame.quit()



if __name__ == "__main__":
    main()