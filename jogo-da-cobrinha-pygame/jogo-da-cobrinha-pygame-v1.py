#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importando bibliotecas nescessárias -----------------------------------------
import pygame
import random

# constantes ------------------------------------------------------------------
LARGURA_DA_TELA = 800
ALTURA_DA_TELA = 600
TAMANHO_DA_CELULA = 25
LARGURA_DA_GRADE = LARGURA_DA_TELA // TAMANHO_DA_CELULA
ALTURA_DA_GRADE = ALTURA_DA_TELA // TAMANHO_DA_CELULA

FPS = 60

PRETO = (0, 0, 0)
CINZA = (130, 130, 130)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

# classes e objetos -----------------------------------------------------------
class Celula:
    def __init__(self, x_grade, y_grade):
        self.x_grade = x_grade
        self.y_grade = y_grade
    
    def desenha(self, tela):
        x = self.y_grade*TAMANHO_DA_CELULA
        y = self.x_grade*TAMANHO_DA_CELULA
        pygame.draw.rect(tela, VERDE, (x, y, TAMANHO_DA_CELULA-2, TAMANHO_DA_CELULA-2))
    
class Cobra:
    def __init__(self, x_grade, y_grade):
        self.cabeca = Celula(x_grade, y_grade)
        self.corpo = [self.cabeca, Celula(x_grade, y_grade-1), Celula(x_grade, y_grade-2)]
        self.direcao = "direita"
        self.viva = True
        
        self.cronometro = 0
        self.tempo_maximo = 100
    
    def move(self, delta):
        self.cronometro += delta
        
        if self.cronometro >= self.tempo_maximo:
            if self.viva:
                # move corpo
                for i in range(len(self.corpo)-1, 0, -1):
                    self.corpo[i].x_grade = self.corpo[i-1].x_grade
                    self.corpo[i].y_grade = self.corpo[i-1].y_grade
                
                # move cabeça
                if self.direcao == "direita":
                    self.cabeca.y_grade += 1
                if self.direcao == "esquerda":
                    self.cabeca.y_grade -= 1
                if self.direcao == "cima":
                    self.cabeca.x_grade -= 1
                if self.direcao == "baixo":
                    self.cabeca.x_grade += 1
                
                # checa colisão da cabeça com o corpo
                for celula in self.corpo[1:]:
                    if self.cabeca.x_grade == celula.x_grade and self.cabeca.y_grade == celula.y_grade:
                        self.viva = False
                
                # checa colisão com paredes
                if (self.cabeca.x_grade >= ALTURA_DA_GRADE or self.cabeca.x_grade < 0 or
                    self.cabeca.y_grade < 0 or self.cabeca.y_grade >= LARGURA_DA_GRADE):
                    self.viva = False
        
            self.cronometro = 0 
    
    def controla(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                if self.direcao == "cima" or self.direcao == "baixo":
                    self.direcao = "direita"
            if evento.key == pygame.K_LEFT:
                if self.direcao == "cima" or self.direcao == "baixo":
                    self.direcao = "esquerda"
            if evento.key == pygame.K_DOWN:
                if self.direcao == "direita" or self.direcao == "esquerda":
                    self.direcao = "baixo"
            if evento.key == pygame.K_UP:
                if self.direcao == "direita" or self.direcao == "esquerda":
                    self.direcao = "cima"
                
    def desenha(self, tela):
        self.cabeca.desenha(tela)
        for celula in self.corpo:
            celula.desenha(tela)

class Comida:
    def __init__(self):
        self.x_grade = random.randint(0, ALTURA_DA_GRADE-1)
        self.y_grade = random.randint(0, LARGURA_DA_GRADE-1)
    
    def desenha(self, tela):
        x = self.y_grade*TAMANHO_DA_CELULA
        y = self.x_grade*TAMANHO_DA_CELULA
        pygame.draw.rect(tela, VERMELHO, (x, y, TAMANHO_DA_CELULA-2, TAMANHO_DA_CELULA-2))
    
    def muda_posicao(self):
        self.x_grade = random.randint(0, ALTURA_DA_GRADE-1)
        self.y_grade = random.randint(0, LARGURA_DA_GRADE-1)
        
# funções ---------------------------------------------------------------------
def desenha_grade(tela):
    tela.fill(CINZA)
    
    for i in range(ALTURA_DA_GRADE):
        for j in range(LARGURA_DA_GRADE):
            pygame.draw.rect(tela, PRETO, (j*TAMANHO_DA_CELULA, i*TAMANHO_DA_CELULA, TAMANHO_DA_CELULA-2, TAMANHO_DA_CELULA-2))

def checa_colisao_cobra_comida(cobra, comida):
    global score
    if cobra.cabeca.x_grade == comida.x_grade and cobra.cabeca.y_grade == comida.y_grade:
        comida.muda_posicao()
        cobra.corpo.append(Celula(-1, -1))
        score += 1

def desenha_score(fonte, tela):
    superficie = fonte.render("Score: {}".format(score), True, BRANCO)
    tela.blit(superficie, (20, 20))
    
    superficie = fonte.render("High Score: {}".format(max_score), True, BRANCO)
    r = superficie.get_rect() # objeto do pygame que ajuda a posicionar coisas na tela
    r.right = LARGURA_DA_TELA - 20
    r.top = 20
    tela.blit(superficie, r)

def atualiza_score_maximo():
    global max_score
    if score > max_score:
        max_score = score

def desenha_mensagem_de_fim_de_jogo(tela):
    fonte = pygame.font.SysFont("arial", 80)
    superficie = fonte.render("Game Over", True, AMARELO)
    r = superficie.get_rect()
    r.center = (LARGURA_DA_TELA//2, ALTURA_DA_TELA//2 - 50)
    tela.blit(superficie, r)
    
    fonte = pygame.font.SysFont("arial", 20)
    superficie = fonte.render("Pressione [ENTER] para jogar de novo.", True, BRANCO)
    r = superficie.get_rect()
    r.center = (LARGURA_DA_TELA//2, ALTURA_DA_TELA//2)
    tela.blit(superficie, r)
    

# variáveis globais -----------------------------------------------------------
score = 0
with open("high-score.txt", 'r') as arquivo:
    high_score = int(arquivo.readline())
    
# função principal ------------------------------------------------------------
def main():
    global score
    # inicia pygame
    pygame.init()
    
    # cria objetos
    tela = pygame.display.set_mode((LARGURA_DA_TELA, ALTURA_DA_TELA))
    pygame.display.set_caption("Jogo da Cobrinha")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 30)
    
    cobra = Cobra(5, 5)
    comida = Comida()
    
    # laço principal do jogo
    rodando = True
    while rodando:
        # limita o número de quadros por segundo
        delta = relogio.tick(FPS)
        
        # processa eventos do mouse e teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and not cobra.viva:
                    cobra = Cobra(5, 5)
                    comida.muda_posicao()
                    score = 0
            
            cobra.controla(evento)
        
        # atualiza o mundo do jogo
        cobra.move(delta)
        checa_colisao_cobra_comida(cobra, comida)
        atualiza_score_maximo()
        
        # desenha objetos e atualiza a janela
        tela.fill(PRETO)
        # desenha_grade(tela)
        comida.desenha(tela)
        cobra.desenha(tela)
        desenha_score(fonte, tela)
        
        # se a cobra não estiver viva, desenha mensagem de game over
        if not cobra.viva:
            desenha_mensagem_de_fim_de_jogo(tela)
        
        pygame.display.update()
    
    # salva score maximo
    with open("high-score.txt", "w") as arquivo:
        arquivo.write(str(high_score))
    
    # encerra o jogo
    pygame.quit()

if __name__ == "__main__":
    main()
