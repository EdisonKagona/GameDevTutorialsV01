import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define constants
FPS = 60
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BALL_SPEED = 5
GAME_DURATION = 600  # 10 minutes in seconds
MISS_THRESHOLD = 10  # Number of misses allowed before game over

# Load sound effects
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("glass-ding-33653.mp3")
game_over_sound = pygame.mixer.Sound("gameover.wav")

# Define classes for objects

# Class for brick objects
class Brick:
    """
    Class to represent brick objects.
    """
    def __init__(self, x, y, width, height, color):
        """
        Initialize a brick.

        Args:
            x (int): X coordinate of the top-left corner.
            y (int): Y coordinate of the top-left corner.
            width (int): Width of the brick.
            height (int): Height of the brick.
            color (tuple): RGB color tuple.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        """
        Draw the brick on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw the brick on.
        """
        pygame.draw.rect(surface, self.color, self.rect)

# Class for paddle object
class Paddle:
    """
    Class to represent the paddle controlled by the player.
    """
    def __init__(self):
        """
        Initialize the paddle.
        """
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = GREEN
        self.move_speed = 0

    def draw(self, surface):
        """
        Draw the paddle on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw the paddle on.
        """
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, direction):
        """
        Move the paddle left or right.

        Args:
            direction (int): Direction of movement (-1 for left, 1 for right).
        """
        self.move_speed = direction * 10

    def update(self):
        """
        Update the paddle's position based on movement speed.
        """
        self.rect.x += self.move_speed
        # Keep the paddle within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Class for ball object
class Ball:
    """
    Class to represent the ball.
    """
    def __init__(self):
        """
        Initialize the ball.
        """
        self.rect = pygame.Rect((SCREEN_WIDTH - BALL_RADIUS) // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
        self.color = WHITE
        self.dx = 0
        self.dy = 0

    def draw(self, surface):
        """
        Draw the ball on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw the ball on.
        """
        pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)

    def update(self):
        """
        Update the position of the ball.
        """
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check for collision with walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def start_movement(self):
        """
        Start the movement of the ball.
        """
        self.dx = BALL_SPEED
        self.dy = -BALL_SPEED  # Start moving upwards

# Function to generate bricks
def generate_bricks():
    """
    Generate bricks for the game.
    """
    bricks = []
    brick_colors = [RED, GREEN, BLUE, YELLOW]
    for i in range(BRICK_ROWS):
        for j in range(BRICK_COLS):
            brick_x = j * (BRICK_WIDTH + 5) + 30
            brick_y = i * (BRICK_HEIGHT + 5) + 50
            color = brick_colors[random.randint(0, len(brick_colors) - 1)]
            bricks.append(Brick(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT, color))
    return bricks

# Function to display game over popup
def game_over_popup():
    """
    Display a game over popup.
    """
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Adjust vertical position
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(2)

# Function to start the game
def start_game():
    """
    Start the game.
    """
    clock = pygame.time.Clock()

    # Create objects
    bricks = generate_bricks()
    paddle = Paddle()
    ball = Ball()

    start_time = time.time()
    game_started = True
    game_over = False
    misses = 0
    player_score = 0

    # Start the ball movement
    ball.start_movement()

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.move(-1)
                elif event.key == pygame.K_RIGHT:
                    paddle.move(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.move_speed = 0

        # Update game state
        if game_started and not game_over:
            # Update paddle position
            paddle.update()

            # Update ball position
            ball.update()

            # Check for collision with paddle
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1
                # Increase ball speed
                ball.dx *= 1.1
                ball.dy *= 1.1
                # Increase score
                player_score += 1
                collision_sound.play()

            # Check for collision with bricks
            for brick in bricks[:]:  # Use a copy of the list to allow removal during iteration
                if ball.rect.colliderect(brick.rect):
                    bricks.remove(brick)
                    ball.dy *= -1
                    player_score += 1
                    collision_sound.play()

            # Check if ball misses paddle
            if ball.rect.bottom >= paddle.rect.top:
                misses += 1
                if misses >= MISS_THRESHOLD:
                    game_over = True
                    game_over_sound.play()

            # Check for game over
            if len(bricks) == 0:
                game_over = True
                game_over_sound.play()

        # Render
        screen.fill(BLACK)

        # Draw bricks
        for brick in bricks:
            brick.draw(screen)

        # Draw paddle
        paddle.draw(screen)

        # Draw ball
        ball.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Check game duration
        if time.time() - start_time >= GAME_DURATION:
            game_over = True

        if game_over:
            game_over_popup()

            # Draw restart button
            restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 10, 200, 50)
            pygame.draw.rect(screen, GREEN, restart_button_rect)
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Restart", True, BLACK)
            text_rect = restart_text.get_rect(center=restart_button_rect.center)
            screen.blit(restart_text, text_rect)

            pygame.display.flip()

            # Wait for restart
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button_rect.collidepoint(event.pos):
                            start_game()

        pygame.display.flip()
        clock.tick(FPS)

# Start the game
start_game()

#To create .exe
#pip install pyinstaller
#pyinstaller --onefile game.py
