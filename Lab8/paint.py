import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 10
    mode = 'blue'
    points = []
    drawing = False
    shape_mode = None
    start_pos = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        erase_mode = pressed[pygame.K_e]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_y:
                    mode = 'yellow'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                    drawing = True
                    if pressed[pygame.K_LSHIFT]:
                        shape_mode = 'rectangle'
                    elif pressed[pygame.K_c]:
                        shape_mode = 'circle'
                    else:
                        shape_mode = 'freehand'

                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                end_pos = event.pos
                if shape_mode == 'freehand':
                    points.append((event.pos, erase_mode))
                    points = points[-256:]
                elif shape_mode == 'rectangle':
                    drawRectangle(screen, start_pos, end_pos, mode)
                elif shape_mode == 'circle':
                    drawCircle(screen, start_pos, end_pos, mode)

        screen.fill((0, 0, 0))
        for (pos, erase) in points:
            pygame.draw.circle(screen, (0, 0, 0) if erase else getColor(mode), pos, radius)

        pygame.display.flip()
        clock.tick(60)


def getColor(mode):
    colors = {
        'blue': (0, 0, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'yellow': (255, 255, 0)
    }
    return colors.get(mode, (255, 255, 255))


def drawRectangle(screen, start, end, mode):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    pygame.draw.rect(screen, getColor(mode), pygame.Rect(x, y, width, height), 2)




def drawCircle(screen, start, end, mode):
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5 / 2)
    center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
    pygame.draw.circle(screen, getColor(mode), center, radius, 2)


main()
