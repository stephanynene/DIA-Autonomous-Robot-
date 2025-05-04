import pygame
import random
import heapq
from typing import List, Tuple, Dict, Set

CELL_SIZE = 40

class Mouse:
    def __init__(self, start_pos):
        self.position = start_pos
        self.mode = "random" 
        self.a_star_path = []  
        self.greedy_path = []
        self.cheese_pos = None  
        self.move_cooldown = 0 
        self.total_cost = 0  # random walk cost tracking


    def set_mode(self, mode: str, cheese_pos=None, maze=None):
        self.mode = mode
        self.total_cost = 0 
        if cheese_pos:
            self.cheese_pos = cheese_pos
        if maze:
            self.maze = maze

        if mode == "a_star":
            self.calculate_a_star_path()
        elif mode == "greedy":
            self.calculate_greedy_path()


    def get_total_cost(self):
        return self.total_cost


    def calculate_a_star_path(self):

        self.a_star_path = []

        if not self.cheese_pos:
            return

        start = self.position
        goal = self.cheese_pos

        # A* implementation
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                self.reconstruct_path(came_from, current)
                return

            for neighbor in self.get_neighbors(current, self.maze):
                tentative_g_score = g_score[current] + self.get_cost(neighbor)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # If no path found, use random walk
        print("A* failed to find a path. Switching to random.")
        self.mode = "random"

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int], maze) -> List[Tuple[int, int]]:
        x, y = pos
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] in (0, 2):
                neighbors.append((nx, ny))
        return neighbors 


    def reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]):
        """Reconstruct path from A* search"""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        self.a_star_path = total_path[::-1]
        self.a_star_path = self.a_star_path[1:]  # Skip the current position
  # Reverse to get start to goal

    def move(self, maze, screen=None, draw_fn=None, mouse_img=None, cheese_img=None, cheese_positions=None):
        next_pos = None

        if self.mode == "random":
            self.random_move(maze)
            return

        elif self.mode == "a_star" and self.a_star_path:
            next_pos = self.a_star_path[0]
        elif self.mode == "greedy" and self.greedy_path:
            next_pos = self.greedy_path[0]

        if next_pos:
            x, y = next_pos
            if maze[y][x] == 2:
                # Redraw scene before delaying, so the move is visible
                if screen and draw_fn and mouse_img:
                    screen.fill((255, 255, 255))
                    draw_fn(screen, maze)  # redraw maze
                    for cheese_pos in cheese_positions:
                        screen.blit(cheese_img, (cheese_pos[0] * CELL_SIZE, cheese_pos[1] * CELL_SIZE))
                    screen.blit(mouse_img, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE))
                    pygame.display.flip()
                pygame.time.delay(10)

        if self.mode == "a_star" and self.a_star_path:
            self.a_star_move()
        elif self.mode == "greedy" and self.greedy_path:
            self.greedy_move()

    def random_move(self, maze):
        x, y = self.position
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] in (0, 2):
                tile_type = maze[new_y][new_x]
                self.total_cost += self.get_cost((new_x, new_y))
                self.position = (new_x, new_y)

                if tile_type == 2:
                    pygame.time.delay(10)  # Delay for mud

                return

    def a_star_move(self):
        if len(self.a_star_path) > 0:
            next_pos = self.a_star_path.pop(0)
            self.total_cost += self.get_cost(next_pos)
            self.position = next_pos

    def calculate_greedy_path(self):
        if not self.cheese_pos or not self.maze:
            return

        start = self.position
        goal = self.cheese_pos

        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), start))
        came_from = {}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            visited.add(current)

            if current == goal:
                self.reconstruct_greedy_path(came_from, current)
                return

            for neighbor in self.get_neighbors(current, self.maze):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (self.heuristic(neighbor, goal), neighbor))

        # fallback
        self.mode = "random"

    def reconstruct_greedy_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        self.greedy_path = total_path[::-1]
        self.greedy_path = self.greedy_path[1:]

    def greedy_move(self):
        if len(self.greedy_path) > 0:
            next_pos = self.greedy_path.pop(0)
            self.total_cost += self.get_cost(next_pos)
            self.position = next_pos

    def get_cost(self, pos):
        x, y = pos
        if self.maze[y][x] == 0:
            return 1  # normal
        elif self.maze[y][x] == 2:
            return 100  # heavy/mud tile
        return float('inf')  # wall or impassable


    def draw(self, screen, image):
        screen.blit(image, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE))