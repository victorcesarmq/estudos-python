# ============================================================
# EXERCÍCIO 05 — NÍVEL MÉDIO
# ============================================================
# Arquivo: medio/exercicio_05_todo.py
#
# 📚 O que você vai aprender/praticar:
#   - Listas avançadas (slice, sort, remove)
#   - Dicionários com listas
#   - Módulo datetime
#   - Persistência em arquivo JSON
#
# 🎯 Título: Gerenciador de Tarefas TODO
#
# 📝 Enunciado:
#   Crie um gerenciador de tarefas TODO completo.
#   O programa deve:
#   1. Funções: adicionar(tarefa), listar(), marcar_concluida(indice), excluir(indice)
#   2. Cada tarefa tem: id, descrição, concluida (bool), data_criacao
#   3. Salvar/carregar tarefas do arquivo "todo.json"
#   4. Menu: 1-Adicionar, 2-Listar, 3-Concluir, 4-Excluir, 5-Sair
#   5. Mostrar tarefas pendentes e concluídas separadamente
#
# 💡 Dica:
#   Use lista de dicts. json.dump/load para persistência!
#
# 📥 Exemplo de entrada e saída esperada:
#   1-Adicionar 2-Listar 3-Concluir 4-Excluir 5-Sair
#   Opção: 1
#   Tarefa: Comprar leite
#   Adicionada! ID: 1
#   Opção: 2
#   [1] Comprar leite [PENDENTE]
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================