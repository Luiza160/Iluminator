import numpy as np
import pandas as pd
import pygame

def sortear_inverso(elementos, pesos):
    
    epsilon=1e-10
    pesos_seguros = [p + epsilon for p in pesos]
    pesos_inversos = 1 / np.array(pesos_seguros)
    probabilidades = pesos_inversos / pesos_inversos.sum()
    
    return np.random.choice(elementos, p=probabilidades)


    

df = pd.read_excel("Dados_Iluminator.xlsx")

class Pergunta:
    def __init__(self, df, id):
        self.nome = id
        self.img = pygame.transform.scale(pygame.image.load(f"Imagens/perguntas/{id}.png"), (666, 194))  
        self.atributes = self.obter_dicionario_atributo(df, id)
    
    def calcular_q1(self, pessoas):
        q1 = 0
        for pessoa in pessoas:
            if self.atributes[pessoa.nome] ==1:
                q1 += 1
        return q1

    def obter_dicionario_atributo(self, df, nome_atributo):
        # Verificar se o atributo existe
        if nome_atributo not in df.columns:
            print(f"Atributo '{nome_atributo}' não encontrado!")
            return None
        
        # Criar dicionário de mapeamento
        nomes_para_valores = {}
        
        for _, row in df.iterrows():
            nome = row.iloc[0]  # Primeira coluna é o nome
            valor = row[nome_atributo]
            
            if pd.isna(valor):  # Usando pd.isna() que funciona melhor com pandas
                nomes_para_valores[nome] = 0
            else:
                nomes_para_valores[nome] = int(valor)  # Converte para inteiro
        
        return nomes_para_valores

class Pessoa:
    def __init__(self, df, nome_pessoa):
        self.nome = nome_pessoa
        self.atributes = self.obter_dicionario_pessoa(df, nome_pessoa)

    def obter_dicionario_pessoa(self, df, nome_pessoa):
        
        # Buscar a pessoa pelo nome
        pessoa_df = df[df.iloc[:, 0] == nome_pessoa]
        
        if pessoa_df.empty:
            print(f"Pessoa '{nome_pessoa}' não encontrada!")
            return None
        
        # Extrair a linha da pessoa
        row = pessoa_df.iloc[0]
        pessoa_dict = {}
        
        for atributo, valor in row[1:].items():  # Pula a coluna de nome
            
            if pd.isna(valor):  # Usando pd.isna() que funciona melhor com pandas
                pessoa_dict[atributo] = 0
            else:
                pessoa_dict[atributo] = int(valor)  # Converte para inteiro
        
        return pessoa_dict

pergunta = Pergunta(df, "pessoa")
print(pergunta.atributes["Felipe"])