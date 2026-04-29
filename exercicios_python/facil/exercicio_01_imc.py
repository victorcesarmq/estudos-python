# ============================================================
# EXERCÍCIO 01 — NÍVEL FÁCIL
# ============================================================
# Arquivo: facil/exercicio_01_imc.py
#
# 📚 O que você vai aprender/praticar:
#   - Variáveis e tipos de dados (int, float)
#   - Entrada e saída (input, print, f-strings)
#   - Operadores aritméticos
#   - Condicionais (if, elif, else)
#
# 🎯 Título: Calculadora de IMC
#
# 📝 Enunciado:
#   Crie um programa que calcula o Índice de Massa Corporal (IMC) de uma pessoa.
#   O programa deve:
#   1. Pedir o peso (em kg) e a altura (em metros)
#   2. Calcular o IMC usando a fórmula: peso / (altura ** 2)
#   3. Classificar o IMC nas categorias:
#      - Abaixo de 18.5: "Abaixo do peso"
#      - 18.5 a 24.9: "Peso normal"
#      - 25 a 29.9: "Sobrepeso"
#      - 30 a 34.9: "Obesidade grau I"
#      - 35 a 39.9: "Obesidade grau II"
#      - Acima de 40: "Obesidade grau III"
#   4. Mostrar o resultado formatado: "Seu IMC é X.XX - [categoria]"
#
# 💡 Dica:
#   Use float() para converter as entradas e duas casas decimais no resultado com f"{imc:.2f}"
#
# 📥 Exemplo de entrada e saída esperada:
#   Entrada:
#   Digite seu peso (kg): 70
#   Digite sua altura (m): 1.75
#   
#   Saída:
#   Seu IMC é 22.86 - Peso normal
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================

peso = float(input("Digite o seu peso: "))
altura = float(input("Digite sua altura: "))
imc = peso / (altura ** 2)

if imc < 18.5:
    categoria = "Abaixo do peso"
elif imc >= 18.5 and imc <= 25:
    categoria = "Peso ideal"
elif imc >= 25 and imc <= 30:
    categoria = "Sobrepeso"
elif imc >= 30 and imc <= 40:
    categoria = "Obesidade grau I"
elif imc >= 40 and imc <= 50:
    categoria = "Obesidade grau II"
else:
    categoria = "Obesidade grau III"

print(f"Seu IMC é {imc:.2f} - [{categoria}]")