import pygame
import random
from environment import draw_maze, generate_maze
from agent import Mouse
from levels import MAZE_SIZES
from agent import Mouse, CELL_SIZE


CELL_SIZE = 40
cheese_collected = False

# User level select
level_choice = input("Select level (1 = Easy, 2 = Medium, 3 = Hard): ")
if level_choice not in ["1", "2", "3"]:
    print("Defaulting to Level 1")
    level_choice = "1"

# level_index = int(level_choice) - 1
# level_data = MAZE_LEVELS[level_index]

# maze = level_data["layout"]
# maze_size = level_data["size"]

level_index = int(level_choice) - 1
maze_size = MAZE_SIZES[level_index]
maze = generate_maze(*maze_size)

CHEESE_POSITIONS = []
while len(CHEESE_POSITIONS) < 5:  # 5 cheese pieces
    x = random.randint(0, maze_size[0] - 1)
    y = random.randint(0, maze_size[1] - 1)
    if maze[y][x] == 0 and (x, y) != (0, 0):
        CHEESE_POSITIONS.append((x, y))

CHEESE_POSITIONS.append((maze_size[0] - 1, maze_size[1] - 1)) 


WINDOW_WIDTH = maze_size[0] * CELL_SIZE
WINDOW_HEIGHT = maze_size[1] * CELL_SIZE

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

mode_choice = input("Select movement mode (1 = Random, 2 = A*, 3 = Greedy): ")
if mode_choice == "1":
    mode = "random"
elif mode_choice == "2":
    mode = "a_star"
elif mode_choice == "3":
    mode = "greedy"
else:
    print("Invalid mode selected. Defaulting to random.")
    mode = "random"

mouse = Mouse(start_pos=(0, 0))
mouse.set_mode(mode, CHEESE_POSITIONS[0], maze)

# screen = pygame.display.set_mode((CELL_SIZE * 10, CELL_SIZE * 10))
pygame.display.set_caption("Mouse and Cheese Maze")
clock = pygame.time.Clock()

mouse_img = pygame.image.load("assets/mouse.png")
mouse_img = pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE))
cheese_img = pygame.image.load("assets/cheese.png")
cheese_img = pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))

# Timer setup for smooth movement
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 100)  # Move every 1500 milliseconds (1.5 seconds)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOVE_EVENT:
            mouse.move(maze)

            # Check if cheese collected
            for cheese_pos in CHEESE_POSITIONS[:]:  # copy to allow removal during iteration
                if mouse.position == cheese_pos:
                    CHEESE_POSITIONS.remove(cheese_pos)
                    print("Collected a cheese!")

                    # Update target if cheeses remain
                    if CHEESE_POSITIONS:
                        mouse.set_mode(mode, CHEESE_POSITIONS[0], maze)

    # Drawing
    screen.fill((255, 255, 255))
    draw_maze(screen, maze)

    # Draw all cheeses
    for cheese_pos in CHEESE_POSITIONS:
        screen.blit(cheese_img, (cheese_pos[0] * CELL_SIZE, cheese_pos[1] * CELL_SIZE))

    # Draw mouse
    mouse.draw(screen, mouse_img)

    pygame.display.flip()
    clock.tick(30)

    # End condition
    if not CHEESE_POSITIONS:
        print("All cheese collected!")
        running = False

pygame.quit()

