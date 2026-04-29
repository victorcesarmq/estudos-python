# ============================================================
# EXERCÍCIO 03 — NÍVEL FÁCIL
# ============================================================
# Arquivo: facil/exercicio_03_nota.py
#
# 📚 O que você vai aprender/praticar:
#   - Listas simples e indexação
#   - Laços for com range()
#   - Condicionais aninhados
#   - Operadores de comparação
#
# 🎯 Título: Calculadora de Média Escolar
#
# 📝 Enunciado:
#   Crie um programa para calcular a média de notas de um aluno.
#   O programa deve:
#   1. Pedir quantas notas serão cadastradas (entre 1 e 10)
#   2. Pedir cada nota (0 a 10)
#   3. Calcular a média aritmética
#   4. Classificar o desempenho:
#      - Média >= 9.0: "A - Excelente!"
#      - Média >= 7.0: "B - Bom!"
#      - Média >= 5.0: "C - Regular"
#      - Média < 5.0: "D - Reprovado!"
#   5. Mostrar todas as notas, a média e a classificação
#
# 💡 Dica:
#   Use uma lista para armazenar as notas e len() para contar quantas foram cadastradas
#
# 📥 Exemplo de entrada e saída esperada:
#   Entrada:
#   Quantas notas? 3
#   Nota 1: 8.5
#   Nota 2: 7.0
#   Nota 3: 9.0
#   
#   Saída:
#   Notas: [8.5, 7.0, 9.0]
#   Média: 8.17
#   Conceito: B - Bom!
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================
from statistics import quantiles


notas = []


while True:
    quantidade_notas = int(input("Digite a quantidade de notas? (0 para sair): "))
    if quantidade_notas == 0:
        break

    for i in range(quantidade_notas):
        nota = float(input(f"Digite a nota {1 + i}: "))
        notas.append(nota)

media = sum(notas) / len(notas)
if media < 5:
    print(f"Reprovado com {media} de média")
elif media >= 5 and media < 7:
    print("C - Regular")
elif media >= 7 and media < 9:
    print("B - Bom!")
elif media > 9:
    print("A - Excelente!!")

for i in notas:
    print(i, end=", ")
print("\n Média: ",media)