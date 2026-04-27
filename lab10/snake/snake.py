import pygame
import random
pygame.init()

pygame.display.set_caption("Snake")
sc = pygame.display.set_mode((900,600), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

direction = "right"
x,y = 30,30
ap = (30,30)

def apple():
    ax = random.randrange(0,900,30)
    ay = random.randrange(0,600,30)
    return (ax, ay)

snake = [(30,30),(60,30)]
delay = 100
dx,dy = 30,0
move = pygame.time.get_ticks()
score = 0
lvl = 2
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy ==0:
                dy = -30
                dx = 0
            elif event.key == pygame.K_DOWN and dy ==0 :
                dx =0
                dy = 30
            elif event.key == pygame.K_LEFT and dx ==0:
                dx = -30
                dy = 0
            elif event.key == pygame.K_RIGHT and dx==0:
                dx = 30
                dy = 0

    now = pygame.time.get_ticks()
    if now - move > delay:
        head = (snake[0][0]+dx,snake[0][1]+dy)
        snake.insert(0,head)
        if head == ap:
            ap = apple()
            score +=1
        else:
            snake.pop() 
        move = now

        if head in snake[1:]:
            running = False

        if head[0] < 0 or head[0] >= 900:
            running = False
        if head[1] < 0 or head[1] >= 600:
            running = False
        if ap in snake[1: ]:
            ap = apple()

    if score == lvl:
        delay -=1
        lvl +=2

    
    sc.fill((155,230,5))
    
    for i in snake:
        pygame.draw.rect(sc, (0,180,0), (*i,30,30))
    pygame.draw.rect(sc, (255,0,0), (*ap, 30, 30))
    
    txt = font.render(str(score), True, (255,255,255))
    sc.blit(txt, (440,15))
    pygame.display.update()
    clock.tick(120)
    

pygame.quit()