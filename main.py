import pygame, sys
from pygame.locals import *
from config import window_width, window_height, screen, clock
from jogo import run

pygame.display.set_caption("Iluminator")

# --- CARREGAR IMAGENS ---
background = pygame.image.load("Imagens/main_menu.png").convert()
background = pygame.transform.scale(background, (window_width, window_height))

botao_normal = pygame.transform.scale(pygame.image.load("Imagens/jogar.png").convert_alpha(), (373, 69))
botao_hover  = pygame.transform.scale(pygame.image.load("Imagens/jogar_hover.png").convert_alpha(), (444, 100))

# Posição do botão
botao_center = (815, 503)  # (628 + 373/2, 468 + 69/2)

# Rects dos botões
rect_normal = botao_normal.get_rect(center=botao_center)
rect_hover  = botao_hover.get_rect(center=botao_center)

while True:
    # --- EVENTOS ---
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit(); sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # botão esquerdo
            if rect_hover.collidepoint(mouse_pos):
                run(screen, clock)

    mouse_pos = pygame.mouse.get_pos()

    # --- LÓGICA DE HOVER ---
    hovering = rect_normal.collidepoint(mouse_pos) or rect_hover.collidepoint(mouse_pos)
    if hovering:
        botao_img  = botao_hover
        botao_rect = rect_hover
    else:
        botao_img  = botao_normal
        botao_rect = rect_normal

    # --- DESENHO  ---
    screen.blit(background, (0, 0))             # fundo
    screen.blit(botao_img, botao_rect.topleft)  # botão

    pygame.display.flip()
    clock.tick(60)
