import pygame

enemyLeft = []
enemyRight = []

class Enemy():
    jumpCount = 10
    for i in range(1, 12):
        enemyRight.append(pygame.image.load(f'Game/R{i}E.png'))
        enemyLeft.append(pygame.image.load(f'Game/L{i}E.png'))

    def __init__(self, x, y, width, height, end, health, player, obslist):
        self.initx = x
        self.inity = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = pygame.Rect(self.x + 13, self.y + 10, 28, 50)
        self.health = health
        self.inithealth = health
        self.alive = True
        self.player = player
        self.obslist = obslist
        self.isJump = False
        self.fallspeed = 9
        if self.y == 350:
            self.onplatform = False
        else:
            self.onplatform = False
        self.currplatformx = self.obslist[0].cords[0]
        self.currplatformw = self.obslist[0].cords[2]

    def draw(self, win):
        if self.alive:
            self.move()
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(enemyRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.hitbox = (self.x + 13, self.y + 10, 28, 50)
                # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
                shiftx = 0
            else:
                win.blit(enemyLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.hitbox = (self.x + 23, self.y + 13, 28, 50)
                # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
                shiftx = 13
            pygame.draw.rect(win, (230, 20, 20), (self.x + shiftx, self.y - 5, self.inithealth // 2, 5))
            if self.health >= 0:
                pygame.draw.rect(win, (30, 200, 20), (self.x + shiftx, self.y - 5, self.health // 2, 5))

    def move(self):
        if self.x - 200 <= self.player.x <= self.x + 200:
            if self.player.x < self.x:
                if self.vel > 0:
                    self.vel *= -1
                self.x += self.vel
                self.checkforcoll()
            else:
                if self.vel < 0:
                    self.vel *= -1
                self.x += self.vel
                self.checkforcoll()
        else:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                    self.checkforcoll()
                else:
                    self.vel *= -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                    self.checkforcoll()
                else:
                    self.vel *= -1
                    self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 20
            if self.health == 0:
                self.alive = False
        else:
            self.alive = False
        print(self.health)

    def spawnReturn(self):
        self.x = self.initx
        self.y = self.inity

    def jump(self):
        self.isJump = True
        if self.jumpCount >= -10:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
            self.y -= (self.jumpCount ** 2) * 0.25 * neg
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 10

    def fall(self):
        if self.y <= 350:
            self.y += self.fallspeed
        else:
            self.onplatform = False


    def checkforcoll(self):
        for i in self.obslist:
            if self.hitbox[1] < i.cords[1] + i.cords[3] and self.hitbox[1] + self.hitbox[3] > i.cords[1]:
                if 0 < (self.hitbox[0] + self.hitbox[2]) - i.cords[0] < 10:
                    self.jump()
                elif 20 > (i.cords[0] + i.cords[2]) - self.hitbox[0] > 1:
                    self.jump()

            if self.isJump and self.hitbox[1] + self.hitbox[3] >= i.cords[1] and i.cords[0] + i.cords[2] > \
                    self.hitbox[0] > i.cords[0] and self.jumpCount != 10 and self.hitbox[1] <= i.cords[1]:
                fallcount = self.jumpCount
                self.isJump = False
                self.jumpCount = 10
                self.onplatform = True
                self.currplatformx = i.cords[0]
                self.currplatformw = i.cords[2]

            if (self.hitbox[0] + self.hitbox[2] < self.currplatformx or self.hitbox[
                0] > self.currplatformx + self.currplatformw):
                self.fall()