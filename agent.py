import pygame

CELL_SIZE = 40

class Mouse:
    def __init__(self, start_pos):
        self.position = start_pos

    def draw(self, screen, image):
        screen.blit(image, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE))
