import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
import sys
width, height = 640, 480
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Set the initial position and rotation of the cube
cube_position = (0, 0, -5)
cube_rotation = 0

# Set up the OpenGL perspective
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Game loop
while True:
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset the modelview matrix
    glLoadIdentity()

    # Set the camera position
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)

    # Rotate the cube
    glRotatef(cube_rotation, 1, 1, 1)

    # Draw the cube
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glEnd()

    # Update the display
    pygame.display.flip()

    # Rotate the cube for the next frame
    cube_rotation += 1

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
