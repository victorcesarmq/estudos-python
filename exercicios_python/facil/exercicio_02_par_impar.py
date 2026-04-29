# ============================================================
# EXERCÍCIO 02 — NÍVEL FÁCIL
# ============================================================
# Arquivo: facil/exercicio_02_par_impar.py
#
# 📚 O que você vai aprender/praticar:
#   - Entrada e saída (input, print)
#   - Operadores aritméticos e módulo (%)
#   - Condicionais (if, else)
#   - Laços (while)
#
# 🎯 Título: Verificador de Números Pares/Ímpares
#
# 📝 Enunciado:
#   Crie um programa que verifica se números são pares ou ímpares.
#   O programa deve:
#   1. Continuar pedindo números até o usuário digitar 0
#   2. Para cada número, mostrar se é PAR ou ÍMPAR
#   3. Contar quantos pares e ímpares foram digitados
#   4. Ao final, mostrar o resumo: "Você digitou X pares e Y ímpares"
#
# 💡 Dica:
#   Use o operador % para verificar resto da divisão por 2. While com condição de parada!
#
# 📥 Exemplo de entrada e saída esperada:
#   Entrada:
#   Digite um número (0 para sair): 4
#   4 é PAR
#   Digite um número (0 para sair): 7
#   7 é ÍMPAR
#   Digite um número (0 para sair): 0
#   
#   Saída:
#   Você digitou 1 pares e 1 ímpares
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================
while True:
    numero = int(input("Digite um numero inteiro (0 para sair): "))
    if numero == 0:
        break
    elif numero % 2 == 0:
        print(f"O numero escolhido é par")
    else:
        print("O numero escolhido é impar")
