import math
import pygame

def angle_test():
    for x in range(-100,100):
        if x != 0:
            z = math.atan(x)
        print("arctan(" + str(x) + ") = " + str(z))


def number_sign(number):
    return math.copysign(1, number)


gravitational_constant = 6.6743 * (10 ** (-11))

def gravitational_acceleration(planet_mass,ship_pos,planet_pos):

    delta_x = planet_pos[0] - ship_pos[0]
    delta_y = planet_pos[1] - ship_pos[1]
    total_distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    acceleration_x = math.copysign(1, delta_x) * abs(gravitational_constant * planet_mass * delta_x / (total_distance ** 3))
    acceleration_y = math.copysign(1, delta_y) * abs(gravitational_constant * planet_mass * delta_y / (total_distance ** 3))

    accel_vector = pygame.Vector2(acceleration_x, acceleration_y)

    return accel_vector

print(gravitational_acceleration(1.99 * (10 ** 30), pygame.Vector2(0, 0), pygame.Vector2(0, 10 ** 9)))