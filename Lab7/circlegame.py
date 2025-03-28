import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

ball_color = (255, 0, 0)
ball_radius = 25
ball_x, ball_y = 400, 300
ball_speed = 20

isRun = True

while isRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRun = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x - ball_radius - ball_speed >= 0:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] and ball_x + ball_radius + ball_speed <= 800:
        ball_x += ball_speed
    if keys[pygame.K_UP] and ball_y - ball_radius - ball_speed >= 0:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN] and ball_y + ball_radius + ball_speed <= 600:
        ball_y += ball_speed

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()