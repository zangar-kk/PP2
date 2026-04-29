import pygame, random, psycopg2, json, os
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 900, 600
CELL = 30
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)

#IMAGES__________________________________________
bg = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\backgroun.png")
bg = pygame.transform.scale(bg, (900, 600))
button_img = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\PLAY (1).png")
button_img = pygame.transform.scale(button_img, (250, 100))
leader_img = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\LEADERBOARD (1).png")
leader_img = pygame.transform.scale(leader_img, (260, 110))
settings_img = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\SETTINGS (1).png")
settings_img = pygame.transform.scale(settings_img, (246, 100))
startpage = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\startpage.png")
startpage = pygame.transform.scale(startpage,(900,600))
namedesk = pygame.image.load(r"TSIS\TSIS4\imagesTSIS4\NAMEDESK.png")
namedesk = pygame.transform.scale(namedesk, (550,440))
#IMAGES__________________________________________


# JSONSETTINGS____________________________________
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    default = {
        "color": [0,180,0],
        "grid": True,
        "sound": True
    }

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            data = json.load(f)

            # 🔥 добавляем недостающие ключи
            for key in default:
                if key not in data:
                    data[key] = default[key]

            return data

    return default

def save_settings(s):
    with open(SETTINGS_FILE,"w") as f:
        json.dump(s,f)

settings = load_settings()
# JSONSETTINGS____________________________________


