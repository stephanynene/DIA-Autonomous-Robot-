import pygame
import random

CELL_SIZE = 40

class Mouse:
    def __init__(self, start_pos):
        self.position = start_pos  # Initial position
        self.prev_position = None  # To store previous valid position
        self.backtracking = False  # Flag to indicate if it's backtracking
        self.visited = set()  # Initialize the visited set to keep track of visited positions

    def move(self, maze):
        x, y = self.position

        # Random direction to try to move (up, down, left, right)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)  # Randomize the direction to make the movement more random

        # Try to move to a valid adjacent cell
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] == 0:
                # Move to the new position if it's valid
                self.position = (new_x, new_y)
                self.visited.add(self.position)
                break  # Exit the loop once a valid move is found

        # Handle backtracking (if needed)
        if self.position == (x, y):  # If no movement has occurred
            # For backtracking, choose a position from the visited list
            if self.path:
                self.pos = self.path.pop()

    def draw(self, screen, image):
        if self.position is None:  # Ensure position is not None
            return  # Don't draw if position is None
        screen.blit(image, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE))
