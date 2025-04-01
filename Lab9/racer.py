import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# FPS settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED, SCORE, COINS = 3, 0, 0

# Fonts
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("Images/AnimatedStreet.png")

# Create game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Racer")


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed_increase = 0.1  # Initial enemy speed increase per coin collection

    def move(self):
        global SCORE
        # Move the enemy down and check for collision with screen boundaries
        self.rect.move_ip(0, SPEED + self.speed_increase)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def increase_speed(self):
        # Increase enemy speed after every 10 coins collected
        global COINS
        if COINS >= 10:
            self.speed_increase += 0.1
            COINS -= 10  # Reset coins after increasing speed


# Coin upgrade checkpoints
c1, c2, c3, c4, c5 = False, False, False, False, False


# Coin class with random weights
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly choose a coin weight (1, 2, or 3 points)
        self.weight = random.choice([1, 2, 3])
        self.image = pygame.image.load("Images/Coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

    def move(self):
        global COINS, SPEED, c1, c2, c3, c4, c5
        # Add coins based on their weight to the player's total coins
        COINS += self.weight

        # Speed upgrades based on coins collected
        if not c1 and COINS >= 10:
            SPEED += 1
            c1 = True
        if not c2 and COINS >= 20:
            SPEED += 1
            c2 = True
        if not c3 and COINS >= 30:
            SPEED += 1
            c3 = True
        if not c4 and COINS >= 40:
            SPEED += 1
            c4 = True
        if not c5 and COINS >= 50:
            SPEED += 1
            c5 = True

        # Randomly position coins off-screen when they move out of the visible area
        self.rect.top = random.randint(40, SCREEN_WIDTH - 40)
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Allow player to move left, right, up, and down within screen boundaries
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)


# Initialize player, enemy, and coin
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Create sprite groups
enemies = pygame.sprite.Group(E1)
coinss = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# Speed increase timer event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


# Game over screen
def game_over_screen():
    screen.fill(RED)
    screen.blit(game_over, (30, 250))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                elif event.key == K_ESCAPE:
                    return False


def handle_crash():
    time.sleep(2)


background_y = 0  # Background

#game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Check for collisions
    if pygame.sprite.spritecollideany(P1, enemies):
        continue_game = handle_crash()
        if not continue_game:
            pygame.quit()
            sys.exit()

    # Update background scrolling
    background_y = (background_y + SPEED) % background.get_height()
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_height()))

    # Display score and coin count
    screen.blit(font_small.render(str(SCORE), True, BLACK), (10, 10))
    screen.blit(font_small.render(str(COINS), True, BLACK), (370, 10))

    # Update all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if entity == C1 and pygame.sprite.spritecollideany(P1, coinss):
            entity.move()
        else:
            entity.move()

    # Update coins position
    for coin in coinss:
        coin.rect.y += SPEED
        if coin.rect.top > SCREEN_HEIGHT:
            coin.rect.y = -coin.rect.height
            coin.rect.x = random.randint(40, SCREEN_WIDTH - 40)

    # Increase enemy speed
    E1.increase_speed()

    pygame.display.update()
    FramePerSec.tick(FPS)
