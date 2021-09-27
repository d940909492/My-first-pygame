

import pygame
import random
import os

WIDTH = 500
HEIGHT = 600
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Anime Manic shooter game")
clock = pygame.time.Clock()

background = pygame.image.load(os.path.join("img", "back1.png")).convert()

player1 = pygame.image.load(os.path.join("img", "huaji.png")).convert()
playerlives = pygame.transform.scale(player1, (30,30))
playerlives.set_colorkey(WHITE)
#enemy1 = pygame.image.load(os.path.join("img", "leimu.png")).convert()
anime_girls = []
for i in range(5):
    anime_girls.append(pygame.image.load(os.path.join("img", f"girl{i}.png")).convert())

shootsound = pygame.mixer.Sound(os.path.join('music','shoot.wav'))
diesound = pygame.mixer.Sound(os.path.join('music','boom.wav'))
expl_sounds = [
    pygame.mixer.Sound(os.path.join('music','expl0.wav')),
    pygame.mixer.Sound(os.path.join('music','expl1.wav')),
]

boost = {}
boost['addpower'] = pygame.image.load(os.path.join("img", "addbullet.png")).convert()
boost['addhp'] = pygame.image.load(os.path.join("img","hpadd.png")).convert()

pygame.mixer.music.load(os.path.join('music','background.wav'))


font_name = pygame.font.match_font('arial')

def showhealth(surf, hp, x, y):
    if hp < 0:
        hp = 0
    LENGTH = 200
    HEIGHT = 10
    fill = (hp/200)*LENGTH
    outline_rect = pygame.Rect(x, y, LENGTH, HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 4)

def showlives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x  = x + 35*i
        img_rect.y = y
        surf.blit(img, img_rect)

def newenemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def messtext(surf, text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def drawmenu():
        messtext(screen, 'Otaku manic Shooting Game!', 40, WIDTH / 2 , HEIGHT / 4)
        messtext(screen, 'By d940909492', 54, WIDTH/2, HEIGHT / 3)
        messtext(screen, 'Press Space to shoot, and use Arrow Keys to move', 22, WIDTH/2, HEIGHT/2)
        messtext(screen, 'Press any keys to enter', 18, WIDTH/2, HEIGHT*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1 , (50,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 22
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom =  HEIGHT - 10
        self.speed = 7
        self.health = 200
        self.lives = 5
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.guntime = 0

    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.guntime > 8000:
            self.gun -= 1
            self.guntime = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 100:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom >HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shootsound.play()
            elif self.gun >=2:
                bullet0 = Bullet(self.rect.left, self.rect.centery)
                bullet1 = Bullet(self.rect.right, self.rect.centery)
                #bullet2 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet0)
                all_sprites.add(bullet1)
                #all_sprites.add(bullet2)
                bullets.add(bullet0)
                bullets.add(bullet1)
                #bullets.add(bullet2)
                shootsound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT)

    def addgun(self):
        self.gun += 1
        self.guntime = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(anime_girls)
        self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width  / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,7)
        self.speedx = random.randrange(-2,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.rot_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 7)
            self.speedx = random.randrange(-2,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['addpower', 'addhp'])
        self.image = boost[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


pygame.mixer.music.play(-1)

menu = True

running= True

while running:
    if menu:
        close = drawmenu()
        if close:
            break
        menu = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            newenemy()
    score = 0


    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True )
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        if random.random() > 0.9:
            pow = power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        newenemy()

    hit1 = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hit1:
        newenemy()
        player.health -= hit.radius
        if player.health <= 0:
            diesound.play()
            player.lives -= 1
            player.health = 200
            player.hide()


    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'addhp':
            player.health += 30
            if player.health >200:
                player.health = 200
        elif hit.type == 'addpower':
            player.addgun()


    if player.lives == 0:
        menu = True

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    all_sprites.draw(screen)
    messtext(screen, str(score), 40, WIDTH/2, 10)
    showhealth(screen, player.health,5, 20)
    showlives(screen, player.lives, playerlives, WIDTH - 180, 15)
    pygame.display.update()

pygame.quit()