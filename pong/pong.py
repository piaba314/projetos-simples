#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importando bibliotecas nescessárias -----------------------------------------
import pygame
import random
import math

pygame.init()

# constantes ------------------------------------------------------------------
LARGURA_DA_TELA = 800
ALTURA_DA_TELA = 600
FPS = 60

LARGURA_DO_JOGADOR = 20
ALTURA_DO_JOGADOR = 120
VELOCIDADE_MAXIMA_DO_JOGADOR = 10

RAIO_DA_BOLA = 10
ANGULO_MAXIMO_DE_REBATE = 60
INCREMENTO_NA_VELOCIDADE_DA_BOLA = 0.5
VELOCIDADE_INICIAL_DA_BOLA = 5
VELOCIDADE_MAXIMA_DA_BOLA = 20

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# objetos do jogo -------------------------------------------------------------
class Jogador:
    def __init__(self, x, y, controles):
        self.rect = pygame.Rect(0, 0, LARGURA_DO_JOGADOR, ALTURA_DO_JOGADOR)
        self.rect.center = (x, y)
        self.controles = controles
        self.yvel = 0
        
        self.pontos = 0
        
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
        self.reinicia_bola(random.choice([-VELOCIDADE_INICIAL_DA_BOLA, VELOCIDADE_INICIAL_DA_BOLA]), 0)
    
    def desenha(self, tela):
        pygame.draw.circle(tela, BRANCO, self.rect.center, RAIO_DA_BOLA)
    
    def atualiza(self, delta):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        
        if self.rect.top < 0 or self.rect.bottom > ALTURA_DA_TELA:
            self.yvel *= -1
    
    def reinicia_bola(self, xvel, yvel):
        self.rect.center = LARGURA_DA_TELA//2, ALTURA_DA_TELA//2
        self.xvel = xvel
        self.yvel = yvel
                   
# telas do jogo ---------------------------------------------------------------
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
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self.gerenciador.va_para(TelaDeJogo())
            
