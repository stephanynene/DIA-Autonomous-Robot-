import pygame
from levels import MAZE_LEVELS
from agent import CELL_SIZE


def draw_maze(screen, maze):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)

    # Get the maze's dimensions dynamically
    maze_height = len(maze)
    maze_width = len(maze[0]) if maze_height > 0 else 0

    # Draw the maze grid
    for y in range(maze_height):
        for x in range(maze_width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Wall
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Path
            pygame.draw.rect(screen, GREY, rect, 1)  # Grid lines
