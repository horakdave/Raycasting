import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Raycasting Simulation")

player_pos = [400, 300]
player_angle = 0
ray_length = 200

walls = [[[100, 100], [100, 500]],
         [[100, 500], [700, 500]],
         [[700, 500], [700, 100]],
         [[700, 100], [100, 100]]]

# Main game loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_angle -= 45  # Turn 45 degrees left
            elif event.key == pygame.K_RIGHT:
                player_angle += 45  # Turn 45 degrees right
            elif event.key == pygame.K_UP:
                player_pos[0] += 5 * math.cos(math.radians(player_angle))  # Move in the x-direction
                player_pos[1] += 5 * math.sin(math.radians(player_angle))  # Move in the y-direction

    screen.fill((0, 0, 0))

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (0, 255, 0), wall[0], wall[1], 2)

    # Cast rays
    for ray_angle in range(-30, 31, 1):  # rays from -30 .. 30 degrees
        angle = math.radians(player_angle + ray_angle)
        end_pos = [player_pos[0] + 1000 * math.cos(angle), player_pos[1] + 1000 * math.sin(angle)]
        
        # Measure distance to walls
        min_distance = float('inf')
        for wall in walls:
            x1, y1 = wall[0]
            x2, y2 = wall[1]
            x3, y3 = player_pos
            x4, y4 = end_pos
            
            # Calculate intersection point
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                if 0 < t < 1 and u > 0:
                    intersection_x = x1 + t * (x2 - x1)
                    intersection_y = y1 + t * (y2 - y1)
                    distance = math.sqrt((player_pos[0] - intersection_x) ** 2 + (player_pos[1] - intersection_y) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        
        end_pos = [player_pos[0] + min_distance * math.cos(angle), player_pos[1] + min_distance * math.sin(angle)]
        pygame.draw.line(screen, (255, 255, 255), player_pos, end_pos)

    pygame.draw.circle(screen, (255, 0, 0), (int(player_pos[0]), int(player_pos[1])), 5)

    pygame.display.flip()

pygame.quit()
