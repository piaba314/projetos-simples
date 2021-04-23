#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importando bibliotecas nescessárias -----------------------------------------
import pygame
import random

pygame.init()

# constantes ------------------------------------------------------------------
LARGURA_DA_TELA = 800
ALTURA_DA_TELA = 600
FPS = 60

LARGURA_DO_JOGADOR = 20
ALTURA_DO_JOGADOR = 120
RAIO_DA_BOLA = 10
VELOCIDADE_MAXIMA_DO_JOGADOR = 10

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# objetos do jogo -------------------------------------------------------------
class Jogador:
    def __init__(self, x, y, controles):
        self.rect = pygame.Rect(0, 0, LARGURA_DO_JOGADOR, ALTURA_DO_JOGADOR)
        self.rect.center = (x, y)
        self.controles = controles
        self.yvel = 0
        
    def desenha(self, tela):
        pygame.draw.rect(tela, BRANCO, self.rect)
    
    def atualiza(self, delta):
        self.rect.y += self.yvel
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.yvel = 0
        if self.rect.bottom > ALTURA_DA_TELA:
            self.rect.bottom = ALTURA_DA_TELA
            self.yvel = 0
    
    def controla(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == self.controles["cima"]:
                self.yvel = -VELOCIDADE_MAXIMA_DO_JOGADOR
            if evento.key == self.controles["baixo"]:
                self.yvel = VELOCIDADE_MAXIMA_DO_JOGADOR
        
        if evento.type == pygame.KEYUP:
            if evento.key == self.controles["cima"]:
                self.yvel = 0
            if evento.key == self.controles["baixo"]:
                self.yvel = 0

class Bola:
    def __init__(self):
        self.rect = pygame.Rect(9, 0, 2*RAIO_DA_BOLA, 2*RAIO_DA_BOLA)
        self.rect.center = LARGURA_DA_TELA//2, ALTURA_DA_TELA//2
        self.xvel = 5
        self.yvel = 4
    
    def desenha(self, tela):
        pygame.draw.circle(tela, BRANCO, self.rect.center, RAIO_DA_BOLA)
    
    def atualiza(self, delta):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        
        if self.rect.top < 0 or self.rect.bottom > ALTURA_DA_TELA:
            self.yvel *= -1
                   
# cenas do jogo ---------------------------------------------------------------
class TelaInicial:
    def __init__(self):
        fonte = pygame.font.SysFont("arial", 120)
        self.titulo_surface = fonte.render("Pong", True, BRANCO)
        self.titulo_rect = self.titulo_surface.get_rect()
        self.titulo_rect.center = LARGURA_DA_TELA//2, ALTURA_DA_TELA//2
        
        fonte = pygame.font.SysFont("arial", 25)
        self.subtitulo_surface = fonte.render("Pressione [Enter] para jogar.", True, BRANCO)
        self.subtitulo_rect = self.subtitulo_surface.get_rect()
        self.subtitulo_rect.midbottom = LARGURA_DA_TELA//2, ALTURA_DA_TELA-20
        self.cronometro_sub_titulo = 0
        self.tempo_de_animacao = 2
        
        self.titulo_xvel = 5
        self.titulo_yvel = 4
        
    def desenha(self, tela):
        tela.blit(self.titulo_surface, self.titulo_rect)
        
        subtitulo_surface_copia = self.subtitulo_surface.copy()
        alfa = self.cronometro_sub_titulo/self.tempo_de_animacao
        if self.cronometro_sub_titulo <= self.tempo_de_animacao//2:
            subtitulo_surface_copia.set_alpha((1-alfa)*50 + alfa*255)
        else:
            subtitulo_surface_copia.set_alpha((1-alfa)*255 + alfa*50)
        tela.blit(subtitulo_surface_copia, self.subtitulo_rect)
        
        
    def atualiza(self, delta):
        self.titulo_rect.x +=  int(self.titulo_xvel)
        self.titulo_rect.y += int(self.titulo_yvel)
        
        if self.titulo_rect.right > LARGURA_DA_TELA or self.titulo_rect.left < 0:
            self.titulo_xvel *= -1
        
        if self.titulo_rect.top < 0 or self.titulo_rect.bottom > ALTURA_DA_TELA:
            self.titulo_yvel *= -1
        
        self.cronometro_sub_titulo += delta
        if self.cronometro_sub_titulo >= self.tempo_de_animacao:
            self.cronometro_sub_titulo = 0
    
    def processa_eventos(self, evento):
        pass
            
class TelaDeJogo:
    def __init__(self):
        self.jogador1 = Jogador(LARGURA_DO_JOGADOR//2 + 20, ALTURA_DA_TELA//2, {"cima": pygame.K_w, "baixo": pygame.K_s})
        self.jogador2 = Jogador(LARGURA_DA_TELA - 20 - LARGURA_DO_JOGADOR//2, ALTURA_DA_TELA//2, {"cima": pygame.K_UP, "baixo": pygame.K_DOWN})
        self.bola = Bola()
        
    def desenha(self, tela):
        self.jogador1.desenha(tela)
        self.jogador2.desenha(tela)
        self.bola.desenha(tela)
    
    def atualiza(self, delta):
        self.jogador1.atualiza(delta)
        self.jogador2.atualiza(delta)
        self.bola.atualiza(delta)
        
        # verifica colisão entre bola e jogadores
        if self.bola.rect.collidelist([self.jogador1.rect, self.jogador2.rect]) != -1:
            self.bola.xvel *= -1
    
    def processa_eventos(self, evento):
        self.jogador1.controla(evento)
        self.jogador2.controla(evento)
        
# função principal ------------------------------------------------------------
def main():
    # cria tela, coloca título e cria relogio
    tela = pygame.display.set_mode((LARGURA_DA_TELA, ALTURA_DA_TELA),pygame.DOUBLEBUF)
    pygame.display.set_caption("Copia do Pong")
    relogio = pygame.time.Clock()
    
    # cria cenas
    tela_inicial = TelaInicial()
    tela_de_jogo = TelaDeJogo()
    
    tela_atual = tela_inicial
    
    # laço principal de jogo
    rodando = 1
    while rodando:
        # conta o tempo desde um último frame
        delta = relogio.tick(FPS)/1000
        
        # processa eventos do mouse e do teclado
        for evento in pygame.event.get():
            # fecha se usuario clicar no x
            if evento.type == pygame.QUIT:
                rodando = 0
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if tela_atual == tela_inicial:
                        tela_atual = tela_de_jogo
            
            tela_atual.processa_eventos(evento)
        
        # atualiza mundo do jogo
        tela_atual.atualiza(delta)
        
        # desenha alguma coisa
        tela.fill(PRETO)
        
        tela_atual.desenha(tela)
        
        # atualiza a janela
        pygame.display.update()
    
    # encerra o jogo
    pygame.quit()

if __name__ == "__main__":
    main()
    