# DATABASE__________________________________________
conn = psycopg2.connect(
    dbname="practice",
    user="postgres",
    password="zangar66",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def save_score(username, score, level):
    cur.execute("SELECT id FROM players WHERE username=%s",(username,))
    r = cur.fetchone()
    if r:
        pid = r[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id",(username,))
        pid = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES(%s,%s,%s)
    """,(pid,score,level))
    conn.commit()

def get_top():
    cur.execute("""
        SELECT p.username, MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id=g.player_id
        GROUP BY p.username
        ORDER BY MAX(g.score) DESC
        LIMIT 10
    """)
    return cur.fetchall()

def get_best(username):
    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id=g.player_id
        WHERE p.username=%s
    """,(username,))
    r=cur.fetchone()
    return r[0] if r[0] else 0
# DATABASE__________________________________________

def get_free_pos(snake, obstacles=[], food=None, power=None):
    while True:
        pos = (random.randrange(0, WIDTH, CELL),
               random.randrange(0, HEIGHT, CELL))

        if pos in snake:
            continue

        if pos in obstacles:
            continue

        if food and pos == food:
            continue

        if power and pos == power:
            continue

        return pos

# SCREENS___________________________________________
def input_name():
    name=""
    while True:
        sc.blit(bg, (0,0))
        sc.blit(namedesk, (175,80))
        sc.blit(font.render(name,True,(255,255,0)),(350,260))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN and name:
                    return name
                elif e.key==pygame.K_BACKSPACE:
                    name=name[:-1]
                else:
                    name+=e.unicode

        pygame.display.update()

def menu(username):
    button_rect = button_img.get_rect(center=(440, 365))
    leader_rect = leader_img.get_rect(center=(440, 460))
    settings_rect = settings_img.get_rect(center=(440, 557))

    while True:
        sc.blit(startpage,(0,0))
        sc.blit(button_img, button_rect)
        sc.blit(leader_img, leader_rect)
        sc.blit(settings_img, settings_rect)

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(e.pos): return "play"
                if leader_rect.collidepoint(e.pos): leaderboard()
                if settings_rect.collidepoint(e.pos): settings_screen()

        pygame.display.update()

def leaderboard():
    scores=get_top()
    while True:
        sc.fill((0,0,0))
        sc.blit(big_font.render("TOP 10",True,(255,255,255)),(350,50))

        for i,(n,s) in enumerate(scores):
            sc.blit(font.render(f"{i+1}. {n} {s}",True,(255,255,255)),(300,150+i*30))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                return
        pygame.display.update()

def settings_screen():
    global settings
    while True:
        sc.fill((0,0,0))

        sc.blit(font.render("S - sound",True,(255,255,255)),(300,200))
        sc.blit(font.render("G - grid",True,(255,255,255)),(300,240))
        sc.blit(font.render("C - color",True,(255,255,255)),(300,280))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:
                    save_settings(settings)
                    return
                if e.key==pygame.K_s:
                    settings["sound"]=not settings["sound"]
                if e.key==pygame.K_g:
                    settings["grid"]=not settings["grid"]
                if e.key==pygame.K_c:
                    settings["color"]=[random.randint(0,255) for _ in range(3)]
        color = settings["color"]

        sound_text = "ON" if settings["sound"] else "OFF"
        grid_text = "ON" if settings["grid"] else "OFF"

        sc.blit(font.render(f"{sound_text}", True, (255,255,255)), (400, 200))
        sc.blit(font.render(f"{grid_text}", True, (255,255,255)), (400, 240))

        pygame.draw.rect(sc, color, (300, 350, 100, 50))
        sc.blit(font.render(f"Color: {color}", True, (255,255,255)), (300, 420))
        pygame.display.update()

def game_over(score, level):
    while True:
        sc.fill((0,0,0))
        sc.blit(big_font.render("GAME OVER",True,(255,0,0)),(300,200))
        sc.blit(font.render(f"Score: {score}",True,(255,255,255)),(350,260))
        sc.blit(font.render(f"Level: {level}",True,(255,255,255)),(350,300))
        sc.blit(font.render("R - retry | ESC - menu",True,(255,255,255)),(250,360))

        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r: return "retry"
                if e.key==pygame.K_ESCAPE: return "menu"

        pygame.display.update()

def game(username):
    snake=[(60,60),(30,60)]
    dx,dy=30,0
    obstacles = []
    power=None
    power_type=None
    power_time=0
    power_spawn_time = 0 
    active_power = None
    food= get_free_pos(snake, obstacles, power=power)
    poison= get_free_pos(snake, obstacles, food=food)
    
    score=0
    level=1
    delay=100
    best=get_best(username)

    move=pygame.time.get_ticks()

    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_UP and dy==0: dx,dy=0,-30
                if e.key==pygame.K_DOWN and dy==0: dx,dy=0,30
                if e.key==pygame.K_LEFT and dx==0: dx,dy=-30,0
                if e.key==pygame.K_RIGHT and dx==0: dx,dy=30,0

        now=pygame.time.get_ticks()
        if now-move>delay:
            head=(snake[0][0]+dx,snake[0][1]+dy)
            snake.insert(0,head)
            move=now

            # food
            if head==food:
                score+=1
                food = get_free_pos(snake, obstacles, power=power)
            else:
                snake.pop()

            # poison
            if head==poison:
                for i in range(2):
                    if len(snake)>1: snake.pop()
                poison=get_free_pos(snake, obstacles,food = food, power=power)
                if len(snake)<=1: return score,level

            # power-ups
            if power and head==power:
                power_time=now
                active_power = power_type
                if power_type=="speed": delay=50
                if power_type=="slow": delay=150
                if power_type=="shield": shield=True
                power=None
                power_type = None

            if power is None and active_power is None:
                if random.randint(1,100) <= 20:
                    power = get_free_pos(snake, obstacles, food = food)
                    power_type = random.choice(["speed","slow","shield"])
                    power_spawn_time = now

            if power and now - power_spawn_time > 8000:
                power = None
                power_type = None

            # reset power
            if active_power and now-power_time>5000:
                delay=100
                active_power = None

            # obstacles
            while score >= level*5:
                level += 1

                if level >= 3:
                    hx, hy = snake[0]

                    for _ in range(3):
                        while True:
                            pos = get_free_pos(snake, obstacles)
                            x, y = pos

                            if abs(x - hx) <= CELL and abs(y - hy) <= CELL:
                                continue

                            obstacles.append(pos)
                            break

            if head in obstacles: return score,level

            # collisions
            if head in snake[1:]: return score,level
            if head[0]<0 or head[0]>=WIDTH: return score,level
            if head[1]<0 or head[1]>=HEIGHT: return score,level

        sc.fill((0,0,0))

        # grid
        if settings["grid"]:
            for x in range(0,WIDTH,CELL):
                pygame.draw.line(sc,(40,40,40),(x,0),(x,HEIGHT))
            for y in range(0,HEIGHT,CELL):
                pygame.draw.line(sc,(40,40,40),(0,y),(WIDTH,y))

        for s in snake:
            pygame.draw.rect(sc,settings["color"],(*s,30,30))

        pygame.draw.rect(sc,(255,0,0),(*food,30,30))
        pygame.draw.rect(sc,(120,0,0),(*poison,30,30))

        if power:
            pygame.draw.rect(sc,(0,255,255),(*power,30,30))

        for o in obstacles:
            pygame.draw.rect(sc,(100,100,100),(*o,30,30))

        sc.blit(font.render(f"{username}",True,(255,255,255)),(10,10))
        sc.blit(font.render(f"Score:{score}",True,(255,255,255)),(10,40))
        sc.blit(font.render(f"Best:{best}",True,(255,255,255)),(10,70))

        pygame.display.update()
        clock.tick(60)
# SCREENS___________________________________________

username=input_name()

while True:
    if menu(username)=="play":
        while True:
            score,level=game(username)
            save_score(username,score,level)
            res=game_over(score,level)
            if res=="menu": break