import pygame
from levels import MAZE_LEVELS
from agent import CELL_SIZE

def draw_maze(screen, maze):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GREY, rect, 1)
