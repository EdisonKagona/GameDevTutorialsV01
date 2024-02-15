import pygame
from pygame.locals import *
import time
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.x_velocity = 0
        self.y_velocity = 0
        self.on_ground = False
        self.score = 0
        self.jump_strength = 10
        self.max_jump_strength = 20
        self.jump_increment = 1
        self.last_ball = None  # Keep track of the last ball hit

    def update(self):
        self.x_velocity = 0
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.x_velocity = -5
        if keys[K_RIGHT]:
            self.x_velocity = 5

        if not self.on_ground:
            self.y_velocity += 0.3

        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        if self.rect.y >= 500:
            self.rect.y = 500
            self.y_velocity = 0
            self.on_ground = True
            self.jump_strength = 10
        else:
            self.on_ground = False

        self.rect.x = max(0, min(self.rect.x, 760))

    def jump(self):
        if self.on_ground:
            self.y_velocity = -self.jump_strength
            self.jump_strength = min(self.jump_strength + self.jump_increment, self.max_jump_strength)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Engaging Platformer Game")

    player = Player()
    platforms = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    hit_bar = HitBar()
    all_sprites.add(hit_bar)

    start_time = time.time()
    game_duration = 60
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()
                    if player.last_ball:
                        hit_bar.move_up()

        all_sprites.update()

        if time.time() - start_time >= game_duration:
            running = False

        if len(collectibles) < 5:
            new_collectible = Collectible()
            collectibles.add(new_collectible)
            all_sprites.add(new_collectible)

        if player.score >= 50 and len(collectibles) < 10:
            new_collectible = Collectible()
            collectibles.add(new_collectible)
            all_sprites.add(new_collectible)

        if pygame.sprite.spritecollide(player, platforms, False):
            player.y_velocity = 0
            player.rect.y -= 1
            player.on_ground = True

        closest_ball = get_closest_ball(player, collectibles)
        if closest_ball:
            ball_difference = player.rect.centerx - closest_ball.rect.centerx
            # Adjust jump strength based on the distance to the closest ball
            player.jump_strength = min(player.max_jump_strength, max(player.jump_increment, abs(ball_difference) / 10))

        collected = pygame.sprite.spritecollide(player, collectibles, True)
        for c in collected:
            player.score += 10
            player.y_velocity = -player.jump_strength  # Jump when a ball is collected

        screen.fill((0, 0, 0))

        all_sprites.draw(screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

def get_closest_ball(player, balls):
    closest_ball = None
    closest_distance = float("inf")
    for ball in balls:
        distance = abs(player.rect.centerx - ball.rect.centerx)
        if distance < closest_distance:
            closest_ball = ball
            closest_distance = distance
    return closest_ball

class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 750)
        self.rect.y = random.randint(100, 400)

class HitBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500

    def move_up(self):
        self.rect.y -= 10

if __name__ == "__main__":
    main()
