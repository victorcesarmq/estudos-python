
# ============================================================
# GABARITO COMPLETO — TODOS OS EXERCÍCIOS
# ============================================================
# ⚠️  Tente resolver cada exercício antes de consultar!
# Cada solução está dentro de uma função nomeada:
#   solucao_facil_01(), solucao_medio_01(), solucao_avancado_01()
# ============================================================

import math
import random
import json
import csv
import os
from abc import ABC, abstractmethod
from datetime import datetime
import time
from collections import defaultdict, Counter
from functools import wraps

# ────────────────────────────────────────
# FÁCIL — Exercício 01: Calculadora de IMC
# ────────────────────────────────────────
def solucao_facil_01():
    """Calcula IMC e classifica categoria de peso"""
    peso = float(input("Digite seu peso (kg): "))
    altura = float(input("Digite sua altura (m): "))
    imc = peso / (altura ** 2)
    
    if imc < 18.5:
        categoria = "Abaixo do peso"
    elif imc < 25:
        categoria = "Peso normal"
    elif imc < 30:
        categoria = "Sobrepeso"
    elif imc < 35:
        categoria = "Obesidade grau I"
    elif imc < 40:
        categoria = "Obesidade grau II"
    else:
        categoria = "Obesidade grau III"
    
    print(f"Seu IMC é {imc:.2f} - {categoria}")

# ────────────────────────────────────────
# FÁCIL — Exercício 02: Verificador de Pares/Ímpares
# ────────────────────────────────────────
def solucao_facil_02():
    """Conta números pares e ímpares até 0"""
    pares = 0
    impares = 0
    
    while True:
        num = int(input("Digite um número (0 para sair): "))
        if num == 0:
            break
        if num % 2 == 0:
            pares += 1
            print(f"{num} é PAR")
        else:
            impares += 1
            print(f"{num} é ÍMPAR")
    
    print(f"Você digitou {pares} pares e {impares} ímpares")

# ────────────────────────────────────────
# FÁCIL — Exercício 03: Calculadora de Média Escolar
# ────────────────────────────────────────
def solucao_facil_03():
    """Calcula média e conceito de notas"""
    qtd = int(input("Quantas notas? "))
    notas = []
    
    for i in range(qtd):
        nota = float(input(f"Nota {i+1}: "))
        notas.append(nota)
    
    media = sum(notas) / len(notas)
    
    if media >= 9.0:
        conceito = "A - Excelente!"
    elif media >= 7.0:
        conceito = "B - Bom!"
    elif media >= 5.0:
        conceito = "C - Regular"
    else:
        conceito = "D - Reprovado!"
    
    print(f"Notas: {notas}")
    print(f"Média: {media:.2f}")
    print(f"Conceito: {conceito}")

# ────────────────────────────────────────
# FÁCIL — Exercício 04: Lista de Compras Supermercado
# ────────────────────────────────────────
def solucao_facil_04():
    """Gerencia lista de compras com total"""
    compras = []
    total = 0
    
    while True:
        item = input("Item (FIM para sair): ").strip().title()
        if item == "FIM":
            break
        preco = float(input("Preço: "))
        compras.append(f"{item}: R$ {preco:.2f}")
        total += preco
    
    print("\n--- Sua Lista de Compras ---")
    for compra in compras:
        print(compra)
    print("-" * 30)
    print(f"Total de itens: {len(compras)}")
    print(f"Valor total: R$ {total:.2f}")

# ────────────────────────────────────────
# FÁCIL — Exercício 05: Menu Matemático
# ────────────────────────────────────────
def solucao_facil_05():
    """Menu interativo de operações matemáticas"""
    print("=== MENU MATEMÁTICO ===")
    
    while True:
        print("1 - Soma\n2 - Subtração\n3 - Multiplicação\n4 - Divisão\n0 - Sair")
        opcao = input("Escolha: ")
        
        if opcao == "0":
            print("Tchau!")
            break
        
        try:
            n1 = float(input("Número 1: "))
            n2 = float(input("Número 2: "))
            
            if opcao == "1":
                print(f"Resultado: {n1} + {n2} = {n1 + n2}")
            elif opcao == "2":
                print(f"Resultado: {n1} - {n2} = {n1 - n2}")
            elif opcao == "3":
                print(f"Resultado: {n1} * {n2} = {n1 * n2}")
            elif opcao == "4":
                if n2 == 0:
                    print("Erro: Divisão por zero!")
                else:
                    print(f"Resultado: {n1} / {n2} = {n1 / n2}")
            else:
                print("Opção inválida!")
        except ValueError:
            print("Digite números válidos!")

