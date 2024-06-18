import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

def create_cube():  # Vertecies and edges of a cube

    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
    )
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    )
    return vertices, edges

def draw_cube(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def lidar_scan(center, num_rays=360, max_distance=10):  # Lidar scan sim from the center
    angle_step = 360 / num_rays
    for angle in np.arange(0, 360, angle_step):
        rad = math.radians(angle)
        for distance in np.linspace(0, max_distance, num=int(max_distance*10)):
            x = center[0] + distance * math.cos(rad)
            y = center[1] + distance * math.sin(rad)
            z = center[2]
            # Intersections check here
            # (we will just draw the ray because its laggy already)
            glBegin(GL_POINTS)
            glVertex3f(x, y, z)
            glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -20)

    vertices, edges = create_cube()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_cube(vertices, edges)
        lidar_scan((0, 0, 0), 360, 10)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()