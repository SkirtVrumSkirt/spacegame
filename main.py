import pygame
import random
import math
import sys

# Initializations

pygame.init()
pygame.font.init()
pi = math.pi

# Functions

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
        return (1,-1)
    
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

    """
        Finds the angle between two lines given as slopes.
        This is done to figure out how much of the computer screen a planet
        will fill up, based on the position of the user, the FOV,
        and the radius of the planet.
    """

    numerator = abs(m1 - m2)
    denominator = 1 + (m1 * m2)

    if denominator == 0:
        theta = math.degrees(math.pi / 2)
    else:
        theta = math.degrees(math.atan(numerator / abs(denominator)))
    
    return theta

def draw_planet(surface,color,ship_direction,ship_pos,planet_pos,planet_rad):

    """
    This function draws planets or suns based off of several parameters.
    The following portion of the process is used to determine the position
    of the planet on the screen.

    ship_camera_angle: The vector of an imaginary line drawn between the position of the planet 
    and the ship being flown. This is useful in determining the position, as in a "quadrant", 
    of the planet relative to the ship. (For example, quadrant 1 would be up and to the right
    on a cartesian plane, which is independent from the orientation of the spaceship.)

        ship_camera_angle[0],ship_camera_angle[1]: the x,y value of the ship_camera_angle vector

    relative_angle: An angle from 0 - 360 degrees. Imagine a 360 screen completely wrapped around
    the ship, the relative_angle dictates where on that screen the planet will be shown.

    x_base: Converts the angle from the "relative_angle" variable to a position on the screen,
    dictating the center of the planet.
    """

    ship_camera_angle = [planet_pos[0] - ship_pos[0], planet_pos[1] - ship_pos[1]]

    if ship_camera_angle[0] == 0: # To avoid divided by zero error
        relative_angle = math.degrees(math.pi / 2)
    elif ship_camera_angle[1] > 0:
        if ship_camera_angle[0] > 0:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) # First Quadrant
        else:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) + 180 # Second Quadrant
    else:
        if ship_camera_angle[0] < 0:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) + 180 # Third Quadrant
        else:
            relative_angle = math.degrees(math.atan(ship_camera_angle[1] / ship_camera_angle[0])) # Fourth Quadrant

    """
    The following process is used to determine the size of the planet on the screen.

    d: The distance from the spaceship to the planet.

    slopes: Two imaginary lines, originating at the spaceship,
    and tangent to single points on opposite edges of the planet. Think of them like "chopsticks"
    that the spaceship is using to hold the planet.

    theta: The angle between these two lines/chopsticks.

    
    """

    x_base = (WIDTH * (((0.5 * FOV) + ship_direction - relative_angle) / FOV))

    d = math.sqrt(ship_camera_angle[0] ** 2 + ship_camera_angle[1] ** 2)
    slopes = tangent_slopes_to_circle(ship_pos[0],ship_pos[1],planet_pos[0],planet_pos[1],planet_rad)
    theta = degrees_between_slopes(slopes[0],slopes[1])
    rad_on_screen = WIDTH * theta / (2 * FOV) + 1  

    if (x_base % (360 * WIDTH / FOV)) > ((360 * WIDTH / FOV) - rad_on_screen):
        x = (x_base % (360 * WIDTH / FOV)) - (360 * WIDTH / FOV)
    else:
        x = x_base % (360 * WIDTH / FOV)

    pygame.draw.circle(surface, color, (x, round(HEIGHT / 2)), rad_on_screen)



# Draws the arrow on the ship interface indicating ship direction
def draw_ship(surface, position, angle):
    ship_width = 20
    ship_height = 25
    
    points = [
        (0, round(-0.6*ship_height)), (round(ship_width/2), round(0.4*ship_height)), (round(-ship_width/2), round(0.4*ship_height))
    ]

    # Rotate points
    rotated = [pygame.Vector2(p).rotate(angle) + position for p in points]
    pygame.draw.circle(surface,LIGHT_BLACK,position,round(1.2*ship_height))
    pygame.draw.circle(surface,RED,position,round(1.2*ship_height),round(0.1*ship_height))
    pygame.draw.polygon(surface, DARK_WHITE, rotated)

# Draws the thrust on the ship interface indicating ship thrust
def draw_thrust(surface,x,y,range,thrust,in_color,out_color):
    thruster_width = 80
    thruster_height = 20
    bevel = 5
    thickness = 5

    rectangle = [round(x - (thruster_width / 2)), round(y - (thruster_height / 2) - (range * thrust)),thruster_width,thruster_height]

    pygame.draw.rect(surface,in_color,rectangle,border_radius=bevel)
    pygame.draw.rect(surface,out_color,rectangle,border_radius=bevel,width=thickness)

# Screen dimensions

