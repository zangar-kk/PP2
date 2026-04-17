import pygame
import datetime

pygame.init()

# окно
WIDTH, HEIGHT = 900, 600
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

# загрузка
mikey = pygame.image.load(r"C:\Users\Admin\Downloads\mickeyclock (1).jpeg").convert()
rhand = pygame.image.load(r"C:\Users\Admin\Downloads\Rhand3.png").convert_alpha()
lhand = pygame.image.load(r"C:\Users\Admin\Downloads\Lhand3.png").convert_alpha()

# масштаб
mikey = pygame.transform.scale(mikey, (WIDTH, HEIGHT))
rhand = pygame.transform.scale(rhand, (900, 600))
lhand = pygame.transform.scale(lhand, (900, 600))


# центр часов
center = (WIDTH // 2, HEIGHT // 2)
font = pygame.font.SysFont("Arial", 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # текущее время
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    time_str = now.strftime("%H:%M:%S")
    text = font.render(time_str, True, (0, 0, 0))

    # углы (если рука смотрит вверх)
    minute_angle = -minutes * 6+307
    second_angle = -seconds * 6+63

    # вращение
    rotated_min = pygame.transform.rotate(lhand, minute_angle)
    rotated_sec = pygame.transform.rotate(rhand, second_angle)

    # центрирование после rotation
    min_rect = rotated_min.get_rect(center=center)
    sec_rect = rotated_sec.get_rect(center=center)

    # отрисовка
    sc.blit(mikey, (0, 0))
    sc.blit(rotated_min, min_rect)
    sc.blit(rotated_sec, sec_rect)
    sc.blit(text, (400,0))
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()