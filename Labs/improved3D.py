import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
width, height = 640, 480
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Set the initial position and rotation of the cube
cube_position = (0, 0, -5)
cube_rotation = [0, 0, 0]  # Store rotation angles for each axis

# Enable depth testing and lighting
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

# Set material properties
glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.5, 0.5, 1))
glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
glMaterialf(GL_FRONT, GL_SHININESS, 50)

# Game loop
while True:
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset the modelview matrix
    glLoadIdentity()

    # Set the camera position
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)

    # Apply rotation to the cube
    glRotatef(cube_rotation[0], 1, 0, 0)
    glRotatef(cube_rotation[1], 0, 1, 0)
    glRotatef(cube_rotation[2], 0, 0, 1)

    # Draw the cube
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glVertex3f(1, -1, -1)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glEnd()

    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cube_rotation[1] += 5
            elif event.key == pygame.K_RIGHT:
                cube_rotation[1] -= 5
            elif event.key == pygame.K_UP:
                cube_rotation[0] += 5
            elif event.key == pygame.K_DOWN:
                cube_rotation[0] -= 5