# ────────────────────────────────────────
# MÉDIO — Exercício 01: Conta Bancária
# ────────────────────────────────────────
def solucao_medio_01():
    """Sistema bancário com funções e histórico"""
    saldo = 0
    transacoes = []
    
    def depositar(valor):
        nonlocal saldo
        saldo += valor
        transacoes.append(f"Depósito: +R$ {valor:.2f}")
        print(f"Depósito realizado! Saldo: R$ {saldo:.2f}")
    
    def sacar(valor):
        nonlocal saldo
        if saldo >= valor:
            saldo -= valor
            transacoes.append(f"Saque: -R$ {valor:.2f}")
            print(f"Saque realizado! Saldo: R$ {saldo:.2f}")
        else:
            print("Saldo insuficiente!")
    
    def exibir_extrato():
        print(f"Saldo: R$ {saldo:.2f}")
        print("Histórico:")
        for t in transacoes[-5:]:  # últimas 5
            print(f"  {t}")
    
    while True:
        print("\n1-Depositar 2-Sacar 3-Extrato 0-Sair")
        op = input("Opção: ")
        if op == "0": break
        elif op == "1":
            try: depositar(float(input("Valor: ")))
            except: print("Valor inválido!")
        elif op == "2":
            try: sacar(float(input("Valor: ")))
            except: print("Valor inválido!")
        elif op == "3":
            exibir_extrato()

# ────────────────────────────────────────
# MÉDIO — Exercício 02: Boletim com Dicionário
# ────────────────────────────────────────
def solucao_medio_02():
    """Boletim escolar com relatório em arquivo"""
    boletim = {}
    
    def adicionar_disciplina(materia, nota):
        boletim[materia.title()] = nota
    
    def gerar_relatorio():
        if not boletim:
            print("Nenhuma disciplina cadastrada!")
            return
        
        medias = [nota for nota in boletim.values()]
        media_geral = sum(medias) / len(medias)
        
        situacao = "Aprovado" if media_geral >= 7 else "Recuperação" if media_geral >= 5 else "Reprovado"
        
        with open("boletim.txt", "w", encoding="utf-8") as f:
            f.write("BOLETIM ESCOLAR\n")
            f.write("=" * 30 + "\n")
            for materia, nota in sorted(boletim.items()):
                conc = "Aprovado" if nota >= 7 else "Recuperação" if nota >= 5 else "Reprovado"
                f.write(f"{materia}: {nota:.1f} ({conc})\n")
            f.write(f"Média: {media_geral:.2f} ({situacao})\n")
        
        print("Relatório salvo em boletim.txt")
    
    while True:
        materia = input("Adicionar disciplina (nome): ").strip()
        if not materia: break
        nota = float(input("Nota: "))
        adicionar_disciplina(materia, nota)
    
    gerar_relatorio()

# ────────────────────────────────────────
# MÉDIO — Exercício 03: Contador de Palavras
# ────────────────────────────────────────
def solucao_medio_03():
    """Conta frequência de palavras em arquivo"""
    try:
        with open("texto.txt", "r", encoding="utf-8") as f:
            texto = f.read().lower()
    except FileNotFoundError:
        # Cria arquivo exemplo
        texto = "Python é ótimo. Python tem muitas bibliotecas. Gosto de Python!"
        with open("texto.txt", "w", encoding="utf-8") as f:
            f.write(texto)
        print("Arquivo texto.txt criado com exemplo!")
    
    # Limpa texto
    for p in ".,!?;:-_":
        texto = texto.replace(p, " ")
    palavras = texto.split()
    
    contador = {}
    for palavra in palavras:
        palavra = palavra.strip()
        if palavra:
            contador[palavra] = contador.get(palavra, 0) + 1
    
    # Top 5
    top = sorted(contador.items(), key=lambda x: x[1], reverse=True)[:5]
    
    with open("relatorio_palavras.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE PALAVRAS\n")
        f.write("=" * 30 + "\n")
        for i, (palavra, count) in enumerate(top, 1):
            f.write(f"{i}. {palavra} ({count})\n")
    
    print("Análise salva em relatorio_palavras.txt")
    print("Top palavras:", top)

# ────────────────────────────────────────
# MÉD