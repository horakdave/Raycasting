import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

def draw_cube():
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]
    
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def check_ray_cube_intersection(ray_origin, ray_vector, cube_min, cube_max):
    t_min = (cube_min - ray_origin) / ray_vector
    t_max = (cube_max - ray_origin) / ray_vector
    
    t1 = np.minimum(t_min, t_max)
    t2 = np.maximum(t_min, t_max)
    
    t_near = np.max(t1)
    t_far = np.min(t2)
    
    if t_near > t_far or t_far < 0:
        return False, None
    intersection_point = ray_origin + ray_vector * t_near
    return True, intersection_point

def lidar_scan(center, cube_min, cube_max, num_rays=360, max_distance=10):
    angle_step = 360 / num_rays
    points = []
    rad_angles = np.radians(np.arange(0, 360, angle_step))
    ray_vectors = np.array([[math.cos(rad), math.sin(rad), 0] for rad in rad_angles])

    for ray_vector in ray_vectors:
        ray_origin = np.array(center)
        result = check_ray_cube_intersection(ray_origin, ray_vector, cube_min, cube_max)
        if result[0]:
            points.append(result[1])

    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    glPointSize(5)  # Set point size
    glBegin(GL_POINTS)
    for point in points:
        glVertex3fv(point)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    cube_min = np.array([-1, -1, -1])
    cube_max = np.array([1, 1, 1])
    start_position = [5, 0, 0]  # Starting position of the LiDAR
    lidar_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    start_position[0] -= 0.5
                elif event.key == K_RIGHT:
                    start_position[0] += 0.5
                elif event.key == K_UP:
                    start_position[1] += 0.5
                elif event.key == K_DOWN:
                    start_position[1] -= 0.5

        lidar_angle += 1 % 360

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(*start_position)
        glRotatef(lidar_angle, 0, 0, 1)
        
        draw_cube()
        lidar_scan(start_position, cube_min, cube_max, 360, 10)
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()