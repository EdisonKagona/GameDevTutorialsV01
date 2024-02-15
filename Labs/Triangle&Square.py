import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
width = 640
height = 480

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lab 1: Computer Graphics")

# Set the color (RGB) for the background
background_color = (255, 255, 255)

# Set the color (RGB) for the shapes
shape_color = (0, 0, 0)

# Set the line thickness
line_thickness = 3

# Game loop
while True:
    # Clear the screen with the background color
    screen.fill(background_color)

    # Draw the triangle on the screen
    point1 = (100, 100)
    point2 = (300, 400)
    point3 = (500, 100)
    pygame.draw.polygon(screen, shape_color, [point1, point2, point3], line_thickness)



    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
