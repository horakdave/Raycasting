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
num_rays = 30  # Number of rays for vision
ray_length = 100  # Length of each ray

# Initial player direction
player_direction = 0

# Turning speed
turning_speed = 0.175  # Adjust turning speed here

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_direction -= turning_speed  # Turn left
    if keys[pygame.K_RIGHT]:
        player_direction += turning_speed  # Turn right

    if keys[pygame.K_UP]:
        player_pos[0] += player_speed * math.cos(math.radians(player_direction))
        player_pos[1] += player_speed * math.sin(math.radians(player_direction))

    # Draw the map with entities
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], 50, 50))  # Player
    pygame.draw.rect(screen, BLACK, (cube_pos[0], cube_pos[1], 50, 50))  # Cube

    # Draw player's vision rays
    for i in range(num_rays):
        angle = math.radians(player_direction - vision_angle / 2 + (i / (num_rays - 1)) * vision_angle)
        end_x = player_pos[0] + ray_length * math.cos(angle)
        end_y = player_pos[1] + ray_length * math.sin(angle)
        pygame.draw.line(screen, RED, player_pos, (end_x, end_y), 2)

    pygame.display.flip()