import pygame
import math
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 640, 480
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
sc.fill(WHITE)

font = pygame.font.SysFont("Arial", 20)

def get_color(mode):
    if mode == 'red': return (255,0,0)
    if mode == 'green': return (0,255,0)
    if mode == 'eraser': return WHITE
    return (0,0,255)

def flood_fill(surface, x, y, new_color):
    target = surface.get_at((x,y))
    if target == new_color: return

    w,h = surface.get_size()
    stack = [(x,y)]

    while stack:
        px,py = stack.pop()
        if px<0 or py<0 or px>=w or py>=h: continue
        if surface.get_at((px,py)) != target: continue

        surface.set_at((px,py), new_color)

        stack.append((px+1,py))
        stack.append((px-1,py))
        stack.append((px,py+1))
        stack.append((px,py-1))

def main():
    mode = 'blue'
    tool = "pencil"
    sh = "circle"

    brush_size = 5

    drawing = False
    last_pos = None
    start_pos = None
    base_layer = sc.copy()

    # text tool
    typing = False
    text = ""
    text_pos = (0,0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # --- клавиши ---
            if event.type == pygame.KEYDOWN:

                # SAVE
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                    pygame.image.save(sc, filename)
                    print("Saved:", filename)

                # TEXT TOOL typing
                elif typing:
                    if event.key == pygame.K_RETURN:
                        img = font.render(text, True, get_color(mode))
                        sc.blit(img, text_pos)
                        typing = False
                        text = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

                else:
                    # цвет
                    if event.key == pygame.K_r: mode = 'red'
                    elif event.key == pygame.K_g: mode = 'green'
                    elif event.key == pygame.K_b: mode = 'blue'
                    elif event.key == pygame.K_e: mode = 'eraser'
                    elif event.key == pygame.K_c: sc.fill(WHITE)

                    # размер
                    elif event.key == pygame.K_1: brush_size = 2
                    elif event.key == pygame.K_2: brush_size = 5
                    elif event.key == pygame.K_3: brush_size = 10

                    # инструменты
                    elif event.key == pygame.K_z: tool = "pencil"
                    elif event.key == pygame.K_x: tool = "line"
                    elif event.key == pygame.K_s: tool = "shape"
                    elif event.key == pygame.K_f: tool = "fill"
                    elif event.key == pygame.K_t: tool = "text"

                    # фигуры
                    elif event.key == pygame.K_q: sh="circle"
                    elif event.key == pygame.K_w: sh="rect"
                    elif event.key == pygame.K_a: sh="triangle"
                    elif event.key == pygame.K_d: sh="romb"

            # --- мышь ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tool == "fill":
                    flood_fill(sc, *event.pos, get_color(mode))

                elif tool == "text":
                    typing = True
                    text = ""
                    text_pos = event.pos

                else:
                    drawing = True
                    if tool == "line":
                        start_pos = event.pos
                        base_layer = sc.copy()

            if event.type == pygame.MOUSEBUTTONUP:
                if tool == "line" and start_pos:
                    sc.blit(base_layer, (0,0))
                    pygame.draw.line(sc, get_color(mode), start_pos, event.pos, brush_size)
                    start_pos = None

                drawing = False
                last_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                x,y = event.pos
                color = get_color(mode)

                if tool == "pencil":
                    if last_pos:
                        pygame.draw.line(sc, color, last_pos, (x,y), brush_size)
                    last_pos = (x,y)

                elif tool == "shape":
                    if sh=="circle":
                        pygame.draw.circle(sc, color, (x,y), brush_size)
                    elif sh=="rect":
                        pygame.draw.rect(sc, color, (x,y,2*brush_size,2*brush_size))
                    elif sh=="triangle":
                        pygame.draw.polygon(sc, color, [
                            (x,y),
                            (x+brush_size, y+brush_size*math.sqrt(3)),
                            (x-brush_size, y+brush_size*math.sqrt(3))
                        ])
                    elif sh=="romb":
                        pygame.draw.polygon(sc, color, [
                            (x,y),
                            (x+brush_size, y+brush_size*math.sqrt(3)),
                            (x,y+2*brush_size*math.sqrt(3)),
                            (x-brush_size, y+brush_size*math.sqrt(3))
                        ])

        # line preview
        if drawing and tool=="line" and start_pos:
            sc.blit(base_layer,(0,0))
            pygame.draw.line(sc, get_color(mode), start_pos, pygame.mouse.get_pos(), brush_size)

        # text preview
        if typing:
            temp = font.render(text, True, get_color(mode))
            sc.blit(temp, text_pos)

        pygame.display.flip()
        clock.tick(120)

main()