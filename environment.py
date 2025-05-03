import random
import pygame
from agent import CELL_SIZE


def draw_maze(screen, maze):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)

    # Get maze's dimensions dynamically
    maze_height = len(maze)
    maze_width = len(maze[0]) if maze_height > 0 else 0

    # Draw maze grid
    for y in range(maze_height):
        for x in range(maze_width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Wall
            else:
                pygame.draw.rect(screen, WHITE, rect)  # Path
            pygame.draw.rect(screen, GREY, rect, 1)  # Grid lines


def generate_maze(width, height):
    # Ensure dimensions are odd for proper maze carving
    width = width if width % 2 == 1 else width - 1
    height = height if height % 2 == 1 else height - 1

    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                maze[ny - dy // 2][nx - dx // 2] = 0
                maze[ny][nx] = 0
                carve(nx, ny)

    # Start carving from (1, 1)
    maze[1][1] = 0
    carve(1, 1)

    # Ensure top-left (0, 0) is clear
    maze[0][0] = 0
    maze[0][1] = 0
    maze[1][0] = 0

    # Ensure bottom-right is a path
    maze[height - 1][width - 1] = 0

    # Ensure connection to bottom-right
    if maze[height - 2][width - 1] == 1 and maze[height - 1][width - 2] == 1:
        maze[height - 2][width - 1] = 0  # open vertical
        maze[height - 1][width - 2] = 0  # open horizontal

    return maze
