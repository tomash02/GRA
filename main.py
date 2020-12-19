from cmath import atan, pi
from numpy.ma import cos, sin
from pygame import *
import pygame
from actor import Actor
from enemy import Enemy
from obstacles import Obstacles
from projectile import Projectile

pygame.init()
winx = 900
winy = 468
win = pygame.display.set_mode((winx, winy))
pygame.display.set_caption("GRA")
LEFT = 1
coolbg = pygame.image.load('Game/coolbg.png')
char = pygame.image.load('Game/standing.png')
b_island = pygame.image.load('Game/b_island.png')
grass_s = pygame.image.load('Game/grasss.png')
s_island = pygame.image.load('Game/s_island.png')
stone = pygame.image.load('Game/stone.png')
wood = pygame.image.load('Game/wood.png')

score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 30, True)
player = Actor(win, 10, 356, 64, 64, 100)
goblins = []

fireRate = 0
run = True
bulletSF = pygame.mixer.Sound('Game/bullet.wav')
hitSF = pygame.mixer.Sound('Game/hit.wav')

bgx1 = 0
bgx2 = 900
collRight = False
collLeft = False
onplatform = False
startplatform = 0
stopFall = True


def setObstacle(cords, sprite):
    if sprite == wood:
        for i in cords:
            Obstacles.obstacles.append(Obstacles(i[0], i[1], 137, 37, sprite))

def setEnemy(cords):
    for i in cords:
        goblins.append(Enemy(i[0], i[1], 64, 64, i[2], i[3], player, Obstacles.obstacles))


setObstacle([[400, 370], [780, 370], [975, 288], [1170, 220], [1400, 370], [1450, 333], [1537, 370], [1800, 370], [2000, 300], [2200, 230], [2220, 370], [2400, 230], [2500, 370]], wood)
setEnemy([[310, 350, 400, 100], [530, 350, 618, 100], [600, 350, 730, 100], [1000, 350, 1100, 100], [1170, 220, 1250, 200], [1400, 350, 1537, 200], [1800, 350, 2000, 200], [2000, 350, 2100, 100], [2410, 229, 2500, 290], [2600, 350, 2800, 200]])
currplatformx = Obstacles.obstacles[0].cords[0]
currplatformw = Obstacles.obstacles[0].cords[2]


