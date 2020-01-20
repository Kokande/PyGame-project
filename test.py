import pygame

screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
game_on = True
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                game_on = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    screen.fill((0, 0, 0))
    pygame.display.flip()