WIDTH, HEIGHT = 960, 540
CENTER_X, CENTER_Y = round(WIDTH/2),round(HEIGHT/2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Object in Space")
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# General settings

FPS = 60

# Colors

BLACK = (0, 0, 0)
LIGHT_BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
DARK_WHITE = (200, 200, 200)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
YELLOW = (255, 255, 0)

BRIGHT_YELLOW = (255, 255, 100)
DARK_RED = (139, 0, 0)
ORANGE = (255, 165, 0)
SKY_BLUE = (130, 200, 229)
IRON_RED = (116, 65, 62)
JUPITER_BROWN = (172, 133, 133)
APRICOT = (237, 219, 173)
PALE_BLUE = (122, 201, 206)
PURPLE_COBALT = (63, 84, 186)
DARK_MINT = (102, 87, 78)

# Spaceship ui positions

ship_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2 + 65)

# Spaceship properties
ship_vel = pygame.Vector2(0, 0)
grid_pos = pygame.Vector2(0, 100000)
ship_angle = 0
thrust = 100000000
rotation_speed = 0.0
rotation_accel = 0.05  # degrees/frame
thrust_pos = 0.0
thrust_application_speed = 0.02

# Space properties
NUM_STARS = 900
gridSpacing = 100
FOV = 60
starColorVariety = 100
starBlurMultiplier = 0.3
starBlurExponentiator = 1.05
time_multiplier = 1.0

# Create stars
stars = [(random.randint(0, round((360 / FOV) * WIDTH)),random.randint(0, HEIGHT),random.randint(1, 4),WHITE[0] - random.randint(1, starColorVariety),WHITE[0] - random.randint(1, starColorVariety),WHITE[0] - random.randint(1, starColorVariety))
         for _ in range(NUM_STARS)
]
star_modifier = round(WIDTH / FOV)

# Control panel properties
arrow_length = 50
arrow_start = 100,150
arrow_end = 150,150
arrow_head_length = 5
arrow_head_width = 10
arrow_color = RED

# Planet Data

# planet_list = [["Planet 1","Radius (m)","Starting position (x, y) (m)","Mass (kg)","Color (RGB)","Orbital Period (s)"],["Planet 2","Radius","Starting position","Mass","Color"]]
planet_list = [["Sun", 6.96 * (10 ** 8), pygame.Vector2(0, 0), 1.99 * (10 ** 30), BRIGHT_YELLOW,100], 
               ["Mercury", 1.74 * (10 ** 6), pygame.Vector2(0, 5.79 * (10 * 10)), 3.30 * (10 ** 23), DARK_RED],
               ["Venus", 6.05 * (10 ** 6), pygame.Vector2(0, 1.08 * (10 ** 11)), 4.87 * (10 ** 24), ORANGE],
               ["Earth", 6.37 * (10 ** 6), pygame.Vector2(0, 1.50 * (10 ** 11)), 5.97 * (10 ** 24), SKY_BLUE],
               ["Mars", 3.39 * (10 ** 6), pygame.Vector2(0, 2.28 * (10 ** 11)), 6.42 * (10 ** 23), IRON_RED],
               ["Jupiter", 6.99 * (10 ** 7), pygame.Vector2(0,7.78 * (10 ** 11)), 1.90 * (10 ** 27), JUPITER_BROWN],
               ["Saturn", 5.82 * (10 ** 7), pygame.Vector2(0,1.43 * (10 ** 12)), 5.68 * (10 ** 26), APRICOT],
               ["Uranus", 2.54 * (10 ** 7), pygame.Vector2(0,2.87 * (10 ** 12)), 8.68 * (10 ** 25), PALE_BLUE],
               ["Neptune", 2.48 * (10 ** 7), pygame.Vector2(0,4.50 * (10 ** 12)), 1.02 * (10 ** 26), PURPLE_COBALT],
               ["Pluto", 1.19 * (10 ** 6), pygame.Vector2(0,5.91 * (10 ** 12)), 1.19 * (10 ** 22), DARK_MINT]]

sun_radius = 432690
sun_pos = pygame.Vector2(0,4435000)
sun_color = YELLOW

# Arrow
arrowImage = pygame.image.load("C:/Users/crawf/Documents/PythonProjects/spacegame/red_arrow.png")
resizedArrowImage = pygame.transform.scale(arrowImage,(50,50))
def draw_arrow(position,angle):
    screen.blit(resizedArrowImage, position)

# Cockpit
cockpit = pygame.image.load("C:/Users/crawf/Documents/PythonProjects/spacegame/cockpit.002.png")
resizedCockpit = pygame.transform.scale(cockpit,(960,540))
def draw_cockpit(position):
    screen.blit(resizedCockpit,position)

# Game loop
clock = pygame.time.Clock()
running = True
t_0 = 0

