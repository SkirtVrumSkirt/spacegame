import pygame
import math

pygame.init()

WIDTH = 600
HEIGHT = 400
FOV = 90

screen = pygame.display.set_mode((600, 400))
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

def tangent_slopes_to_circle(x0, y0, a, b, r): # Chat GPT Code

    """
    Compute the slopes of the two lines tangent from point (x0, y0)
    to a circle centered at (a, b) with radius r.

    Returns:
        A tuple (m1, m2) of the two slopes (floats), where m1 > m2
    """
    # Vector from point to center
    dx = a - x0
    dy = b - y0
    d_sq = dx**2 + dy**2
    r_sq = r**2

    fill_screen = False

    if d_sq < r_sq:
        return "Overlap"
    
    else:
        # Angle to center
        theta = math.atan2(dy, dx)

        # Tangent angle offset
        delta = math.acos(r / math.sqrt(d_sq))

        # Two tangent directions
        angle1 = -(theta + delta)
        angle2 = -(theta - delta)

        m1 = math.tan(angle1)
        m2 = math.tan(angle2)

        # Return in descending order
        return (max(m1, m2), min(m1, m2))

def degrees_between_slopes(m1, m2): # Chat GPT Code
    numerator = abs(m1 - m2)
    denominator = 1 + (m1 * m2)

    if denominator == 0:
        theta = math.degrees(math.pi / 2)
    else:
        theta = math.degrees(math.atan(numerator / abs(denominator)))
    
    return theta

print(tangent_slopes_to_circle(0,0,100,100,10))

# Draw a filled red circle
def draw_planet(surface,color,ship_direction,ship_pos,planet_pos,planet_rad):

    ship_camera_angle = [planet_pos[0] - ship_pos[0], planet_pos[1] - ship_pos[1]]
    print("Ship Camera Angle: " + str(ship_camera_angle))

    if ship_camera_angle[0] == 0: # To avoid divided by zero error
        relative_angle = math.degrees(math.pi / 2)
    elif ship_camera_angle[1] > 0:
        if ship_camera_angle[0] > 0:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) # First Quadrant
        else:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) + 180 # Second Quadrant
    else:
        if ship_camera_angle[0] < 0:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) + 90 # Third Quadrant
        else:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) + 270 # Fourth Quadrant
    
    print("Relative Angle: " + str(relative_angle))

    x = round(WIDTH * (((0.5 * FOV) + ship_direction - relative_angle) / FOV))
    print("x: " + str(x))


    d = math.sqrt(ship_camera_angle[0] ** 2 + ship_camera_angle[1] ** 2)
    print("Distance: " + str(d))

    slopes = tangent_slopes_to_circle(ship_pos[0],ship_pos[1],planet_pos[0],planet_pos[1],planet_rad)
    print("Slopes: " + str(slopes))

    theta = degrees_between_slopes(slopes[0],slopes[1])
    print("Theta: " + str(theta))

    rad_on_screen = WIDTH * theta / (2 * FOV)
    # rad_on_screen = WIDTH * math.degrees(math.atan(planet_rad / d)) / (2 * FOV)
    print("Radius on screen: " + str(rad_on_screen))
    
    pygame.draw.circle(surface, color, (x, round(HEIGHT / 2)), rad_on_screen)

draw_planet(screen,white,45,[-1000,1000],[1000,2000],43)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()