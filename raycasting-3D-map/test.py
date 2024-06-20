import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Define the vertices of a cube
vertices = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Define the edges of the cube
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

# Draw the cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main function to initialize Pygame and OpenGL
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)  # Enable depth testing here
    
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    
    glTranslatef(0.0, 0.0, -10)  # Move the camera back along the z-axis
    
    # Camera position
    camera_x, camera_y, camera_z = 0, 0, 0  # Initialize camera at the center of the cube
    
    # Remove the rotation from the main loop to prevent spinning
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera_x -= 0.1
                elif event.key == pygame.K_RIGHT:
                    camera_x += 0.1
                elif event.key == pygame.K_UP:
                    camera_z += 0.1
                elif event.key == pygame.K_DOWN:
                    camera_z -= 0.1
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()  # Reset the view matrix
        gluLookAt(camera_x, camera_y, camera_z, 0, 0, 0, 0, 1, 0)  # Set the camera position
        
        draw_cube()
        
        pygame.display.flip()
        pygame.time.wait(10)

main()