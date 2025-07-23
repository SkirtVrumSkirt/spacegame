import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 960, 540
CENTER_X, CENTER_Y = round(WIDTH/2),round(HEIGHT/2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Object in Space")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_WHITE = (200, 200, 200)
RED = (255,0,0)

# Spaceship properties
ship_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ship_vel = pygame.Vector2(0, 0)
grid_pos = pygame.Vector2(0,0)
ship_angle = 0
thrust = 0.1
rotation_speed = 10  # degrees/frame

# Space properties
NUM_STARS = 100
gridSpacing = 100
FOV = 60

# Format properties
zoom = 1.0
offset = [0.0,0.0]
gridBlockSize = gridSpacing*zoom

# Create stars
stars = [(random.randint(0,round((360/FOV)*WIDTH)),random.randint(0,HEIGHT),random.randint(1,2))
         for _ in range(NUM_STARS)
]

#stars = [pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(stars)]
#stars = [pygame.Vector2(random.randint(0, round((360/FOV)*WIDTH)), random.randint(0, HEIGHT)) for _ in range(stars)]

# Text initialization
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Grid Block Size
zooming = 0

# Control panel properties
arrow_length = 50
arrow_start = 100,150
arrow_end = 150,150
arrow_head_length = 5
arrow_head_width = 10
arrow_color = RED

# Misc.
pi = math.pi

# Spaceship shape
def draw_ship(surface, position, angle):
    points = [
        (0, -15), (10, 10), (-10, 10)
    ]
    # Rotate points
    rotated = [pygame.Vector2(p).rotate(angle) + position for p in points]
    pygame.draw.polygon(surface, WHITE, rotated)

def draw_grid(surface):

    # Grid Block Size

    gridBlockSize = gridSpacing*zoom/(2**(round(math.log2(zoom))))

    if grid_pos[0] < offset[0]:
        offset[0] -= gridBlockSize
    if grid_pos[0] > offset[0]:
        offset[0] += gridBlockSize
    
    if grid_pos[1] < offset[1]:
        offset[1] -= gridBlockSize
    if grid_pos[1] > offset[1]:
        offset[1] += gridBlockSize

    for x in range(round(WIDTH/(gridSpacing*zoom))):
    
        points = [          
            (-offset[0]+CENTER_X+grid_pos[0]+gridBlockSize*x,HEIGHT), 
            (-offset[0]+CENTER_X+grid_pos[0]+gridBlockSize*x,0),
            (-offset[0]+CENTER_X+grid_pos[0]-gridBlockSize*x,HEIGHT), 
            (-offset[0]+CENTER_X+grid_pos[0]-gridBlockSize*x,0)
        ]

        pygame.draw.line(surface,DARK_WHITE,points[0],points[1])
        pygame.draw.line(surface,DARK_WHITE,points[2],points[3])

    for y in range(round(HEIGHT/gridSpacing/zoom)):

        points = [
            (WIDTH,-offset[1]+CENTER_Y+grid_pos[1]+gridBlockSize*y), 
            (0,-offset[1]+CENTER_Y+grid_pos[1]+gridBlockSize*y),
            (WIDTH,-offset[1]+CENTER_Y+grid_pos[1]-gridBlockSize*y), 
            (0,-offset[1]+CENTER_Y+grid_pos[1]-gridBlockSize*y)
        ]

        pygame.draw.line(surface,DARK_WHITE,points[0],points[1])
        pygame.draw.line(surface,DARK_WHITE,points[2],points[3])

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
while running:
    screen.fill(BLACK)

    shipSpeed = math.sqrt((ship_vel[0]**2)+(ship_vel[1]**2))
    if ship_vel[0] < 0:
        shipDirection = -(180/pi)*math.atan(ship_vel[1]/(ship_vel[0]+0.00001))+180
    elif ship_vel[1] > 0:
        shipDirection = 360-(180/pi)*math.atan(ship_vel[1]/(ship_vel[0]+0.00001))
    else:
        shipDirection = -(180/pi)*math.atan(ship_vel[1]/(ship_vel[0]+0.00001))

    # Grid Block Size
    gridBlockSize = gridSpacing*zoom

    text_surface = my_font.render(str((90-ship_angle) % 360), False, WHITE)
    shipSpeed_surface = my_font.render(str(round(shipSpeed,2)),False,WHITE)
    zoom_surface = my_font.render(str(round(zoom,2)),False,WHITE)
    gridPos_surface = my_font.render(str(round(grid_pos,2)),False,WHITE)
    shipVelocity_surface = my_font.render(str(round(ship_vel,2)),False,WHITE)
    shipDirection_surface = my_font.render(str(round(shipDirection,2)),False,WHITE)

    screen.blit(text_surface, (20,20))
    screen.blit(shipSpeed_surface,(20,80))
    screen.blit(zoom_surface,(20,140))
    screen.blit(shipVelocity_surface,(20,200))
    screen.blit(gridPos_surface,(20,260))
    screen.blit(shipDirection_surface,(20,320))
    
    # Draw stars
    #for x, y, radius in stars:
        #pygame.draw.circle(screen,WHITE,(x,y),radius)

    #for star in stars:
        #modifierr = round(WIDTH / FOV)
        #pygame.draw.circle(screen, WHITE, (int(star.x), int(star.y)), 1)
        #pygame.draw.circle(screen, WHITE, (int(star.x+(modifierr*ship_angle)%(360*modifierr)), int(star.y)), 1)


    # Close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Input handling
    if keys[pygame.K_LEFT]:
        ship_angle -= rotation_speed
    if keys[pygame.K_RIGHT]:
        ship_angle += rotation_speed
    if keys[pygame.K_UP]:
        # Apply thrust in direction of ship's nose
        angle_rad = math.radians(-ship_angle)
        force = pygame.Vector2(-math.sin(angle_rad), -math.cos(angle_rad)) * thrust
        ship_vel += force

    # Zoom changing
    if keys[pygame.K_PERIOD]:
        zoom += 0.01*zoom
    if keys[pygame.K_COMMA]:
        zoom -= 0.01*zoom

    # Update position
    grid_pos -= ship_vel*zoom

    # Screen wrap
    if ship_pos.x > WIDTH: ship_pos.x = 0
    if ship_pos.x < 0: ship_pos.x = WIDTH
    if ship_pos.y > HEIGHT: ship_pos.y = 0
    if ship_pos.y < 0: ship_pos.y = HEIGHT

    # Draw spaceship
    draw_ship(screen, ship_pos, ship_angle)

    # Draw arrow
    draw_arrow((50,50),0)

    # Draw cockpit
    draw_cockpit((0,0))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
