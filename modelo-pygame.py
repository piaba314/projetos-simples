#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importa bibliotecas nescessárias --------------------------------------------
import pygame
pygame.init()

# define algumas constantes ---------------------------------------------------
LARGURA_DA_TELA = 800
ALTURA_DA_TELA = 600
FPS = 60


# função principal ------------------------------------------------------------
def main():
    # cria tela, relogio, título, etc
    tela = pygame.display.set_mode((LARGURA_DA_TELA, ALTURA_DA_TELA))
    relogio = pygame.time.Clock()
    
    # laço principal
    rodando = True
    while rodando:
        # limita o número de FPS e obtem o tempo desde o último frame
        delta = relogio.tick(FPS)/1000
        
        # processa eventos do mouse e teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
        
        # atualiza o mundo do jogo
        
        
        #desenha alguma coisa
        
        
        # atualiza janela
        pygame.display.update()
    
    # encerra pygame
    pygame.quit()

if __name__ == "__main__":
    main()
