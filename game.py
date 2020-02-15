import pygame
import figure

from glob import glob

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

pygame.key.set_repeat(1, 100)

screen: pygame.Surface = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Тетрис')

icon = pygame.image.load('images/icon.jpg')
pygame.display.set_icon(icon)

frame = pygame.image.load('images/frame.png')
background = pygame.image.load('images/background.png')
bricks = [
    pygame.image.load(brick)
    for brick in glob('images/bricks/*.png')
]
blowing_frames = [
    pygame.image.load(frame)
    for frame in glob('images/blast/*.jpg')
]

buttons = {
    'play': {
        'clicked': False,
        'image_default': pygame.image.load('images/play.jpg'),
        'image_clicked': pygame.image.load('images/play_click.jpg'),
        'position': (555, 590)
    },
    'pause': {
        'clicked': False,
        'image_default': pygame.image.load('images/pause.jpg'),
        'image_clicked': pygame.image.load('images/pause_click.jpg'),
        'position': (555, 654)
    },
    'exit': {
        'clicked': False,
        'image_default': pygame.image.load('images/exit.jpg'),
        'image_clicked': pygame.image.load('images/exit_click.jpg'),
        'position': (555, 714)
    }
}
for button in buttons.values():
    button['rect'] = pygame.Rect(
        button['position'],
        (
            button['image_default'].get_rect().width,
            button['image_default'].get_rect().height
        )
    )

GRID_WIDTH = 18
GRID_HEIGHT = 30
grid = [
    [None for x in range(GRID_WIDTH)]
    for y in range(GRID_HEIGHT)
]

active_figure = None
next_figure = figure.random(bricks)

clock = pygame.time.Clock()
time = 0

FREQUENCY = 1000
current_frequency = FREQUENCY

score = 0

blowing = False
blowing_frame = 0
blowing_line = 0

game_over = False
paused = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if active_figure is not None:
                if event.key == pygame.K_LEFT:
                    active_figure.move('left')
                elif event.key == pygame.K_RIGHT:
                    active_figure.move('right')
                elif event.key == pygame.K_UP:
                    if active_figure.rotate():
                        print('rotated')
            if event.key == pygame.K_DOWN:
                current_frequency = FREQUENCY // 20
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current_frequency = FREQUENCY
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for name, button in buttons.items():
                if button['rect'].collidepoint(x, y):
                    if name == 'play':
                        game_over = False
                        for y in range(GRID_HEIGHT):
                            for x in range(GRID_WIDTH):
                                grid[y][x] = None
                        paused = False
                        blowing = False
                        active_figure = None
                        score = 0
                    elif name == 'pause':
                        paused = not paused
                        continue
                    elif name == 'exit':
                        running = False
                        break
                    button['clicked'] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in buttons.values():
                button['clicked'] = False

    if not blowing and active_figure is None:
        for line in grid:
            if None not in line:
                blowing = True
                blowing_frame = 0
                blowing_line = grid.index(line)
                score += 1

    if not game_over and not paused:
        time += clock.tick()
        if blowing:
            if time >= 200:
                for x in range(GRID_WIDTH):
                    grid[blowing_line][x] = blowing_frames[blowing_frame]
                blowing_frame += 1
                if blowing_frame >= len(blowing_frames):
                    for y in range(blowing_line, 0, -1):
                        grid[y] = grid[y - 1]
                    grid[0] = [None for _ in range(GRID_WIDTH)]
                    blowing = False
                time = 0
        else:
            if time >= current_frequency:
                if active_figure is None:
                    active_figure = next_figure
                    next_figure = figure.random(bricks)
                    if not active_figure.place(grid, GRID_WIDTH // 2 - 1, 0, active_figure.current_state):
                        print("game over")
                        game_over = True
                        active_figure = None
                else:
                    if not active_figure.move('down'):
                        active_figure = None
                time = 0

    screen.blit(frame, (0, 0))
    screen.blit(background, (25, 25))

    for button in buttons.values():
        screen.blit(
            button['image_clicked'] if button['clicked']
            else button['image_default'],
            button['position']
        )

    if game_over:
        text = font.render(
            'Игра окончена',
            False, (0, 0, 0)
        )
        screen.blit(text, (570, 300))
    if paused:
        text = font.render(
            'Пауза',
            False, (0, 0, 0)
        )
        screen.blit(text, (570, 350))
    text = font.render(
        'Очки: ' + str(score),
        False, (0, 0, 0)
    )
    screen.blit(text, (570, 400))

    for y in range(len(next_figure.states[next_figure.current_state])):
        for x in range(len(next_figure.states[next_figure.current_state][0])):
            if next_figure.states[next_figure.current_state][y][x]:
                screen.blit(
                    next_figure.brick,
                    (
                        600 + x * background.get_width() // GRID_WIDTH,
                        100 + y * background.get_height() // GRID_HEIGHT
                    )
                )

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = grid[y][x]
            if square is not None:
                screen.blit(
                    square,
                    (
                        25 + x * background.get_width() // GRID_WIDTH,
                        25 + y * background.get_height() // GRID_HEIGHT
                    )
                )

    pygame.display.flip()
