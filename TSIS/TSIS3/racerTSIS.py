import pygame, sys, random, time, json, os
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 400, 600
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.mixer.init()
crash_sound = pygame.mixer.Sound(r"TSIS\TSIS3\images\crash.wav")
pygame.mixer.music.load(r"TSIS\TSIS3\images\background.wav")
pygame.mixer.music.play(-1)

background = pygame.image.load(r"TSIS\TSIS3\images\AnimatedStreet.png")
background = pygame.transform.scale(background, (400,600))

WHITE = (255,255,255)
BLACK = (0,0,0)

font_small = pygame.font.SysFont("Arial", 20)
font_big = pygame.font.SysFont("Arial", 30)

lanes = [80,200,320]

# JSONSAVINGS_____________________________
SETTINGS_FILE = "settings.json"
SCORES_FILE = "scores.json"

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            data = json.load(f)
            data.setdefault("sound", True)
            data.setdefault("difficulty", "normal")
            data.setdefault("car_color", "blue")
            return data
    return {
        "sound": True,
        "difficulty": "normal",
        "car_color": "blue"
    }

def save_settings(data):
    with open(SETTINGS_FILE,"w") as f:
        json.dump(data,f)

settings = load_settings()

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE,"r") as f:
            return json.load(f)
    return []

def save_score(entry):
    scores = load_scores()
    scores.append(entry)
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    with open(SCORES_FILE,"w") as f:
        json.dump(scores,f)

# CLASSES___________________________________

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        color = settings.get("car_color", "blue")

        if color == "green":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\Player_green.png")
        elif color == "red":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\Player_red.png")
        else:
            self.image = pygame.image.load(r"TSIS\TSIS3\images\Player_blue.png")

        self.image = pygame.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect(center=(200,520))
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5,0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"TSIS\TSIS3\images\Enemy.png")
        self.image = pygame.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect(center=(random.choice(lanes),0))

    def move(self, speed):
        self.rect.move_ip(0,speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.choice(lanes),0)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.type = random.choice(["oil", "barrier", "pothole"])

        if self.type == "oil":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\puddles.png")
        elif self.type == "barrier":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\barrier.png")
        else:
            self.image = pygame.image.load(r"TSIS\TSIS3\images\hole.png")

        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(random.choice(lanes),0))

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.top > HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"TSIS\TSIS3\images\dollar.png")
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect(center=(random.choice(lanes),0))

    def move(self, speed):
        self.rect.move_ip(0,speed)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.choice(lanes),0)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro","shield","repair"])

        if self.type == "nitro":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\Nitro.png")
        elif self.type == "shield":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\shield2.png")
        elif self.type == "repair":
            self.image = pygame.image.load(r"TSIS\TSIS3\images\repair.png")
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(random.choice(lanes),0))
        self.spawn_time = time.time()

    def move(self, speed):
        self.rect.move_ip(0,speed)
        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > 5:
            self.kill()


