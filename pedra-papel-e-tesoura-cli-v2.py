#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importando bibliotecas nescessárias -----------------------------------------
import random
import os
import platform

sistema = platform.system() # Windows, Linux, etc

# arte ------------------------------------------------------------------------
artes = [[
"         _______  ",
"     ---'   ____) ",
"           (_____)",
"           (_____)",
"           (____) ",
"     ---.__(___)  "
],
[
"     _______      ",
"---'    ____)____ ",
"           ______)",
"          _______)",
"         _______) ",
"---.__________)   "
],
[
"    _______       ",
"---'   ____)____  ",
"          ______) ",
"       __________)",
"      (____)      ",
"---.__(___)       "
]]

# tavez seja mais prático acrescentar as artes já espelhadas
def espelha_arte(arte):
    saida = []
    for linha in arte:
        linha_espelhada = ""
        for c in linha:
            if c == '(':
                linha_espelhada = ')' + linha_espelhada
            elif c == ')':
                linha_espelhada = '(' + linha_espelhada
            else:
                linha_espelhada = c + linha_espelhada
        saida.append(linha_espelhada)
    return saida

artes_espelhadas = [espelha_arte(arte) for arte in artes]

# jogo ------------------------------------------------------------------------
def limpa_tela():
    if sistema == "Linux":
        os.system("clear")
    if sistema == "Windows":
        os.system("cls")

def recebe_escolha():
    print("[1] Pedra    [2] Papel    [3] Tesoura\n")
    while True:
        escolha = input("> ")
        if escolha in "123" and escolha != '':
            return int(escolha)
        if escolha.lower() == 'q':
            return 0
        else:
            print("Escolha inválida!")

def imprime_artes(escolha_do_jogador, escolha_do_computador):
    saida = ""
    for i in range(6):
        saida += artes[escolha_do_jogador-1][i]+"      "
        saida += artes_espelhadas[escolha_do_computador-1][i] + '\n'
    saida += '\n'
    return saida
        

def imprime_resultado(escolha_do_jogador, escolha_do_computador):
    global vitorias, empates, derrotas, total
    total += 1
    saida = ""
    if escolha_do_jogador == escolha_do_computador:
        saida += "Empate.\n"
        empates += 1
    elif (escolha_do_jogador == 1 and escolha_do_computador == 3): # pedra e tesoura
        saida += "Você venceu!\n"
        vitorias += 1
    elif (escolha_do_jogador == 2 and escolha_do_computador == 1): # papel e pedra
        saida += "Você venceu!\n"
        vitorias += 1
    elif (escolha_do_jogador == 3 and escolha_do_computador == 2): # tesoura e papel
        saida += "Você venceu!\n"
        vitorias += 1
    else:
        saida += "Você perdeu.\n"
        derrotas += 1
    return saida

def imprime_estatisticas():
    return "Vitórias: {}    Derrotas: {}    Empates: {}\n".format(vitorias, derrotas, empates)
    #print("Vitórias: {}%    Derrotas: {}%    Empates: {}%".format(int(vitorias/total*100), int(derrotas/total*100), int(empates/total*100)))


# inicia estatísticas
vitorias = 0
derrotas = 0
empates = 0
total = 0

# inicia painel
painel = 9*'\n'

# função principal
def main():
    global painel
    # inicia o jogo
    while True:
        # limpa a tela
        limpa_tela()
        # imprime título do jogo e painel
        print("#-------- Pedra, Papel e Tesoura --------#\n")
        print(painel)
        
        # imprime opções e recebe escolha do jogador
        escolha_do_jogador = recebe_escolha()
        
        # fecha o jogo se o jogador digitar 'q'
        if escolha_do_jogador == 0:
            break
        
        # gera a escolha do computador
        escolha_do_computador = random.choice([1, 2, 3])
        
        # acrescenta as artes das escolhas no painel
        painel = imprime_artes(escolha_do_jogador, escolha_do_computador)
        
        # acrescenta o resultado no painel
        painel += imprime_resultado(escolha_do_jogador, escolha_do_computador)
        
        # acrescenta as estatísticas no painel
        painel += imprime_estatisticas()
        
        # imprime painel
        limpa_tela()
        print(painel)

if __name__ == "__main__":
    main()
