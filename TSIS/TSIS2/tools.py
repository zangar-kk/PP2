import pygame
import math
from datetime import datetime


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

def draw_pencil(surface, color, last_pos, current_pos, size):
    if last_pos:
        pygame.draw.line(surface, color, last_pos, current_pos, size)
    return current_pos


def preview_line(surface, base_layer, color, start_pos, current_pos, size):
    surface.blit(base_layer, (0, 0))
    pygame.draw.line(surface, color, start_pos, current_pos, size)

def draw_shape(surface, shape, color, pos, size):
    x, y = pos

    if shape == "circle":
        pygame.draw.circle(surface, color, (x, y), size)

    elif shape == "rect":
        pygame.draw.rect(surface, color, (x, y, 2*size, 2*size))

    elif shape == "triangle":
        pygame.draw.polygon(surface, color, [
            (x, y),
            (x+size, y+size*math.sqrt(3)),
            (x-size, y+size*math.sqrt(3))
        ])

    elif shape == "romb":
        pygame.draw.polygon(surface, color, [
            (x, y),
            (x+size, y+size*math.sqrt(3)),
            (x, y+2*size*math.sqrt(3)),
            (x-size, y+size*math.sqrt(3))
        ])

def draw_text(surface, font, text, pos, color):
    img = font.render(text, True, color)
    surface.blit(img, pos)

def save_canvas(surface):
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(surface, filename)
    print("Saved:", filename)