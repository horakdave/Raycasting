import pygame
import math
import time

print("Welcome to my 3D engine!")
print("You can build walls with LMB")
print("Adjust the height of the walls with I - Increase, D - Decrease")
print("Space - Fly upwards, CTRL - Fly down")
print("W - Look up, S - Look down")

pygame.init()

screen = pygame.display.set_mode((1600, 600))
pygame.display.set_caption("Raycasting")

screen_width = 800
screen_height = 600

player_pos = [400, 300]
player_angle = 0
player_vert_angle = 0   # Looking up/down
player_z = 50
ray_length = 1000
player_radius = 5
fly_speed = 100
view_line_length = 7.5

walls = []

start_pos = None
is_drawing = False
current_wall_height = 1  # Default wall height

# Font for displaying wall height
font = pygame.font.SysFont(None, 36)

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
is_increase_height_pressed = False
is_decrease_height_pressed = False

height_increment = 0.05  # Slower increment
last_height_change_time = time.time()
height_change_interval = 0.2  # 200 milliseconds

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
            elif event.key == pygame.K_i:  # Increase wall height
                is_increase_height_pressed = True
            elif event.key == pygame.K_d:  # Decrease wall height
                is_decrease_height_pressed = True
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
            elif event.key == pygame.K_i:
                is_increase_height_pressed = False
            elif event.key == pygame.K_d:
                is_decrease_height_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):  # Left mouse button or right mouse button
                if not is_drawing:
                    start_pos = event.pos
                    is_drawing = True
                else:
                    end_pos = event.pos
                    walls.append([start_pos, end_pos, current_wall_height])
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

    if is_s_pressed:
        player_vert_angle = min(player_vert_angle + 1, 30)
    if is_w_pressed:
        player_vert_angle = max(player_vert_angle - 1, -30)

    if is_space_pressed:
        player_z -= fly_speed  # Move down
    if is_ctrl_pressed:
        player_z += fly_speed  # Move up

    current_time = time.time()
    if is_increase_height_pressed and current_time - last_height_change_time > height_change_interval:
        current_wall_height += height_increment
        last_height_change_time = current_time

    if is_decrease_height_pressed and current_time - last_height_change_time > height_change_interval:
        current_wall_height = max(current_wall_height - height_increment, 0.25)  # Ensure wall height is at least 0.25
        last_height_change_time = current_time

    screen.fill((0, 0, 0))

    # Draw walls
    for wall in walls:
        pygame.draw.line(screen, (0, 255, 0), wall[0], wall[1], 2)

    pygame.draw.circle(screen, (255, 255, 255), player_pos, player_radius)

    view_line_end_pos = (
        player_pos[0] + view_line_length * math.cos(math.radians(player_angle)),
        player_pos[1] + view_line_length * math.sin(math.radians(player_angle))
    )
    pygame.draw.line(screen, (255, 0, 0), player_pos, view_line_end_pos, 2)

    num_rays = 200
    ray_angle = 60 / num_rays

    # Raycasting logic
    for i in range(num_rays):
        angle = math.radians(player_angle - 30 + i * ray_angle)
        end_pos = [player_pos[0] + ray_length * math.cos(angle), player_pos[1] + ray_length * math.sin(angle)]

        ray_intersections = []
        for wall in walls:
            x1, y1 = wall[0]
            x2, y2 = wall[1]
            wall_height = wall[2]  # Wall height from the list
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
                    ray_intersections.append((distance, intersection_x, intersection_y, wall_height))

        ray_intersections.sort(reverse=True)  # Sort from farthest to nearest

        for distance, intersection_x, intersection_y, wall_height in ray_intersections:
            end_pos = [intersection_x, intersection_y]
            adjusted_distance = distance
            base_slice_height = 30000 / (adjusted_distance + 0.0001)  # Base slice height
            adjusted_slice_height = base_slice_height * wall_height  # Adjust for wall height
            brightness = 255 - min(adjusted_distance * 0.5, 255)
            color = (brightness, brightness, brightness)

            # Calculate the vertical offset
            vertical_offset = player_z / (adjusted_distance + 0.0001)
            base_slice_height *= math.cos(math.radians(player_vert_angle))
            adjusted_slice_height *= math.cos(math.radians(player_vert_angle))
            slice_y_base = (screen_height / 2) - (base_slice_height / 2) - (player_vert_angle * 10) - vertical_offset
            slice_y_offset = slice_y_base - (adjusted_slice_height - base_slice_height) / 2  # Adjust upwards only

            slice_rect = pygame.Rect(screen_width + i * (screen_width / num_rays), slice_y_base - adjusted_slice_height, screen_width / num_rays, adjusted_slice_height)
            pygame.draw.rect(screen, color, slice_rect)

            # Draw a yellow dot at the intersection point
            pygame.draw.circle(screen, (255, 255, 0), (int(intersection_x), int(intersection_y)), 2)

        # Draw the ray from player position to end_pos (or maximum ray length)
        pygame.draw.line(screen, (255, 255, 255), player_pos, end_pos, 1)

    if is_drawing:
        current_mouse_pos = pygame.mouse.get_pos()  
        pygame.draw.line(screen, (255, 0, 0), start_pos, current_mouse_pos, 2)

    # Render and display the current wall height
    height_text = font.render(f'Wall Height: {current_wall_height:.2f}', True, (255, 255, 255))
    screen.blit(height_text, (10, 10))

    pygame.display.flip()

pygame.quit()
