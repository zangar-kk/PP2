import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    radius = 15
    x = 0
    y = 0
    mode = 'blue'
    points = []
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
                    mode = 'ereaser'
                    
                elif event.key == pygame.K_1:
                    sh ="circle"
                elif event.key == pygame.K_2:
                    sh ="rect"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    radius = min(200, radius + 1)
                elif event.button == 3: 
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                points.append(position)
                points = points[-256:]
                
        screen.fill((0, 0, 0))
        
        for i in range(len(points)-1):
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode,sh)
        
        pygame.display.flip()
        
        clock.tick(140)

def drawLineBetween(screen, index, start, end, width, color_mode, sh):
    c1 = max(0, min(255, 2 *index  - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'ereaser':
        color = (0,0,0)
    
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        if sh == "circle":
            pygame.draw.circle(screen, color, (x, y), width)
        if sh == "rect":
            pygame.draw.rect(screen, color, (x, y, 2*width, 2*width))
            

main()