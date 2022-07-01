from pygame import *
from random import randint
from time import sleep

miss_enemy = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 10, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss_enemy
        if self.rect.y >= 490:
            self.rect.y = -40
            miss_enemy += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

player = Player('rocket.png', 350, 450, 40, 40, 5)

enemy1 = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)
enemy2 = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)
enemy3 = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)
enemy4 = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)
enemy5 = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)

monsters = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

finish = False
game = True
clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont("Arial", 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

bullet_s = mixer.Sound('fire.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet_s.play()
                player.fire()

    if finish != True:

        score_count = font2.render('Счет:' + str(score), True,  (255, 215, 0))
        miss_count = font2.render('Пропущено:' + str(miss_enemy), True,  (255, 215, 0))

        win = font1.render('U WIN', True, (255, 215, 0))
        lose = font1.render('U LOSE', True, (255, 215, 0))

        window.blit(background, (0, 0))
        window.blit(score_count, (10, 0))
        window.blit(miss_count, (10, 30))

        monsters.update()
        monsters.draw(window)

        player.update()
        player.reset()

        bullets.update()
        bullets.draw(window)
        
        if miss_enemy == 3:
            finish = True
            window.blit(lose, (200, 200))
        
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            enemy = Enemy('ufo.png', randint(50, 650), randint(-250, 0), 40, 40, 1)
            monsters.add(enemy)
            score += 1

    display.update()
    clock.tick(FPS)