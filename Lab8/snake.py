import pygame
import random

pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Game variables
score = 0
level = 1
speed = 200  # Initial speed
fruit_eaten = False

# Snake initialization
head_square = [100, 100]
squares = [[30 + i * 10, 100] for i in range(8)]
direction = "right"
next_dir = "right"

done = False

# Generate a random fruit position ensuring it does not overlap with walls or snake
def generate_fruit():
    while True:
        fr_x = random.randrange(0, width // 10) * 10
        fr_y = random.randrange(0, height // 10) * 10
        if [fr_x, fr_y] not in squares:
            return [fr_x, fr_y]

fruit_coor = generate_fruit()

# Game over function
def game_over(font, size, color):
    global done
    g_o_font = pygame.font.SysFont(font, size)
    g_o_surface = g_o_font.render(f"Game Over! Score: {score}, Level: {level}", True, color)
    g_o_rect = g_o_surface.get_rect(center=(width // 2, height // 2))
    screen.fill((0, 0, 0))
    screen.blit(g_o_surface, g_o_rect)
    pygame.display.update()
    pygame.time.delay(4000)
    pygame.quit()

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and direction != "up":
                next_dir = "down"
            if event.key == pygame.K_UP and direction != "down":
                next_dir = "up"
            if event.key == pygame.K_LEFT and direction != "right":
                next_dir = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                next_dir = "right"

    # Update direction
    direction = next_dir

    # Move snake head
    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10

    # Check for wall collision
    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over("times new roman", 45, (255, 0, 0))

    # Check for self-collision
    for square in squares[:-1]:
        if head_square == square:
            game_over("times new roman", 45, (255, 0, 0))

    # Update snake position
    new_square = list(head_square)
    squares.append(new_square)
    squares.pop(0)

    # Check if fruit is eaten
    if head_square == fruit_coor:
        fruit_eaten = True
        score += 10
        squares.insert(0, squares[0])  # Grow snake

        # Leveling system: Increase speed every 3 fruits
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 20)  # Increase speed

    if fruit_eaten:
        fruit_coor = generate_fruit()
        fruit_eaten = False

    # Drawing section
    screen.fill((0, 0, 0))

    # Display score and level
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    # Draw fruit
    pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)

    # Draw snake
    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(speed)

pygame.quit()