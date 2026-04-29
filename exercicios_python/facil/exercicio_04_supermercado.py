# ============================================================
# EXERCÍCIO 04 — NÍVEL FÁCIL
# ============================================================
# Arquivo: facil/exercicio_04_supermercado.py
#
# 📚 O que você vai aprender/praticar:
#   - Strings (upper, lower, len, format)
#   - Listas (append, sum)
#   - Laços for
#   - Formatação com f-strings
#
# 🎯 Título: Lista de Compras do Supermercado
#
# 📝 Enunciado:
#   Crie um programa para gerenciar uma lista de compras no supermercado.
#   O programa deve:
#   1. Permitir adicionar itens com preço até o usuário digitar "FIM"
#   2. Armazenar cada item em uma lista no formato "Produto: preço"
#   3. Mostrar a lista completa formatada
#   4. Calcular e mostrar o valor total da compra
#   5. Mostrar quantos itens foram comprados
#
# 💡 Dica:
#   Use input() em loop while e lista.append(). Converta preços para float!
#
# 📥 Exemplo de entrada e saída esperada:
#   Entrada:
#   Item (FIM para sair): arroz
#   Preço: 12.50
#   Item (FIM para sair): feijão
#   Preço: 8.75
#   Item (FIM para sair): FIM
#   
#   Saída:
#   --- Sua Lista de Compras ---
#   Arroz: R$ 12.50
#   Feijão: R$ 8.75
#   -----------------------------
#   Total de itens: 2
#   Valor total: R$ 21.25
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================

carrinho = []

while True:

    item = input("Item (FIM para sair): ")
    if item == "FIM":
        break
    valor = float(input("Digite o valor do item: "))
    # ADICIONA ITEM E VALOR AO CARRINHO
    carrinho.append({
        "Item": item,
        "Valor": valor
    })
print("----------LISTA DE COMPRAS----------")
for produto in carrinho:
    print(f"{produto["Item"]}: R${produto["Valor"]}", end= "\n")
print("------------------------------------")

total_itens = len(carrinho)
print(f"Total de itens: {total_itens}")

valor_total = sum(item["Valor"] for item in carrinho)
print(f"Valor total: {valor_total:0.2f}")