import pygame
from environment import draw_maze
from agent import Mouse
from levels import MAZE_LEVELS

CELL_SIZE = 40
CHEESE_POS = (9, 9)

pygame.init()
screen = pygame.display.set_mode((CELL_SIZE * 10, CELL_SIZE * 10))
pygame.display.set_caption("Mouse and Cheese Maze")
clock = pygame.time.Clock()

mouse_img = pygame.image.load("assets/mouse.png")
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))
cheese_img = pygame.image.load("assets/cheese.png")
cheese_img = pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))

mouse = Mouse(start_pos=(0, 0))
maze = MAZE_LEVELS[0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    draw_maze(screen, maze)

    # Draw cheese
    screen.blit(cheese_img, (CHEESE_POS[0] * CELL_SIZE, CHEESE_POS[1] * CELL_SIZE))

    # Draw mouse
    mouse.draw(screen, mouse_img)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
