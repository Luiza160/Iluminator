import pygame, sys
import pandas as pd
import numpy as np
from classes import Pessoa, Pergunta, Botao_hover, CaixaTexto
from textos import PERGUNTAS
from pygame.locals import *
from config import window_width, window_height

pygame.display.set_caption("Iluminator")

def adicionar(screen, clock):
    # --- CARREGAR IMAGENS ---
    background = pygame.image.load("Imagens/bg_jogo.png").convert()
    background = pygame.transform.scale(background, (window_width, window_height))
    foreground = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    fundo_derrota = pygame.image.load("Imagens/derrota.png").convert()

    # Gerar botões
    sim = Botao_hover((373, 69), (420, 77), (858, 315), "sim")
    prov_sim = Botao_hover((373, 69), (420, 77), (858, 408), "prov_sim")
    nao_sei = Botao_hover((373, 69), (420, 77), (858, 500), "nao_sei")
    prov_nao = Botao_hover((373, 69), (420, 77), (858, 593), "prov_nao")
    nao = Botao_hover((373, 69), (420, 77), (858, 686), "nao")

    enviar = Botao_hover((313, 69), (351, 77), (1044, 696), "enviar")
    sair = Botao_hover((313, 69), (351, 77), (673, 696), "sair")

    caixa_texto = CaixaTexto(516, 541, 684, 69)

    # Carregar fonte
    fonte = pygame.font.Font("JetBrainsMono-Bold.ttf", 33)
    fonte_mini = pygame.font.Font("JetBrainsMono-Bold.ttf", 20)

    # Gerar pessoas
    pessoas = []
    df = pd.read_excel("Dados_Iluminator.xlsx")
    for pessoa in df.iloc[:, 0]:
        pessoas.append(Pessoa(df, pessoa, 1))

    # Normaliza a probabilidade das pessoas
    def normalizar_pessoas(pessoas):
        prob_total = 0
        for pessoa in pessoas:
            prob_total += pessoa.prob
        for pessoa in pessoas:
            pessoa.prob = pessoa.prob/prob_total
    
    normalizar_pessoas(pessoas)

    # Gerar perguntas
    perguntas = []
    for atributo in df.columns[1:]:
        perguntas.append(Pergunta(df, atributo, fonte, (183, 110, 34)))
    
    # Atualiza o dataset após o término do jogo
    def atualizar_dados(respostas, pessoa):
        df = pd.read_excel("Dados_Iluminator.xlsx")
        if pessoa not in df["Nome"].values:
            nova_pessoa = {col: 0 for col in df.columns}
            nova_pessoa["Nome"] = pessoa
            df = pd.concat([df, pd.DataFrame([nova_pessoa])], ignore_index=True)

        for pergunta in respostas.keys():
            df.loc[df["Nome"] == pessoa, pergunta.nome] += respostas[pergunta]

        df.to_excel("Dados_Iluminator.xlsx", index=False)

    # Guarda as respostas do jogador
    respostas = {}

    running = True
    state = "plain"

    while running:
        # --- EVENTOS ---
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == QUIT: # Sair do sistema
                pygame.quit(); sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE: #ESC
                return False

            if event.type == MOUSEBUTTONDOWN and event.button == 1: #Clique com botão esquerdo

                # SIM
                if sim.rect.collidepoint(mouse_pos):
                    # Guarda a resposta
                    respostas[perguntas[0]] = 3

                    # Atualiza as probabilidades
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] > 0.5:
                            pessoa.prob = pessoa.prob*0.95
                        elif perguntas[0].atributes[pessoa.nome] < 0.5:
                            pessoa.prob = pessoa.prob*0.05
                    normalizar_pessoas(pessoas)

                    # Remove pergunta e reorganiza
                    perguntas.pop(0)

                # PROVAVELMENTE SIM
                if prov_sim.rect.collidepoint(mouse_pos):
                    # Guarda a resposta
                    respostas[perguntas[0]] = 2

                    # Atualiza as probabilidades
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] > 0.5:
                            pessoa.prob = pessoa.prob*0.75
                        elif perguntas[0].atributes[pessoa.nome] < 0.5:
                            pessoa.prob = pessoa.prob*0.25
                    normalizar_pessoas(pessoas)

                    # Remove pergunta e reorganiza
                    perguntas.pop(0)

                # NÃO SEI
                if nao_sei.rect.collidepoint(mouse_pos):
                    # Guarda a resposta
                    respostas[perguntas[0]] = 0

                    # Remove pergunta e reorganiza
                    perguntas.pop(0)

                # PROVAVELMENTE NÃO
                if prov_nao.rect.collidepoint(mouse_pos):   
                    # Guarda a resposta
                    respostas[perguntas[0]] = -2

                    # Atualiza as probabilidades
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] > 0.5:
                            pessoa.prob = pessoa.prob*0.25
                        elif perguntas[0].atributes[pessoa.nome] < 0.5:
                            pessoa.prob = pessoa.prob*0.75
                    normalizar_pessoas(pessoas)

                    # Remove pergunta e reorganiza
                    perguntas.pop(0)

                # NÃO
                if nao.rect.collidepoint(mouse_pos):
                    # Guarda a resposta
                    respostas[perguntas[0]] = -3

                    # Atualiza as probabilidades
                    for pessoa in pessoas:
                        if perguntas[0].atributes[pessoa.nome] > 0.5:
                            pessoa.prob = pessoa.prob*0.05
                        elif perguntas[0].atributes[pessoa.nome] < 0.5:
                            pessoa.prob = pessoa.prob*0.95
                    normalizar_pessoas(pessoas)

                    # Remove pergunta e reorganiza
                    perguntas.pop(0)

        # Checa se há perguntas disponíveis
        if len(perguntas) > 0:

            # --- DESENHO  ---
            screen.blit(background, (0, 0))    
            foreground.fill((0, 0, 0, 0))  
            sim.draw(foreground)
            prov_sim.draw(foreground)
            nao_sei.draw(foreground)
            prov_nao.draw(foreground)
            nao.draw(foreground)
            perguntas[0].draw(foreground)

            #foreground.blit(perguntas[0].img, (535, 63)) 
            screen.blit(foreground, (0, 0)) 
            pygame.display.flip()
            clock.tick(60)
        else:
            state = "derrota"

        #-----TELA DE DERROTA-----
        while state == "derrota":
            screen.blit(fundo_derrota, (0, 0))  
            caixa_texto.draw(fonte, screen)
            enviar.draw(screen)
            sair.draw(screen)
            
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == QUIT: # Sair do sistema
                    pygame.quit(); sys.exit()

                if event.type == KEYDOWN and event.key == K_ESCAPE: #ESC
                    return False

                caixa_texto.manipular_evento(event)

                if event.type == MOUSEBUTTONDOWN and event.button == 1: #Clique com botão esquerdo

                    # ENVIAR
                    if enviar.rect.collidepoint(mouse_pos):
                        gabarito = caixa_texto.texto.title()
                        atualizar_dados(respostas, gabarito)
                        return False
                    
                    # SAIR
                    if sair.rect.collidepoint(mouse_pos):
                        return False

            pygame.display.flip()
            clock.tick(60)
        
