import pygame
from pygame import *

playerLeft = []
playerRight = []


class Actor():
    for i in range(1, 9):
        playerRight.append(pygame.image.load(f'Game/R{i}.png'))
        playerLeft.append(pygame.image.load(f'Game/L{i}.png'))

    def __init__(self, win, x, y, width, height, health):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walk = 0
        self.standing = True
        self.hitbox = (self.x + 18, self.y + 12, 27, 48)
        self.fallspeed = 1

    def draw(self, win):

        if self.walk + 1 >= 8:
            self.walk = 0
        if not self.standing:
            if self.left:
                self.win.blit(playerLeft[self.walk], (self.x, self.y))
                self.walk += 1
            elif self.right:
                self.win.blit(playerRight[self.walk], (self.x, self.y))
                self.walk += 1
        else:
            if self.left:
                self.win.blit(playerLeft[0], (self.x, self.y))
            else:
                self.win.blit(playerRight[0], (self.x, self.y))
        self.hitbox = (self.x + 18, self.y + 12, 27, 50)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 40
        self.y = 356
        self.walk = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        self.win.blit(text, (426 - (text.get_width() / 2), 100))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    def fall(self):
        if self.y <= 356:
            self.y += self.fallspeed
