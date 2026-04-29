# ============================================================
# EXERCÍCIO 03 — NÍVEL MÉDIO
# ============================================================
# Arquivo: medio/exercicio_03_contador_palavras.py
#
# 📚 O que você vai aprender/praticar:
#   - Leitura/escrita de arquivos .txt
#   - Strings avançadas (split, strip, lower)
#   - Dicionários para contagem
#   - Módulo collections (Counter opcional)
#
# 🎯 Título: Contador de Palavras em Arquivo
#
# 📝 Enunciado:
#   Crie um programa que analisa a frequência de palavras em um arquivo de texto.
#   O programa deve:
#   1. Ler um arquivo "texto.txt" (crie um exemplo se não existir)
#   2. Contar quantas vezes cada palavra aparece (ignore maiúsculas/minúsculas)
#   3. Remover pontuação e quebras de linha
#   4. Mostrar as 5 palavras mais frequentes
#   5. Salvar relatório em "relatorio_palavras.txt"
#   6. Tratar erro se arquivo não existir
#
# 💡 Dica:
#   Use .split() após .lower().replace() para limpar texto!
#
# 📥 Exemplo de entrada e saída esperada:
#   texto.txt:
#   Python é ótimo. Python tem muitas bibliotecas. Gosto de Python!
#   
#   Saída:
#   Palavras mais frequentes:
#   1. python (3)
#   2. é (1)
#   3. ótimo (1)
#   ...
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================