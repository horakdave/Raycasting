import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1600, 600))
pygame.display.set_caption("")

screen_width = 800
screen_height = 600

player_pos = [400, 300]
player_angle = 0
ray_length = 200

walls = [[[100, 100], [100, 500]],
         [[100, 500], [700, 500]],
         [[700, 500], [700, 100]],
         [[700, 100], [100, 100]],
         [[300, 200], [500, 200]],
         [[500, 200], [500, 400]],
         [[500, 400], [300, 400]],
         [[300, 400], [300, 200]]]

# Main game loop
is_running = True
is_up_pressed = False
is_left_pressed = False
is_right_pressed = False
is_down_pressed = False

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                is_left_pressed = True
            elif event.key == pygame.K_RIGHT:
                is_right_pressed = True
            elif event.key == pygame.K_UP:
                is_up_pressed = True
            elif event.key == pygame.K_DOWN:
                is_down_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                is_left_pressed = False
            elif event.key == pygame.K_RIGHT:
                is_right_pressed = False
            elif event.key == pygame.K_UP:
                is_up_pressed = False
            elif event.key == pygame.K_DOWN:
                is_down_pressed = False

    if is_left_pressed:
        player_angle -= 1
    if is_right_pressed:
        player_angle += 1

    if is_up_pressed:
        player_pos[0] += 2 * math.cos(math.radians(player_angle))  # Move in the x-direction
        player_pos[1] += 2 * math.sin(math.radians(player_angle))  # Move in the y-direction

    if is_down_pressed:
        player_pos[0] += -2 * math.cos(math.radians(player_angle))  # Move in the x-direction
        player_pos[1] += -2 * math.sin(math.radians(player_angle))  # Move in the y-direction


    screen.fill((0, 0, 0))

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (0, 255, 0), wall[0], wall[1], 2)

    num_rays = 60
    ray_angle = 600 / num_rays
    for i in range(num_rays):
        angle = math.radians(player_angle - 30 + i * ray_angle)
        end_pos = [player_pos[0] + 1000 * math.cos(angle), player_pos[1] + 1000 * math.sin(angle)]
        
        min_distance = float('inf')
        for wall in walls:
            x1, y1 = wall[0]
            x2, y2 = wall[1]
            x3, y3 = player_pos
            x4, y4 = end_pos
            
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
        
        # Drawing the adjusted rays
        end_pos = [player_pos[0] + min_distance * math.cos(angle), player_pos[1] + min_distance * math.sin(angle)]
        pygame.draw.line(screen, (255, 255, 255), player_pos, end_pos)

        # Render 3D view
        slice_height = 30000 / (min_distance + 0.0001)  # Make sure there aint 0/0
        brightness = 255 - min(min_distance * 0.5, 255)
        color = (brightness, brightness, brightness)
        slice_rect = pygame.Rect(screen_width + i * (screen_width / num_rays), (screen_height - slice_height) / 2, screen_width / num_rays, slice_height)
        pygame.draw.rect(screen, color, slice_rect)

    pygame.draw.circle(screen, (255, 0, 0), (int(player_pos[0]), int(player_pos[1])), 5)

    pygame.display.flip()

pygame.quit()
