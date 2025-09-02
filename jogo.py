import pygame, sys
import pandas as pd
from classes import Pessoa, Pergunta
from pygame.locals import *
from config import window_width, window_height

pygame.display.set_caption("Iluminator")

def run(screen, clock):
    # --- CARREGAR IMAGENS ---
    background = pygame.image.load("Imagens/bg_jogo.png").convert()
    background = pygame.transform.scale(background, (window_width, window_height))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)


    # Rects dos botões
    rect_sim = pygame.Rect(671, 281, 373, 69)
    rect_talvez_sim = pygame.Rect(671, 373, 373, 69)
    rect_nao_sei = pygame.Rect(671, 466, 373, 69)
    rect_talvez_nao = pygame.Rect(671, 559, 373, 69)
    rect_nao = pygame.Rect(671, 651, 373, 69)

    # Gerar pessoas
    pessoas = []
    df = pd.read_excel("Dados_Iluminator.xlsx")
    for pessoa in df.iloc[:, 0]:
        pessoas.append(Pessoa(df, pessoa))
    

    # Gerar perguntas
    perguntas = []
    for atributo in df.columns[1:]:
        perguntas.append(Pergunta(df, atributo))
    

    print(perguntas[0].nome)

    running = True

    def analisar_perguntas(perguntas, pessoas):
        alfa = len(pessoas)/2
        for pergunta in perguntas:
            q1 = pergunta.calcular_q1(pessoas)
            pergunta.beta = abs(alfa-q1)
        return sorted(perguntas, key=lambda x: x.beta)



    while running:
        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if rect_sim.collidepoint(mouse_pos):
                    pessoas_possiveis = []
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] == 1:
                            pessoas_possiveis.append(pessoa)
                    pessoas = pessoas_possiveis
                    perguntas.pop(0)
                    for pessoa in pessoas:
                        print(pessoa.nome)
                    
                    print(len(pessoas))
                    print(perguntas[0].nome)
                    print(f"q1 = {perguntas[0].calcular_q1(pessoas)}")
                    print(f"alpha = {len(pessoas)/2}")
                    perguntas = analisar_perguntas(perguntas, pessoas)
                    for pergunta in perguntas:
                        print(pergunta.nome, pergunta.beta)

                if rect_talvez_sim.collidepoint(mouse_pos): 
                    pessoas_possiveis = []
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] == 1:
                            pessoas_possiveis.append(pessoa)
                    pessoas = pessoas_possiveis
                    perguntas.pop(0)
                    for pessoa in pessoas:
                        print(pessoa.nome)
                    
                    print(len(pessoas))
                    print(perguntas[0].nome)
                    print(f"q1 = {perguntas[0].calcular_q1(pessoas)}")
                    print(f"alpha = {len(pessoas)/2}")
                    perguntas = analisar_perguntas(perguntas, pessoas)
                    for pergunta in perguntas:
                        print(pergunta.nome, pergunta.beta)

                if rect_nao_sei.collidepoint(mouse_pos):
                    perguntas.pop(0)
                    print(len(pessoas))
                    print(perguntas[0].nome)
                    print(f"q1 = {perguntas[0].calcular_q1(pessoas)}")
                    print(f"alpha = {len(pessoas)/2}")
                    perguntas = analisar_perguntas(perguntas, pessoas)
                    for pessoa in pessoas:
                        print(pessoa.nome)
                    for pergunta in perguntas:
                        print(pergunta.nome, pergunta.beta)

                if rect_talvez_nao.collidepoint(mouse_pos):       
                    pessoas_possiveis = []
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] == 0:
                            pessoas_possiveis.append(pessoa)
                    pessoas = pessoas_possiveis
                    perguntas.pop(0)

                    for pessoa in pessoas:
                        print(pessoa.nome)
                    
                    print(len(pessoas))
                    print(perguntas[0].nome)
                    print(f"q1 = {perguntas[0].calcular_q1(pessoas)}")
                    print(f"alpha = {len(pessoas)/2}")
                    perguntas = analisar_perguntas(perguntas, pessoas)
                    for pergunta in perguntas:
                        print(pergunta.nome, pergunta.beta)

                if rect_nao.collidepoint(mouse_pos):
                    pessoas_possiveis = []
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] == 0:
                            pessoas_possiveis.append(pessoa)
                    pessoas = pessoas_possiveis
                    perguntas.pop(0)
                    for pessoa in pessoas:
                        print(pessoa.nome)
                    
                    print(len(pessoas))
                    print(perguntas[0].nome)
                    print(f"q1 = {perguntas[0].calcular_q1(pessoas)}")
                    print(f"alpha = {len(pessoas)/2}")
                    perguntas = analisar_perguntas(perguntas, pessoas)
                    for pergunta in perguntas:
                        print(pergunta.nome, pergunta.beta)

        if len(pessoas) == 1:
            print(f"O seu personagem é: {pessoas[0].nome}")

        mouse_pos = pygame.mouse.get_pos()

        # --- DESENHO  ---
        screen.blit(background, (0, 0))    
        foreground.fill((0, 0, 0, 0))  

        foreground.blit(perguntas[0].img, (535, 63)) 
        screen.blit(foreground, (0, 0)) 
        pygame.display.flip()
        clock.tick(60)
