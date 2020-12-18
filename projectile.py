import pygame


class Projectile(object):
    bullets = []
    count = 0

    def __init__(self, x, y, radius, color, v):
        self.id = Projectile.count
        self.x = x
        self.y = y
        self.vx = v[0]
        self.vy = v[1]
        self.radius = radius
        self.color = color

    def move(self):
        if 2000 > self.x > 0 or 500 > self.y > 0:
            self.x += self.vx
            self.y -= self.vy

    def remove(self):
        for i in range(len(self.bullets)):
            if self.bullets[i - 1].id == self.id:
                self.bullets.pop(i - 1)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        # pygame.draw.rect(win, (200, 0, 21), self.hitbox, 2)


