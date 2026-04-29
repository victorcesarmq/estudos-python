# ============================================================
# EXERCÍCIO 04 — NÍVEL AVANÇADO
# ============================================================
# Arquivo: avancado/exercicio_04_busca_binaria.py
#
# 📚 O que você vai aprender/praticar:
#   - Recursão com caso base
#   - Algoritmos (busca binária)
#   - Generators (yield)
#   - Listas ordenadas e slicing
#
# 🎯 Título: Busca Binária Recursiva Otimizada
#
# 📝 Enunciado:
#   Implemente busca binária recursiva com generator.
#   O programa deve:
#   1. Função busca_binaria(lista_ordenada, alvo) → yield índices encontrados
#   2. Caso recursivo: meio = (inicio + fim) // 2
#   3. Gerar números aleatórios ordenados para teste (1000 elementos)
#   4. Medir tempo de busca com time.perf_counter()
#   5. Comparar com busca linear simples
#   6. Menu para múltiplas buscas
#
# 💡 Dica:
#   Recursão: if inicio > fim return. Yield meio se encontrado!
#
# 📥 Exemplo de entrada e saída esperada:
#   Lista gerada: [1, 3, 5, ..., 999]
#   Buscar 500 → Encontrado no índice 250 (0.0001s)
#   Busca linear: 0.0012s (10x mais lento!)
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================