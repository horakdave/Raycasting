import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Raycasting Simulation")

player_pos = [400, 300]
player_angle = 0
ray_length = 200

# Main game loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # List of wall coordinates (start_pos ... end_pos)
    walls = [[[100, 100], [100, 500]],
             [[100, 500], [700, 500]],
             [[700, 500], [700, 100]],
             [[700, 100], [100, 100]]]

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (0, 255, 0), wall[0], wall[1], 2)

    #movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_angle -= 45  # Turn 45 degrees left
            elif event.key == pygame.K_RIGHT:
                player_angle += 45  # Turn 45 degrees right

    # Cast rays
    for ray_angle in range(-30, 31, 1):  # Cast rays from -30 to 30 degrees
        angle = math.radians(player_angle + ray_angle)
        end_pos = [player_pos[0] + ray_length * math.cos(angle), player_pos[1] + ray_length * math.sin(angle)]
        # Extending the rays
        end_pos = [player_pos[0] + 1000 * math.cos(angle), player_pos[1] + 1000 * math.sin(angle)]
        pygame.draw.line(screen, (255, 255, 255), player_pos, end_pos)

    # Draw player
    pygame.draw.circle(screen, (255, 0, 0), (int(player_pos[0]), int(player_pos[1])), 5)

    # Update the display
    pygame.display.flip()

pygame.quit()