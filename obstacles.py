import pygame


class Obstacles:
    obstacles = []

    def __init__(self, x, y, width, height, sprite):
        self.cords = [x, y, width, height]
        self.sprite = sprite

    def draw(self, win):
        # pygame.draw.rect(win, (200, 100, 21), self.cords, 2)
        win.blit(self.sprite, (self.cords[0], self.cords[1]))
