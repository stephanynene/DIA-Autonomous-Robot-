import pygame
from environment import draw_maze
from agent import Mouse
from levels import MAZE_LEVELS

CELL_SIZE = 40
cheese_collected = False

# User level select
level_choice = input("Select level (1 = Easy, 2 = Medium, 3 = Hard): ")
if level_choice not in ["1", "2", "3"]:
    print("Invalid choice! Defaulting to Level 1")
    level_choice = "1"

level_index = int(level_choice) - 1
level_data = MAZE_LEVELS[level_index]

maze = level_data["layout"]
maze_size = level_data["size"]

WINDOW_WIDTH = maze_size[0] * CELL_SIZE
WINDOW_HEIGHT = maze_size[1] * CELL_SIZE

CHEESE_POS = (maze_size[0] - 1, maze_size[1] - 1)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


pygame.init()
# screen = pygame.display.set_mode((CELL_SIZE * 10, CELL_SIZE * 10))
pygame.display.set_caption("Mouse and Cheese Maze")
clock = pygame.time.Clock()

mouse_img = pygame.image.load("assets/mouse.png")
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))
cheese_img = pygame.image.load("assets/cheese.png")
cheese_img = pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))

mouse = Mouse(start_pos=(0, 0))

# Timer setup for smooth movement
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 100)  # Move every 1500 milliseconds (1.5 seconds)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Trigger mouse movement only when MOVE_EVENT is triggered
        if event.type == MOVE_EVENT:
            # Stop if the cheese has been collected

                if not cheese_collected:
                 mouse.move(maze)
                if not cheese_collected and mouse.position == CHEESE_POS:
                    cheese_collected = True
                    print("Cheese collected!")


    screen.fill((255, 255, 255))
    draw_maze(screen, maze)

    # Draw cheese
    screen.blit(cheese_img, (CHEESE_POS[0] * CELL_SIZE, CHEESE_POS[1] * CELL_SIZE))
    # Draw mouse
    mouse.draw(screen, mouse_img)

    pygame.display.flip()
    clock.tick(30)  # Frame rate (30 frames per second)

pygame.quit()
