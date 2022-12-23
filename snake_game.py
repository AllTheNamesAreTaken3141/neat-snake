import pygame
from random import randint
from math import floor
from typing import Sequence

# Color globals
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SEGMENT_WIDTH = 20
SEGMENT_HEIGHT = 20

# Represents one segment of the snake, used for display
class Segment(pygame.sprite.Sprite):

    def __init__(self, x:int, y:int, color:Sequence[int]) -> None:
        super().__init__()

        # Set the width, height, and color
        self.image = pygame.Surface((SEGMENT_WIDTH, SEGMENT_HEIGHT))
        self.image.fill(color)

        # Reposition the segment
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# A single snake. Performs most of the logic for the game
class Snake:
    COLOR_CODES = {
        'body' : BLACK,
        'head' : BLUE,
        'apple' : RED
    }

    # Holds Segment objects for displaying each segment
    display_segments = pygame.sprite.Group()

    game_over = False
    score = 0 # Number of apples collected

    def __init__(self, screen, game_size: Sequence[int], game_offset: Sequence[int], spawn_pos: Sequence[int], length:int=3) -> None:
        self.screen = screen

        # The dimensions of the game board
        self.game_width = game_size[0]
        self.game_height = game_size[1]
        self.offset_x = game_offset[0]
        self.offset_y = game_offset[1]
        self.length = length

        # The snake's movement direction. 0 = up, 1 = right, 2 = down, 3 = left
        self.direction = 0

        # The coordinates of each segment of the snake; used for logic
        self.segment_positions = []
        self.segment_positions.append(spawn_pos)

        self.apple_position = (randint(0, self.game_width - 1), randint(0, self.game_height - 1))

    # Converts the positions of each segment into Segment objects for display
    def display(self) -> None:
        # Clear the container to prevent duplicates
        self.display_segments.empty()

        apple = self.apple_position
        self.display_segments.add(Segment(apple[0] * SEGMENT_WIDTH + self.offset_x, apple[1] * SEGMENT_HEIGHT + self.offset_y, self.COLOR_CODES['apple']))

        head = self.segment_positions[-1]
        self.display_segments.add(Segment(head[0] * SEGMENT_WIDTH + self.offset_x, head[1] * SEGMENT_HEIGHT + self.offset_y, self.COLOR_CODES['head']))

        # Use slices to loop through every segment except the head
        for seg in self.segment_positions[:-1:]:
            self.display_segments.add(Segment(seg[0] * SEGMENT_WIDTH + self.offset_x, seg[1] * SEGMENT_HEIGHT + self.offset_y, self.COLOR_CODES['body']))
        self.display_segments.update()
        self.display_segments.draw(self.screen)

    # Gets control input, moves the snake, and checks for collisions
    def move_snake(self, turn_direction:int) -> None:
        # turn_direction changes the movement direction of the snake
        # -1 = turn left, 1 = turn right, 0 = don't turn
        self.direction += turn_direction
        self.direction = self.direction % 4

        old_head = self.segment_positions[-1]

        if self.direction == 0:
            new_head = (old_head[0], old_head[1] - 1)
        elif self.direction == 1:
            new_head = (old_head[0] + 1, old_head[1])
        elif self.direction == 2:
            new_head = (old_head[0], old_head[1] + 1)
        else:
            new_head = (old_head[0] - 1, old_head[1])

        # Check for collision with the walls or the snake
        if new_head in self.segment_positions or\
            new_head[0] < 0 or new_head[0] >= self.game_width or\
            new_head[1] < 0 or new_head[1] >= self.game_height:
            self.game_over = True
            return

        if new_head == self.apple_position:
            self.score += 1
            self.length += 1
            self.apple_position = (randint(0, self.game_width - 1), randint(0, self.game_height - 1))

        self.segment_positions.append(new_head)
        if len(self.segment_positions) > self.length:
            self.segment_positions.pop(0)