def redraw(bgx1, bgx2):
    win.blit(coolbg, (bgx1, 0))
    win.blit(coolbg, (bgx2, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (10, 10))
    player.draw(win)
    for obstacle in Obstacles.obstacles:
        obstacle.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in Projectile.bullets:
        bullet.draw(win)
    pygame.display.update()


def menu():
    menutext = font.render('Shift - Strzelanie', 1, (255, 255, 255))
    menutext1 = font.render('w, s, a, d - poruszanie się', 1, (255, 255, 255))
    menutext2 = font.render('wciśnij  dwukrotnie esc aby kontynuwać', 1, (255, 255, 255))
    menubg = pygame.Surface((900, 480))
    menubg.set_alpha(230)
    menubg.fill((9, 13, 71))
    win.blit(menubg, (0, 0))
    win.blit(menutext, (338, 100))
    win.blit(menutext1, (290, 200))
    win.blit(menutext2, (200, 300))
    menurun = True
    while menurun:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menurun = False
    pygame.time.delay(200)

def bulletspeed():
    v = 13
    mouse = pygame.mouse.get_pos()
    dx = mouse[0] - player.x - 32
    dy = (mouse[1] - player.y - 32) * -1
    if dx == 0:
        return 0, v
    elif dy == 0:
        return v, 0
    elif dx < 0:
        A_angle = atan(dy / dx) + pi
    else:
        A_angle = atan(dy / dx)
    vx = v * cos(A_angle)
    vy = v * sin(A_angle)
    return vx, vy

menu()
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()
    event = pygame.event.poll()

    for i in Obstacles.obstacles:
        if player.hitbox[1] < i.cords[1] + i.cords[3] and player.hitbox[1] + player.hitbox[3] > i.cords[1]:
            if 0 < (player.hitbox[0] + player.hitbox[2]) - i.cords[0] < 10:
                collRight = True
                collLeft = False
                break
            elif 20 > (i.cords[0] + i.cords[2]) - player.hitbox[0] > 1:
                collRight = False
                collLeft = True
                break
            else:
                collRight = False
                collLeft = False

        if player.hitbox[1] + player.hitbox[3] >= i.cords[1] >= player.hitbox[1] and i.cords[0] + i.cords[2] > \
                player.hitbox[0] > i.cords[0]:
            if player.isJump and player.jumpCount != 10:
                fallcount = player.jumpCount
                player.isJump = False
                player.jumpCount = 10
                onplatform = True
                currplatformx = i.cords[0]
                currplatformw = i.cords[2]
                stopFall = True

            if onplatform == False:
                stopFall = True
                currplatformx = i.cords[0]
                currplatformw = i.cords[2]
                onplatform = True

        if (player.hitbox[0] + player.hitbox[2] < currplatformx or player.hitbox[
            0] > currplatformx + currplatformw) and not player.isJump and stopFall:
            onplatform = False
            player.fall()

        for bullet in Projectile.bullets:
            if bullet.y - bullet.radius < i.cords[1] + i.cords[3] and bullet.y + bullet.radius > \
                    i.cords[1]:
                if bullet.x + bullet.radius > i.cords[0] and bullet.x - bullet.radius < i.cords[0] + \
                        i.cords[2]:
                    bullet.remove()

    if keys[pygame.K_a] and not collLeft:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False

    if keys[pygame.K_d] and not collRight:
        player.left = False
        player.right = True
        player.standing = False
        if player.x < winx - 300:
            player.x += player.vel
        else:
            bgx1 -= player.vel
            bgx2 -= player.vel
            currplatformx -= player.vel
            if bgx1 <= -winx:
                bgx1 = winx
            if bgx2 <= -winx:
                bgx2 = winx
            for goblin in goblins:
                goblin.x -= player.vel
                goblin.path[1] -= player.vel
                goblin.path[0] -= player.vel
            for i in Obstacles.obstacles:
                i.cords[0] -= player.vel

    if keys[pygame.K_ESCAPE]:
        menu()
    if keys[pygame.K_q]:
        print(player.hitbox[0], player.y)

    if not (keys[pygame.K_a] or keys[pygame.K_d]):
        player.standing = True
    if not (player.isJump):
        if keys[pygame.K_SPACE]:
            player.isJump = True
    else:
        if player.jumpCount >= -10:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.25 * neg
            player.jumpCount -= 1
        else:
            player.isJump = False
            player.jumpCount = 10

    for goblin in goblins:
        if goblin.alive:
            if player.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player.hitbox[1] + player.hitbox[3] > \
                    goblin.hitbox[1]:
                if player.hitbox[0] + player.hitbox[2] > goblin.hitbox[0] and player.hitbox[0] < goblin.hitbox[0] + \
                        goblin.hitbox[2]:
                    player.hit()
                    goblin.spawnReturn()
                    score -= 5

    if fireRate > 0:
        fireRate += 1
    if fireRate > 10:
        fireRate = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if ((keys[pygame.K_LSHIFT]) or event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT) and fireRate == 0:
        if len(Projectile.bullets) < 1000:
            Projectile.bullets.append(Projectile(round(player.x + 32), round(player.y + 32), 5,
                                                 (230, 100, 100), bulletspeed()))
            Projectile.count += 1
        fireRate = 1

    for goblin in goblins:
        for bullet in Projectile.bullets:
            if goblin.alive:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                        goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                            goblin.hitbox[2]:
                        goblin.hit()
                        score += 1
                        bullet.remove()

    for bullet in Projectile.bullets:
        bullet.move()
    redraw(bgx1, bgx2)
pygame.quit()
