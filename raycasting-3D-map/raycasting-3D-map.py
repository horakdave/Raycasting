import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(tuple(map(float, line.strip().split()[1:])))
            elif line.startswith('f'):
                face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                faces.append(face)
    return vertices, faces

def draw_model(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def lidar_scan(center, vertices, faces, num_rays=360, max_distance=10): # Lidar scan sim
    angle_step = 360 / num_rays
    for angle in np.arange(0, 360, angle_step):
        rad = math.radians(angle)
        for distance in np.linspace(0, max_distance, num=int(max_distance*10)):
            x = center[0] + distance * math.cos(rad)
            y = center[1] + distance * math.sin(rad)
            z = center[2]
            for face in faces:
                v0, v1, v2 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
                # Implement ray-triangle intersection test heres
                # If the ray intersects with the triangle defined by v0, v1, v2, visualize/record the intersection point
                # Priklad: check_ray_triangle_intersection(ray_origin, ray_direction, v0, v1, v2)
                # If intersection occurs, visualize or record the intersection point
                glBegin(GL_POINTS)
                glVertex3f(x, y, z)  # Visualize the LiDAR scan point
                glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -20)

    vertices, faces = load_obj(r"C:\Users\horak\Documents\GitHub\Raycasting\raycasting-3D-map\map.obj")

    start_position = (5, 0, 0) # of the LIDAR

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces)

        # Starting pos
        lidar_scan(start_position, vertices, faces, 360, 10)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()