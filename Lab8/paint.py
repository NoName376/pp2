'''

    - R - режим прямоугольника.
    - C - режим круга.
    - P - режим ручки.
    - E - режим ластика.
    - Q - очистить экран.

    - 1 - черный.
    - 2 - зеленый.
    - 3 - красный.
    - 4 - синий.
    - 5 - желтый.
'''




import pygame

WIDTH, HEIGHT = 1200, 800
FPS = 90
draw = False
radius = 2
color = 'blue'
mode = 'pen'

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Paint')
clock = pygame.time.Clock()
screen.fill(pygame.Color('white'))
font = pygame.font.SysFont('None', 60)

def drawLine(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    A, B = y2 - y1, x1 - x2
    C = x2 * y1 - x1 * y2

    if dx > dy:
        if x1 > x2: x1, x2, y1, y2 = x2, x1, y2, y1
        for x in range(x1, x2):
            y = (-C - A * x) / B
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)
    else:
        if y1 > y2: x1, x2, y1, y2 = x2, x1, y2, y1
        for y in range(y1, y2):
            x = (-C - B * y) / A
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)

def drawCircle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    radius = abs(x1 - x2) / 2
    pygame.draw.circle(screen, pygame.Color(color), (x, y), radius, width)

def drawRectangle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    widthr = abs(x1 - x2)
    height = abs(y1 - y2)
    if x2 > x1 and y2 > y1:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y1, widthr, height), width)
    if y2 > y1 and x1 > x2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y1, widthr, height), width)
    if x1 > x2 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x2, y2, widthr, height), width)
    if x2 > x1 and y1 > y2:
        pygame.draw.rect(screen, pygame.Color(color), (x1, y2, widthr, height), width)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: mode = 'rectangle'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_p: mode = 'pen'
            if event.key == pygame.K_e: mode = 'erase'
            if event.key == pygame.K_q: screen.fill(pygame.Color('white'))

            if event.key == pygame.K_1: color = 'black'
            if event.key == pygame.K_2: color = 'green'
            if event.key == pygame.K_3: color = 'red'
            if event.key == pygame.K_4: color = 'blue'
            if event.key == pygame.K_5: color = 'yellow'

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
            if mode == 'pen': pygame.draw.circle(screen, pygame.Color(color), event.pos, radius)
            prevPos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if mode == 'rectangle': drawRectangle(screen, prevPos, event.pos, radius, color)
            elif mode == 'circle': drawCircle(screen, prevPos, event.pos, radius, color)
            draw = False

        if event.type == pygame.MOUSEMOTION:
            if draw and mode == 'pen': drawLine(screen, lastPos, event.pos, radius, color)
            elif draw and mode == 'erase': drawLine(screen, lastPos, event.pos, radius, 'white')
            lastPos = event.pos

    pygame.draw.rect(screen, pygame.Color('white'), (5, 5, 115, 75))
    renderRadius = font.render(str(radius), True, pygame.Color(color))
    screen.blit(renderRadius, (5, 5))

    pygame.display.flip()
    clock.tick(FPS)
