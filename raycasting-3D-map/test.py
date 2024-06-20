import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Map with Player and Square")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player and Square positions
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
    pygame.draw.circle(screen, BLACK, (int(player_pos[0]), int(player_pos[1])), 25)  # Player as a circle
    pygame.draw.rect(screen, BLACK, pygame.Rect(cube_pos[0]-25, cube_pos[1]-25, 50, 50))  # Square entity

    # Draw player's vision rays
    for i in range(num_rays):
        angle = math.radians(player_direction - vision_angle / 2 + (i / (num_rays - 1)) * vision_angle)
        end_x = player_pos[0] + ray_length * math.cos(angle)
        end_y = player_pos[1] + ray_length * math.sin(angle)
        pygame.draw.line(screen, RED, player_pos, (end_x, end_y), 2)

    player_plane_x = math.sin(player_direction)
    player_plane_y = -math.cos(player_direction)

    # Raycasting for 3D view
    for i in range(screen.get_width()):
        camera_x = 2 * i / screen.get_width() - 1  # Map screen space to camera space
        ray_dir_x = math.cos(player_direction) + player_plane_x * camera_x
        ray_dir_y = math.sin(player_direction) + player_plane_y * camera_x

        # Calculate the position of the wall hit by the ray
        map_x, map_y = player_pos[0], player_pos[1]
        delta_dist_x = abs(1 / ray_dir_x)
        delta_dist_y = abs(1 / ray_dir_y)
        
        step_x = 1 if ray_dir_x > 0 else -1
        step_y = 1 if ray_dir_y > 0 else -1

        side_dist_x = (map_x + 1 - player_pos[0]) * delta_dist_x
        side_dist_y = (map_y + 1 - player_pos[1]) * delta_dist_y

        hit = False
        side = None

        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if map[map_x][map_y] == 1:
                hit = True

        # Calculate distance to the wall
        if side == 0:
            perp_wall_dist = (map_x - player_pos[0] + (1 - step_x) / 2) / ray_dir_x
        else:
            perp_wall_dist = (map_y - player_pos[1] + (1 - step_y) / 2) / ray_dir_y

        # Calculate height of the wall slice to draw
        line_height = int(screen.get_height() / perp_wall_dist)

        # Draw the wall slice
        wall_color = (255, 0, 0)  # Red wall color
        pygame.draw.line(screen, wall_color, (i, screen.get_height() // 2 - line_height // 2), (i, screen.get_height() // 2 + line_height // 2))

    pygame.display.flip()