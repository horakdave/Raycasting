import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1600, 600))
pygame.display.set_caption("Raycasting Map Maker")

screen_width = 800
screen_height = 600

player_pos = [400, 300]
player_angle = 0
player_vert_angle = 0   # Up and down
player_z = 50           # Height
ray_length = 200
player_radius = 5
fly_speed = 100

walls = []

start_pos = None
is_drawing = False

# Main game loop
is_running = True
is_up_pressed = False
is_left_pressed = False
is_right_pressed = False
is_down_pressed = False
is_w_pressed = False
is_s_pressed = False
is_space_pressed = False
is_ctrl_pressed = False

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
            elif event.key == pygame.K_w:
                is_w_pressed = True
            elif event.key == pygame.K_s:
                is_s_pressed = True
            elif event.key == pygame.K_SPACE:
                is_space_pressed = True
            elif event.key == pygame.K_LCTRL:
                is_ctrl_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                is_left_pressed = False
            elif event.key == pygame.K_RIGHT:
                is_right_pressed = False
            elif event.key == pygame.K_UP:
                is_up_pressed = False
            elif event.key == pygame.K_DOWN:
                is_down_pressed = False
            elif event.key == pygame.K_w:
                is_w_pressed = False
            elif event.key == pygame.K_s:
                is_s_pressed = False
            elif event.key == pygame.K_SPACE:
                is_space_pressed = False
            elif event.key == pygame.K_LCTRL:
                is_ctrl_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not is_drawing:
                    start_pos = event.pos
                    is_drawing = True
                else:
                    end_pos = event.pos
                    walls.append([start_pos, end_pos])
                    is_drawing = False

    if is_left_pressed:
        player_angle -= 1
    if is_right_pressed:
        player_angle += 1

    if is_up_pressed:
        player_pos[0] += 2 * math.cos(math.radians(player_angle))
        player_pos[1] += 2 * math.sin(math.radians(player_angle))

    if is_down_pressed:
        player_pos[0] -= 2 * math.cos(math.radians(player_angle))
        player_pos[1] -= 2 * math.sin(math.radians(player_angle))

    if is_w_pressed:
        player_vert_angle = min(player_vert_angle + 1, 30)  # Limit vertical angle to 30 degrees
    if is_s_pressed:
        player_vert_angle = max(player_vert_angle - 1, -30)  # Limit vertical angle to -30 degrees

    if is_space_pressed:
        player_z -= fly_speed  # Move down faster
    if is_ctrl_pressed:
        player_z += fly_speed  # Move up faster

    screen.fill((0, 0, 0))  # Clear the screen

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (0, 255, 0), wall[0], wall[1], 2)

    pygame.draw.circle(screen, (255, 255, 255), player_pos, player_radius)

    num_rays = 200
    ray_angle = 60 / num_rays
    
    # Raycasting logic  AI helped:)
    for i in range(num_rays):
        angle = math.radians(player_angle - 30 + i * ray_angle)
        end_pos = [player_pos[0] + ray_length * math.cos(angle), player_pos[1] + ray_length * math.sin(angle)]
        
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
                        end_pos = [intersection_x, intersection_y]

        pygame.draw.line(screen, (255, 255, 255), player_pos, end_pos, 2)

        # Render 3D view    AI helped:)
        adjusted_distance = min_distance
        slice_height = 30000 / (adjusted_distance + 0.0001)  # Avoid division by zero
        brightness = 255 - min(adjusted_distance * 0.5, 255)
        color = (brightness, brightness, brightness)

        # Calculate vertical ofset    AI helped:)  
        vertical_offset = player_z / (adjusted_distance + 0.0001)
        slice_height *= math.cos(math.radians(player_vert_angle))
        slice_y_offset = (screen_height / 2) - (slice_height / 2) - vertical_offset
        
        slice_rect = pygame.Rect(screen_width + i * (screen_width / num_rays), slice_y_offset, screen_width / num_rays, slice_height)
        pygame.draw.rect(screen, color, slice_rect)

    if is_drawing:
        current_mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 0, 0), start_pos, current_mouse_pos, 2)

    pygame.display.flip()

pygame.quit()
