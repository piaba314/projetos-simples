#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importando bibliotecas nescessárias -----------------------------------------
import random
import os
import platform

# carregando lista de palavras ------------------------------------------------
with open("lista-de-palavras.txt") as arquivo:
    lista_de_palavras = arquivo.read().split('\n')

# arte ------------------------------------------------------------------------
artes = [
[
"  +---+",
"  |   |",
"      |",
"      |",
"      |",
"      |",
"========="],
[
"  +---+",
"  |   |",
"  O   |",
"      |",
"      |",
"      |",
"========="],
[
"  +---+",
"  |   |",
"  O   |",
" /    |",
"      |",
"      |",
"========="], 
[
"  +---+",
"  |   |",
"  O   |",
" /|   |",
"      |",
"      |",
"========="], 
[
"  +---+",
"  |   |",
"  O   |",
" /|\\  |",
"      |",
"      |",
"========="],
[
"  +---+",
"  |   |",
"  O   |",
" /|\\  |",
" /    |",
"      |",
"========="],
[
"  +---+",
"  |   |",
"  O   |",
" /|\\  |",
" / \\  |",
"      |",
"========="]]

# centraliza artes
for arte in artes:
    for i, linha in enumerate(arte):
        arte[i] = linha.center(37, ' ')

# jogo ------------------------------------------------------------------------
sistema = platform.system()

def limpa_tela():
    if sistema == "Linux":
        os.system("clear")
    if sistema == "Windows":
        os.system("cls")

def imprime_arte():
    for linha in artes[tentativas_erradas]:
        print(linha)

def imprime_palavra(palavra, letras_reveladas):
    saida = ""
    for i, letra in enumerate(palavra):
        if letras_reveladas[i]:
            saida += letra + ' '
        else:
            saida += '- '
    print(saida.center(37, ' '))

def imprime_letras_disponiveis():
    print("\nLetras disponíveis: ")
    for i in range(26):
        if letras_disponiveis[i]:
            print(alfabeto[i], end='')
    print('\n')

def recebe_jogada():
    while True:
        c = input("Digite uma letra: ").upper()
        if len(c) == 1 and c in alfabeto:
            if letras_disponiveis[alfabeto.index(c)]:
                return c
            else:
                print("Letra já tentada!")
        else:
            print("Tentativa inválida!")

def faz_jogada(letra, palavra, letras_reveladas):
    global tentativas_erradas
    if letra in palavra:
        for i, l in enumerate(palavra):
            if letra == l:
                 letras_reveladas[i] = 1
    else:
        tentativas_erradas += 1
        
    letras_disponiveis[alfabeto.index(letra)] = 0

def verifica_vitoria(letras_reveladas):
    for v in letras_reveladas:
        if v == 0:
            return False
    return True

# inicia variáveis globais
tentativas_erradas = 0
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letras_disponiveis = 26*[1]

# função principal
def main():
    global tentativas_erradas, letras_disponiveis
    while True:
        # escolhe uma palavra aleatória da lista e cria painel
        palavra = random.choice(lista_de_palavras)
        letras_reveladas = len(palavra)*[0] # 0: não, 1: sim
        
        while True:
            # limpa a tela
            limpa_tela()
            
            # imprime cabeçalho e imagem (que depende do número de tentativas erradas)
            print("#---------- Jogo da Forca ----------#\n")
            imprime_arte()
            
            # imprime palavra
            imprime_palavra(palavra, letras_reveladas)
            
            # imprime letras ainda não tentadas
            imprime_letras_disponiveis()
            
            # recebe jogada
            letra = recebe_jogada()
            
            # faz jogada
            faz_jogada(letra, palavra, letras_reveladas)
            
            # verifica se o jogador venceu
            if verifica_vitoria(letras_reveladas):
                print("Parabéns, você venceu!")
                print("A palavra é {}.\n".format(palavra))
                break
            
            # verifica derrota
            if tentativas_erradas == 6:
                print("Que pena. Você perdeu.")
                print("A palavra é {}.\n".format(palavra))
                break
        
        # pergunta se o jogador quer jogar de novo
        print("Pressione q para sair e qualquer outra\ntecla para jogar de novo.")
        resp = input("> ")
        if resp == 'q':
            break
        
        # reinicia número de tentativas erradas, letras disponíveis
        tentativas_erradas = 0
        letras_disponiveis = 26*[1]
        
        
if __name__ == "__main__":
    main()
