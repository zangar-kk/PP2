import pygame

pygame.init()
pygame.mixer.init()

sc = pygame.display.set_mode((900,600), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
WHITE =(255,255,255)

cur = 0
folder = r"C:\Users\Admin\Downloads\music"
playlist = ["Billie Eilish - Ocean Eyes.mp3", "Travis Scott feat. Drake - Sicko Mode.mp3", "Kehlani & Missy Elliott - Back and Forth.mp3"]
path = folder+ "\\"+ playlist[cur]
pygame.mixer.music.load(path)
pygame.mixer.music.play()
sound = pygame.mixer.Sound(path)
lenght= sound.get_length()
play = 1



run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cur = (cur + 1) % len(playlist)
                pygame.mixer.music.load(folder + "\\" + playlist[cur])
                pygame.mixer.music.play()

                sound = pygame.mixer.Sound(folder + "\\" + playlist[cur])
                lenght= sound.get_length()

            if event.key == pygame.K_LEFT:
                cur = (cur + 1) % len(playlist)
                pygame.mixer.music.load(folder + "\\" + playlist[cur])
                pygame.mixer.music.play()

                sound = pygame.mixer.Sound(folder + "\\" + playlist[cur])
                lenght= sound.get_length()
            if event.key == pygame.K_SPACE:
                if play:
                    pygame.mixer.music.pause()
                    play = 0
                else:
                    pygame.mixer.music.unpause()
                    play = 1
            if event.key == pygame.K_q:
                run = False
    
    
    sc.fill((0,0,0))

    timem = pygame.mixer.music.get_pos()
    total = timem // 1000
    sec = total //60
    min = sec //60

    minutes = int(lenght // 60)
    seconds = int(lenght % 60)

    timelen = f"{minutes:02}:{seconds:02}"
    time = f"{min:02}:{sec:02}"
    #op = "\nNEXT: -> \nPREVIOUS: <- \nQUIT: q"
    song = playlist[cur]


    text = font.render(time, True, WHITE)
    text2 = font.render(song,True, WHITE)
    text3 = font.render(timelen,True, WHITE)
    sc.blit(text, (0,30))
    sc.blit(text2, (0,0))
    sc.blit(text3, (100,30))
  
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()
