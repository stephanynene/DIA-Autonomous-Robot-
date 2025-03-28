import pygame
import random

CELL_SIZE = 40

class Mouse:
    def __init__(self, start_pos):
        self.position = start_pos  # Initial position
        self.prev_position = None  # To store previous valid position
        self.backtracking = False  # Flag to indicate if it's backtracking

    def move(self, maze):
        if self.position is None:  # Ensure position is not None
            return  # Prevent movement if position is None

        x, y = self.position

        # Define possible movement directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # down, right, up, left

        if not self.backtracking:
            self.direction = random.choice(directions)

        dx, dy = self.direction
        new_x = x + dx
        new_y = y + dy

        # Check if move is valid (inside maze and not a wall)
        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            if maze[new_y][new_x] == 0:  # Valid move (path)
                self.position = (new_x, new_y)
                self.prev_position = self.position  # Save last valid position
                self.backtracking = False
            else:
                # Wall encountered, backtrack
                self.backtracking = True
                self.position = self.prev_position
        else:
            # If out of bounds, backtrack
            self.backtracking = True
            self.position = self.prev_position

    def draw(self, screen, image):
        if self.position is None:  # Ensure position is not None
            return  # Don't draw if position is None
        screen.blit(image, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE))