def game_loop(username):
    speed = 5
    coins = 0
    distance = 0
    active_power = None
    power_time = 0

    player = Player()

    enemies = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    powers = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group(player)

    enemy = Enemy()
    coin = Coin()

    enemies.add(enemy)
    coins_group.add(coin)

    all_sprites.add(enemy)
    all_sprites.add(coin)

    spawn_timer = 0

    if settings["difficulty"] == "easy":
        speed = 3
    elif settings["difficulty"] == "normal":
        speed = 5
    else:
        speed = 8

    run = True
    while run:
        max_enemies = 2 + coins // 5
        spawn_chance = min(10, 2 + coins // 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return

        sc.blit(background, (0,0))

        spawn_timer += 1
        distance += speed

        if random.randint(1, 100) <= spawn_chance and len(enemies) < max_enemies:
            e = Enemy()
            enemies.add(e)
            all_sprites.add(e)

        if spawn_timer % 300 == 0:
            p = PowerUp()
            powers.add(p)
            all_sprites.add(p)

        if spawn_timer % 180 == 0:
            o = Obstacle()
            obstacles.add(o)
            all_sprites.add(o)

        for e in enemies:
            e.move(speed)
        for c in coins_group:
            c.move(speed)
        for p in powers:
            p.move(speed)
        for o in obstacles:
            o.move(speed)

        player.move()

        for entity in all_sprites:
            sc.blit(entity.image, entity.rect)

        score = coins + distance//100

        if pygame.sprite.spritecollideany(player, enemies):
            if player.shield:
                player.shield = False
            else:
                crash_sound.play()   # 🔥 ВОТ СЮДА
                pygame.time.delay(300)
                result = game_over_screen(score, coins, distance)

                if result == "retry":
                    return game_loop(username)   # перезапуск игры
                else:
                    return   # в меню

        if pygame.sprite.spritecollideany(player, coins_group):
            coins += 1
            coin.rect.center = (random.choice(lanes),0)

        hit = pygame.sprite.spritecollideany(player, powers)
        if hit:
            active_power = hit.type
            power_time = time.time()
            hit.kill()

        if active_power == "nitro":
            speed = 10
            if time.time() - power_time > 4:
                speed = 5
                active_power = None

        if active_power == "shield":
            player.shield = True

        if active_power == "repair":
            speed = 5
            active_power = None

        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_obstacle:
            if hit_obstacle.type == "oil":
                speed = max(2, speed - 2)  # замедление

            elif hit_obstacle.type == "barrier":
                # как враг → смерть
                if player.shield:
                    player.shield = False
                else:
                    return game_over_screen(score, coins, distance)

            elif hit_obstacle.type == "pothole":
                speed = max(2, speed - 1)

            hit_obstacle.kill()


        sc.blit(font_small.render(f"Score: {score}",True,WHITE),(10,10))
        sc.blit(font_small.render(f"Coins: {coins}",True,WHITE),(10,30))
        sc.blit(font_small.render(f"Dist: {distance}",True,WHITE),(10,50))

        if active_power:
            sc.blit(font_small.render(f"{active_power}",True,(255,0,0)),(10,70))

        pygame.display.update()
        clock.tick(60)

    save_score({
        "name": username,
        "score": score,
        "distance": distance
    })

# SCREENS______________________________________

def game_over_screen(score, coins, distance):
    while True:
        sc.fill((0,0,0))

        title = font_big.render("GAME OVER", True, (255,0,0))
        sc.blit(title, (90,100))

        sc.blit(font_small.render(f"Score: {score}", True, (255,255,255)), (120,200))
        sc.blit(font_small.render(f"Coins: {coins}", True, (255,255,255)), (120,230))
        sc.blit(font_small.render(f"Distance: {distance}", True, (255,255,255)), (120,260))

        retry_btn = draw_button("Retry", 100, 350)
        menu_btn = draw_button("Menu", 100, 420)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()
        clock.tick(60)

def draw_button(text,x,y):
    rect = pygame.Rect(x,y,200,50)
    pygame.draw.rect(sc,(100,100,100),rect)
    label = font_big.render(text,True,WHITE)
    sc.blit(label,(x+30,y+10))
    return rect

def input_name():
    name = ""
    typing = True
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name or "Player"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        sc.fill(BLACK)
        txt = font_big.render("Enter Name:",True,WHITE)
        sc.blit(txt,(80,200))
        sc.blit(font_big.render(name,True,WHITE),(80,260))
        pygame.display.update()
        clock.tick(60)

def leaderboard():
    run = True
    scores = load_scores()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        sc.fill(BLACK)

        sc.blit(font_big.render("Leaderboard",True,WHITE),(80,50))

        for i, s in enumerate(scores):
            text = f"{i+1}. {s['name']} | Score: {s['score']} | Dist: {s['distance']}"
            sc.blit(font_small.render(text,True,WHITE),(50,120+i*30))

        pygame.display.update()
        clock.tick(60)

def settings_screen():
    run = True

    while run:
        sc.fill((0,0,0))

        sc.blit(font_big.render("SETTINGS", True, WHITE), (100,80))

        # --- ТЕКУЩИЕ ЗНАЧЕНИЯ ---
        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color = settings.get("car_color", "blue")
        color_text = f"Car color: {color}"
        diff_text = f"Difficulty: {settings['difficulty']}"

        sc.blit(font_small.render(sound_text, True, WHITE), (80,180))
        sc.blit(font_small.render(color_text, True, WHITE), (80,220))
        sc.blit(font_small.render(diff_text, True, WHITE), (80,260))

        sc.blit(font_small.render("S - toggle sound", True, (200,200,200)), (80,320))
        sc.blit(font_small.render("C - change color", True, (200,200,200)), (80,350))
        sc.blit(font_small.render("D - change difficulty", True, (200,200,200)), (80,380))
        sc.blit(font_small.render("ESC - back", True, (200,200,200)), (80,410))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # 🔊 звук
                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                # 🎨 цвет машины
                if event.key == pygame.K_c:
                    colors = ["green", "blue", "red"]
                    current = colors.index(settings.get("car_color", "blue"))
                    settings["car_color"] = colors[(current + 1) % len(colors)]

                # 🎯 сложность
                if event.key == pygame.K_d:
                    diffs = ["easy", "normal", "hard"]
                    current = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(current + 1) % len(diffs)]

                # выход
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return

        pygame.display.update()
        clock.tick(60)



while True:
    sc.fill(BLACK)

    sc.blit(font_big.render("RACER",True,WHITE),(120,100))

    play_btn = draw_button("Play",100,200)
    lead_btn = draw_button("Leaderboard",100,270)
    set_btn = draw_button("Settings",100,340)
    quit_btn = draw_button("Quit",100,410)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.collidepoint(event.pos):
                name = input_name()
                game_loop(name)

            if lead_btn.collidepoint(event.pos):
                leaderboard()

            if set_btn.collidepoint(event.pos):
                settings_screen()

            if quit_btn.collidepoint(event.pos):
                pygame.quit(); sys.exit()

    pygame.display.update()
    clock.tick(60)