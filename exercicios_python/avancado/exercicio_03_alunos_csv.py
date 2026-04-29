# ============================================================
# EXERCÍCIO 03 — NÍVEL AVANÇADO
# ============================================================
# Arquivo: avancado/exercicio_03_alunos_csv.py
#
# 📚 O que você vai aprender/praticar:
#   - Módulo csv
#   - Classes com @property e @setter
#   - List comprehension avançada
#   - Decoradores personalizados
#
# 🎯 Título: Gerenciador de Alunos com CSV
#
# 📝 Enunciado:
#   Crie um sistema de gerenciamento de alunos com persistência CSV.
#   Deve ter:
#   1. Classe Aluno com @property para nome, notas[], media (calculada)
#   2. Decorador @valida_nota para validar notas 0-10
#   3. GerenciadorAlunos: carregar/salvar CSV, adicionar_aluno, top_3_melhor_media
#   4. CSV formato: nome,nota1,nota2,nota3
#   5. Menu para CRUD completo de alunos
#
# 💡 Dica:
#   csv.DictReader/Writer. @property calcula média automaticamente!
#
# 📥 Exemplo de entrada e saída esperada:
#   Alunos.csv:
#   nome,n1,n2,n3
#   Ana,8,9,7
#   João,6,5,7
#   
#   Top 3: Ana (8.0), João (6.0)
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================