while running:

    screen.fill(BLACK)

    t_1 = pygame.time.get_ticks()
    FPS = round((1000 / (t_1 - t_0)),3)
    t_0 = t_1

    shipSpeed = math.sqrt((ship_vel[0] ** 2) + (ship_vel[1] ** 2)) # pythagorean using x and y components of ship speed

    # Sets the direction of the ship

    if ship_vel[0] < 0: # I don't know how this stuff works, don't touch
        shipDirection = -(180 / pi) * math.atan(ship_vel[1] / (ship_vel[0] + 0.00001)) + 180
    elif ship_vel[1] > 0:
        shipDirection = 360 - (180 / pi) * math.atan(ship_vel[1] / (ship_vel[0] + 0.00001))
    else:
        shipDirection = -(180 / pi) * math.atan(ship_vel[1] / (ship_vel[0] + 0.00001))

    text_surface = my_font.render(str((90-ship_angle) % 360), False, WHITE)
    shipSpeed_surface = my_font.render(str(round(shipSpeed,2)),False,WHITE)
    gridPos_surface = my_font.render(str(round(grid_pos,2)), False, WHITE)
    shipVelocity_surface = my_font.render(str(round(ship_vel,2)),False,WHITE)
    shipDirection_surface = my_font.render(str(round(shipDirection,2)),False,WHITE)
    FPS_surface = my_font.render(str(FPS),False,WHITE)
    time_surface = my_font.render(str(time_multiplier),False,WHITE)
    
    # Draw stars
    for x, y, radius, r, g, b in stars:
        star_pos_x = (x - (round(WIDTH / FOV) * ship_angle)) % (360 * WIDTH / FOV)
        star_blur = (starBlurMultiplier * abs(rotation_speed) * (WIDTH / FOV)) ** starBlurExponentiator + radius
        ellipse_rect = pygame.Rect(star_pos_x, y, star_blur, radius)
        star_shade = round(0.1 * abs(rotation_speed))
        star_color = (r - star_shade,g - star_shade,b - star_shade)
        pygame.draw.ellipse(screen,star_color,ellipse_rect)

    keys = pygame.key.get_pressed()

    # Input handling

    if keys[pygame.K_LEFT]:
        rotation_speed -= rotation_accel

    if keys[pygame.K_RIGHT]:
        rotation_speed += rotation_accel

    if keys[pygame.K_UP]:
        # Apply thrust in direction of ship's nose
        if thrust_pos < 1.0:
            thrust_pos += thrust_application_speed
        else:
            thrust_pos = 1.0

    if keys[pygame.K_DOWN]:
        if thrust_pos > 0.0:
            thrust_pos -= thrust_application_speed
        else:
            thrust_pos = 0.0
    
    if keys[pygame.K_p]:
        time_multiplier = time_multiplier + (time_multiplier * 0.01)
    
    if keys[pygame.K_o]:
        if time_multiplier > 1:
            time_multiplier = time_multiplier - (time_multiplier * 0.01)
        else:
            time_multiplier = 1.0
    
    if keys[pygame.K_l]:
        time_multiplier = 1.0
    
    if keys[pygame.K_b]:
        ship_vel[0] = 0
        ship_vel[1] = 0

    if keys[pygame.K_x]:
        ship_vel[0] = 0
    
    if keys[pygame.K_y]:
        ship_vel[1] = 0
    
    if keys[pygame.K_r]:
        rotation_speed = 0
        ship_vel[0] = 0
        ship_vel[1] = 0
        time_multiplier = 1.0
        ship_angle = 0
        thrust_pos = 0.0
    
    angle_rad = math.radians(ship_angle)
    force = pygame.Vector2(math.sin(angle_rad), math.cos(angle_rad)) * thrust_pos * thrust * time_multiplier
    ship_vel += (force / FPS)

    # Update position
    grid_pos += (ship_vel / FPS) * time_multiplier
    ship_angle += (rotation_speed) * time_multiplier


    # Drawing

    # Draw Planets
    # draw_planet(screen,YELLOW, 90-ship_angle,grid_pos,sun_pos,sun_radius)
    # draw_planet(screen, planet_list[0][4], 90 - ship_angle, grid_pos, planet_list[0][2], planet_list[0][1])

    for x in planet_list:
        draw_planet(screen, x[4], 90 - ship_angle, grid_pos, x[2], x[1])

    # Draw cockpit
    # draw_cockpit((0,0))

    # Draw spaceship
    draw_ship(screen, ship_pos, ship_angle)

    # Draw thruster
    draw_thrust(screen, round(WIDTH / 2), round(HEIGHT * 0.84),0.1 * HEIGHT,thrust_pos,DARK_WHITE,BROWN)

    screen.blit(text_surface, (20,20))
    screen.blit(shipSpeed_surface,(20,80))
    screen.blit(shipVelocity_surface,(20,200))
    screen.blit(gridPos_surface,(20,140))
    screen.blit(time_surface,(20,260))
    screen.blit(shipDirection_surface,(20,320))
    screen.blit(FPS_surface, (round(WIDTH/2),20))

    # Close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
