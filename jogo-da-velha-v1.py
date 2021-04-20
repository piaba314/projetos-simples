#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform

sistema = platform.system()

def limpa_tela():
    if sistema == "Linux":
        os.system("clear")
    if sistema == "Windows":
        os.system("cls")

tabuleiro = [['1', '2', '3'],
             ['4', '5', '6'],
             ['7', '8', '9']]

def desenha_tabuleiro():
    print("#----------Jogo da Velha----------#\n")
    print("           +---+---+---+             ")
    
    # percorre as linhas
    for i in range(3):
        print("           |", end="")
        # percorre os casas de cada linha
        for j in range(3):
            print(" {} |".format(tabuleiro[i][j]), end="")
        print()
        print("           +---+---+---+")
    
    print()


def pergunta_quem_comeca():
    while True:
        resp = input("Quem começa? (X/O) ").upper()
        if resp == 'X' or resp == 'O':
            return resp
        print("Resposta Inválida!")

def recebe_jogada(jogador_atual):
    while True:
        resp = input("Jogador {}: ".format(jogador_atual))
        if resp.isnumeric():
            resp = int(resp)
            if resp >= 1 and resp <= 9:
                i = (resp-1)//3
                j = (resp-1)%3
                if tabuleiro[i][j].isnumeric():
                    return (i, j)
        print("Jogada Inválida!")
        
def faz_jogada(jogada, jogador_atual):
    tabuleiro[jogada[0]][jogada[1]] = jogador_atual

def verifica_vitoria():
    # verifica linha
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2]:
            return True
    # verifica coluna
    for i in range(3):
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i]:
            return True
    # verifica diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2]:
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0]:
        return True
    
    return False

def verifica_empate():
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j].isnumeric():
                return False
    return True

def limpa_tabuleiro():
    global tabuleiro
    tabuleiro = [['1', '2', '3'],
                 ['4', '5', '6'],
                 ['7', '8', '9']]
        
def main():
    while True:
        # limpe o tabuleiro
        limpa_tabuleiro()
        # limpe a tela e desenhe o tabuleiro
        limpa_tela()
        desenha_tabuleiro()
        # pergunte quem começa (X/O)
        jogador_atual = pergunta_quem_comeca()
        # enquanto o jogo estiver rodando
        while True:
            # limpe a tela e desenhe o tabuleiro
            limpa_tela()
            desenha_tabuleiro()
            # receba a jogada do jogador atual
            jogada = recebe_jogada(jogador_atual)
            faz_jogada(jogada, jogador_atual)
            # se alguém venceu ou houve empate
            if verifica_vitoria() or verifica_empate():
                # encerre o jogo
                break
            # troque o jogador e repita
            if jogador_atual == 'X':
                jogador_atual = 'O'
            else:
                jogador_atual = 'X'
        # imprima o vencedor ou empate
        limpa_tela()
        desenha_tabuleiro()
        if verifica_empate():
            print("Empate!")
        else:
            print("Jogador {} venceu!".format(jogador_atual))
        # pergunta se o usuário quer jogar de novo
        resp = input("Jogar de novo? (s/n) ").lower()
        if resp != 's':
            break

if __name__ == "__main__":
    main()