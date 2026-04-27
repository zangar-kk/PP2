import pygame
import random, time

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer")

font = pygame.font.SysFont("Arial", 20)

COL_COINS=0

background = pygame.image.load(r"lab10\images\AnimatedStreet.png")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"lab10\images\Enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)

    def move(self):
        self.rect.move_ip(0, 5)

        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"lab10\images\Player.png")
        self.image = pygame.transform.scale(self.image, (50, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < 400:
            self.rect.move_ip(5, 0)
        if pressed_keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom <600:
            self.rect.move_ip(0,5)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"lab10\images\dollar.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)
    def move(self):
        self.rect.move_ip(0, 5)

        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

coins.add(coin)
enemies.add(enemy)
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sc.blit(background, (0,0))

    for entity in all_sprites:
        sc.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(player, enemies):
          pygame.mixer.Sound(r'lab10\images\crash.wav').play()

          sc.fill((255,0,0))

          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          run = False

    if pygame.sprite.spritecollideany(player, coins):
        COL_COINS +=1
        for coin in coins:
            coin.rect.top = 0
            coin.rect.center = (random.randint(40, 360), 0)

    scores = font.render(str(COL_COINS), True, (0,0,0))
    sc.blit(scores, (10,10))

    pygame.display.update()
    clock.tick(60)
pygame.quit()
