import pygame
pygame.init()

sc = pygame.display.set_mode((810,610), pygame.RESIZABLE)
clock = pygame.time.Clock()
x,y =25,25
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if y - 25 > 0:
            y -= 20

    if keys[pygame.K_DOWN]:
        if y + 25 <= 600:
            y += 20

    if keys[pygame.K_LEFT]:
        if x - 25 > 0:
            x -= 20

    if keys[pygame.K_RIGHT]:
        if x + 25 <= 800:
            x += 20
    sc.fill((255,255,255))

    pygame.draw.circle(sc, (255, 0,0), (x,y), 25)
    pygame.display.update()
    clock.tick(60)
pygame.quit()