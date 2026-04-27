import pygame
import math
def main():
    pygame.init()
    sc = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    drawing = False
    sh = "circle"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_c:
                    sc.fill((0, 0, 0))
                
                elif event.key == pygame.K_1:
                    sh ="circle"
                elif event.key == pygame.K_2:
                    sh ="rect"
                elif event.key == pygame.K_3:
                    sh ="triangle"
                elif event.key == pygame.K_4:
                    sh = "romb"
                
                elif event.key == pygame.K_UP:
                    radius = min(200, radius + 1)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos

                if mode == 'eraser':
                    color = (0, 0, 0)
                elif mode == 'red':
                    color = (255, 0, 0)
                elif mode == 'green':
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                if sh == "circle":
                    pygame.draw.circle(sc, color, (x, y), radius)
                if sh == "rect":
                    pygame.draw.rect(sc, color, (x, y, 2*radius, 2*radius))
                if sh == "triangle":
                    pygame.draw.polygon(sc, color, [(x, y), (x+radius, y+(radius*math.sqrt(3))), (x-radius,y+radius*math.sqrt(3))])
                if sh == "romb":
                     pygame.draw.polygon(sc,color, [(x, y), (x+radius, y+(radius*math.sqrt(3))), (x,y+2*radius*math.sqrt(3)),(x-radius,y+radius*math.sqrt(3))])
    
        pygame.display.flip()
        clock.tick(120)

main()