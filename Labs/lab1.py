import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (0, 1)  # Initial direction (right)
snake_speed = 3  # Adjust this value to control the snake's speed (lower values make it slower)
snake_move_counter = 0
snake_growth = False

# Food variables
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Timer variables
game_duration_seconds = 300  # 5 minutes
game_start_time = pygame.time.get_ticks()

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle arrow key presses to change the snake's direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, 1):
        snake_direction = (0, -1)
    elif keys[pygame.K_DOWN] and snake_direction != (0, -1):
        snake_direction = (0, 1)
    elif keys[pygame.K_LEFT] and snake_direction != (1, 0):
        snake_direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
        snake_direction = (1, 0)

    # Move the snake at a controlled speed
    snake_move_counter += 1
    if snake_move_counter >= snake_speed:
        new_head = (
            (snake[0][0] + snake_direction[0]) % GRID_WIDTH,
            (snake[0][1] + snake_direction[1]) % GRID_HEIGHT,
        )
        snake.insert(0, new_head)

        # Check for collisions with food
        if snake[0] == food:
            snake_growth = True
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )

        # If not growing, remove the tail
        if not snake_growth:
            snake.pop()
        else:
            snake_growth = False

        snake_move_counter = 0  # Reset the move counter

    # Clear the screen
    screen.fill(WHITE)

    # Draw the food
    pygame.draw.rect(
        screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

    # Update the display
    pygame.display.flip()

    # Check game duration
    current_time = pygame.time.get_ticks()
    elapsed_seconds = (current_time - game_start_time) // 1000
    if elapsed_seconds >= game_duration_seconds:
        pygame.quit()
        sys.exit()

    # Control game speed
    clock.tick(10)  # Adjust this value to change the overall game speed
