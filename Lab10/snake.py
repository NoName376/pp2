import pygame
import random
import psycopg2

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

conn = psycopg2.connect(
    host="82.97.250.165", dbname="postgres", user="kbtu", password="kbtu", port=5435
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS snake (
    username VARCHAR PRIMARY KEY,
    score INT DEFAULT 0,
    level INT DEFAULT 1
)
""")
conn.commit()

username = input("Enter your username: ").strip()
cursor.execute("SELECT score, level FROM snake WHERE username=%s", (username,))
user_data = cursor.fetchone()

if user_data:
    score, level = user_data
else:
    score, level = 0, 1
    cursor.execute("INSERT INTO snake (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
    conn.commit()

speed = max(200 - (level - 1) * 20, 50)
fruit_eaten = False
paused = False

head_square = [100, 100]
squares = [[30 + i * 10, 100] for i in range(8)]
direction = "right"
next_dir = "right"

done = False

def generate_fruit():
    while True:
        fr_x = random.randrange(0, width // 10) * 10
        fr_y = random.randrange(0, height // 10) * 10
        if [fr_x, fr_y] not in squares:
            return [fr_x, fr_y]

fruit_coor = generate_fruit()

def game_over(font, size, color):
    global done
    g_o_font = pygame.font.SysFont(font, size)
    g_o_surface = g_o_font.render(f"Game Over! Score: {score}, Level: {level}", True, color)
    g_o_rect = g_o_surface.get_rect(center=(width // 2, height // 2))
    screen.fill((0, 0, 0))
    screen.blit(g_o_surface, g_o_rect)
    pygame.display.update()
    pygame.time.delay(4000)
    save_user()
    pygame.quit()

def save_user():
    cursor.execute(
        "UPDATE snake SET score=%s, level=%s WHERE username=%s",
        (score, level, username)
    )
    conn.commit()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_user()
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
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    font = pygame.font.SysFont("times new roman", 30)
                    pause_surface = font.render("Paused", True, (255, 255, 0))
                    pause_rect = pause_surface.get_rect(center=(width // 2, height // 2))
                    screen.blit(pause_surface, pause_rect)
                    pygame.display.update()
                else:
                    save_user()

    if paused:
        pygame.time.delay(100)
        continue

    direction = next_dir

    if direction == "right":
        head_square[0] += 10
    if direction == "left":
        head_square[0] -= 10
    if direction == "up":
        head_square[1] -= 10
    if direction == "down":
        head_square[1] += 10

    if head_square[0] < 0 or head_square[0] >= width or head_square[1] < 0 or head_square[1] >= height:
        game_over("times new roman", 45, (255, 0, 0))

    for square in squares[:-1]:
        if head_square == square:
            game_over("times new roman", 45, (255, 0, 0))

    new_square = list(head_square)
    squares.append(new_square)
    squares.pop(0)

    if head_square == fruit_coor:
        fruit_eaten = True
        score += 10
        squares.insert(0, squares[0])
        if score % 30 == 0:
            level += 1
            speed = max(50, speed - 20)

    if fruit_eaten:
        fruit_coor = generate_fruit()
        fruit_eaten = False

    screen.fill((0, 0, 0))

    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"{username}  Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.draw.circle(screen, (0, 255, 0), (fruit_coor[0] + 5, fruit_coor[1] + 5), 5)

    for el in squares:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(speed)

save_user()
pygame.quit()
