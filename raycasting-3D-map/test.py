import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Map with Player and Cube")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player and Cube positions
player_pos = [50, 50]
cube_pos = (150, 50)

# Player movement speed
player_speed = 0.175

# Player vision angle
vision_angle = 60  # in degrees

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Draw the map with entities
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], 50, 50))  # Player
    pygame.draw.rect(screen, BLACK, (cube_pos[0], cube_pos[1], 50, 50))  # Cube

    # Draw player's vision cone
    vision_radius = 100
    start_angle = math.radians(-vision_angle / 2)
    end_angle = math.radians(vision_angle / 2)
    pygame.draw.arc(screen, RED, (player_pos[0] - vision_radius, player_pos[1] - vision_radius, 2 * vision_radius, 2 * vision_radius), start_angle, end_angle, 3)

    pygame.display.flip()