class TelaDeJogo:
    def __init__(self):
        self.jogador1 = Jogador(LARGURA_DO_JOGADOR//2 + 20, ALTURA_DA_TELA//2, {"cima": pygame.K_w, "baixo": pygame.K_s})
        self.jogador2 = Jogador(LARGURA_DA_TELA - 20 - LARGURA_DO_JOGADOR//2, ALTURA_DA_TELA//2, {"cima": pygame.K_UP, "baixo": pygame.K_DOWN})
        self.bola = Bola()
        
        self.fonte_pontuacao = pygame.font.SysFont("arial", 50)
        
        self.rede_surface = pygame.Surface((5, ALTURA_DA_TELA))
        self.rede_rect = self.rede_surface.get_rect()
        self.rede_rect.midtop = (LARGURA_DA_TELA//2, 0)
        for i in range(0, ALTURA_DA_TELA//15):
            pygame.draw.rect(self.rede_surface, BRANCO, (0, 15*i, 5, 10))
        
        self.pausado = False
        
    def desenha(self, tela):
        self.jogador1.desenha(tela)
        self.jogador2.desenha(tela)
        tela.blit(self.rede_surface, self.rede_rect)
        self.bola.desenha(tela)
        self.desenha_pontuacao(tela)
        
        # verifica se alguem ganhou
        # essa verificação precisa ser feita aqui para capturarmos o plano de fundo
        # para a tela de fim de jogo
        if self.jogador1.pontos >= 7 or self.jogador2.pontos >= 7:
            self.gerenciador.va_para(TelaDeFimDeJogo())
    
    def atualiza(self, delta):
        if not self.pausado:
            self.jogador1.atualiza(delta)
            self.jogador2.atualiza(delta)
            self.bola.atualiza(delta)

            # verifica e resolve colisão entre bola e jogadores
            self.verifica_colisao_bola_jogador()

            # verifica se algum jogador marcou ponto
            if self.bola.rect.centerx > LARGURA_DA_TELA:
                self.jogador1.pontos += 1
                self.bola.reinicia_bola(-VELOCIDADE_INICIAL_DA_BOLA, 0)
            if self.bola.rect.centerx < 0:
                self.jogador2.pontos += 1
                self.bola.reinicia_bola(VELOCIDADE_INICIAL_DA_BOLA, 0)
                      
    def processa_eventos(self, evento):
        self.jogador1.controla(evento)
        self.jogador2.controla(evento)
        
        # pausa ou retorna o jogo pressionando [Enter]
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self.pausado = not self.pausado
        
    def verifica_colisao_bola_jogador(self):
        for jogador in [self.jogador1, self.jogador2]:
            if self.bola.rect.colliderect(jogador.rect):
                # calcule a diferença do ponot de contato até o meio do jogador
                d = jogador.rect.centery - self.bola.rect.centery
                # o ângulo de rebate será proporcional a essa diferença
                angulo_de_rebate = -math.radians(d/(ALTURA_DO_JOGADOR/2) * ANGULO_MAXIMO_DE_REBATE)
                # módulo da velocidade da bola
                v = (self.bola.xvel**2 + self.bola.yvel**2)**0.5
                # nova velocidade da bola
                v += INCREMENTO_NA_VELOCIDADE_DA_BOLA
                if v > VELOCIDADE_MAXIMA_DA_BOLA:
                    v = VELOCIDADE_MAXIMA_DA_BOLA
                
                self.bola.xvel = v * math.cos(angulo_de_rebate)
                self.bola.yvel = v * math.sin(angulo_de_rebate)
                
                if jogador == self.jogador2:
                    self.bola.xvel *= -1
    
    def desenha_pontuacao(self, tela):
        pontos_surface = self.fonte_pontuacao.render(str(self.jogador1.pontos), True, BRANCO)
        pontos_rect = pontos_surface.get_rect()
        pontos_rect.right = LARGURA_DA_TELA//2 - 30
        pontos_rect.top = 10
        tela.blit(pontos_surface, pontos_rect)
        
        pontos_surface = self.fonte_pontuacao.render(str(self.jogador2.pontos), True, BRANCO)
        pontos_rect = pontos_surface.get_rect()
        pontos_rect.left = LARGURA_DA_TELA//2 + 30
        pontos_rect.top = 10
        tela.blit(pontos_surface, pontos_rect)

class TelaDeFimDeJogo:
    def __init__(self):
        fonte = pygame.font.SysFont("arial", 80)
        self.titulo_surface = fonte.render("Fim de Jogo!", True, BRANCO)
        self.titulo_rect = self.titulo_surface.get_rect()
        self.titulo_rect.center = (LARGURA_DA_TELA//2, ALTURA_DA_TELA//2 - 100)
        
        fonte = pygame.font.SysFont("arial", 25)
        self.subtitulo_surface = fonte.render("Pressione [Enter] para jogar de novo.", True, BRANCO)
        self.subtitulo_rect = self.subtitulo_surface.get_rect()
        self.subtitulo_rect.centerx = LARGURA_DA_TELA//2
        self.subtitulo_rect.top = self.titulo_rect.bottom + 10
        self.cronometro_subtitulo = 0
        self.tempo_de_animacao_subtitulo = 2
        
    
    def desenha(self, tela):
        tela.blit(self.plano_de_fundo, (0, 0))
        
        tela.blit(self.titulo_surface, self.titulo_rect)
        
        self.subtitulo_surface_copia = self.subtitulo_surface.copy()
        alfa = self.cronometro_subtitulo/self.tempo_de_animacao_subtitulo
        if self.cronometro_subtitulo <= self.tempo_de_animacao_subtitulo/2:
            self.subtitulo_surface_copia.set_alpha((1-alfa)*50 + alfa*255)
        else:
            self.subtitulo_surface_copia.set_alpha((1-alfa)*255 + alfa*50)
        tela.blit(self.subtitulo_surface_copia, self.subtitulo_rect)
    
    def atualiza(self, delta):
        self.cronometro_subtitulo += delta
        if self.cronometro_subtitulo > self.tempo_de_animacao_subtitulo:
            self.cronometro_subtitulo = 0
            
    def processa_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self.gerenciador.va_para(TelaDeJogo())
    
class GerenciadorDeTelas:
    def __init__(self, jogo):
        self.jogo = jogo
        self.va_para(TelaInicial())
        
        
    def va_para(self, tela):
        self.tela_atual = tela
        self.tela_atual.gerenciador = self
        self.tela_atual.plano_de_fundo = self.jogo.tela.copy()
        
    
# classe principal ------------------------------------------------------------
class Jogo:
    def __init__(self):
        # cria tela, coloca título e cria relogio
        self.tela = pygame.display.set_mode((LARGURA_DA_TELA, ALTURA_DA_TELA),pygame.DOUBLEBUF)
        pygame.display.set_caption("Copia do Pong")
        self.relogio = pygame.time.Clock()
        
        # gerenciador de telas
        self.g = GerenciadorDeTelas(self)
    
    def main(self):
        # laço principal do jogo
        self.rodando = 1
        while self.rodando:
            # limita o FPS conta o tempo desde um último frame
            delta = self.relogio.tick(FPS)/1000
            
            # processa eventos do mouse e do teclado
            for evento in pygame.event.get():
                # fecha se usuario clicar no x
                if evento.type == pygame.QUIT:
                    self.rodando = 0
                
                self.g.tela_atual.processa_eventos(evento)
            
            # atualiza mundo do jogo
            self.g.tela_atual.atualiza(delta)
            
            # desenha alguma coisa
            self.tela.fill(PRETO)
            
            self.g.tela_atual.desenha(self.tela)
            
            # atualiza a janela
            pygame.display.update()
        
        # encerra o jogo
        pygame.quit()

if __name__ == "__main__":
    Jogo().main()   
