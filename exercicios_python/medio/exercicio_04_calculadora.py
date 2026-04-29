# ============================================================
# EXERCÍCIO 04 — NÍVEL MÉDIO
# ============================================================
# Arquivo: medio/exercicio_04_calculadora.py
#
# 📚 O que você vai aprender/praticar:
#   - Funções avançadas (*args, **kwargs)
#   - Módulo math (sqrt, pow, etc.)
#   - Tratamento de exceções múltiplas
#   - Listas e dicionários dinâmicos
#
# 🎯 Título: Calculadora Científica Avançada
#
# 📝 Enunciado:
#   Crie uma calculadora científica com funções avançadas.
#   O programa deve:
#   1. Ter função calculadora(*args, operacao='soma'): soma, multiplica ou potência
#   2. Função raiz_quadrada(numero): usando math.sqrt()
#   3. Menu com: 1-Básica(*args), 2-Raiz, 3-Potência, 0-Sair
#   4. Tratar ZeroDivisionError, ValueError e TypeError
#   5. Registrar histórico de 10 últimas operações em lista
#
# 💡 Dica:
#   *args permite números variáveis! Use dict para mapear operações.
#
# 📥 Exemplo de entrada e saída esperada:
#   1-Básica 2-Raiz 3-Potência 0-Sair
#   Opção: 1
#   Operação (soma/mult/pot): soma
#   Números: 10 20 5
#   Resultado: 35.0
#   Histórico: ['soma(10,20,5)=35.0']
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================