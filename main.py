import pygame_gui as gui
import pygame
from snake_game import *
pygame.init()

# Constants
TURN_DELAY = (int)(0.25 * 1000) # Time between snake moves, in seconds (which are converted to milliseconds).

# Create/initialize the pygame screen
screen = pygame.display.set_mode((600, 500))
screen.fill(pygame.Color(255, 255, 255))
pygame.display.init()
pygame.display.update()

# Create/initialize the UI
manager = gui.UIManager((600,500))
restart_button_rect = pygame.Rect(0, 0, 150, 100)
restart_button_rect.bottomleft = (0, 0)
restart_button = gui.elements.UIButton(relative_rect=restart_button_rect, text='Restart', anchors={'left':'left','bottom':'bottom'}, manager=manager)

# Initialize the game
snake = Snake(screen, (30, 25), (0, 0), (15, 12))

clock = pygame.time.Clock()
turn_timer = pygame.USEREVENT
pygame.time.set_timer(turn_timer, TURN_DELAY)
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0

    # Closes the window if you click the X in the corner
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == restart_button:
                print("This is a test")

        if event.type == turn_timer:
            if not snake.game_over:
                snake.move_snake(0)

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill(WHITE)
    snake.display()

    pygame.display.update()
