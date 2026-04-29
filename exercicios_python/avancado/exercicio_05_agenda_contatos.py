# ============================================================
# EXERCÍCIO 05 — NÍVEL AVANÇADO
# ============================================================
# Arquivo: avancado/exercicio_05_agenda_contatos.py
#
# 📚 O que você vai aprender/praticar:
#   - Decoradores (@classmethod, @staticmethod)
#   - Módulos json, collections (defaultdict)
#   - Algoritmos ordenação customizada
#   - Context managers (with statement)
#
# 🎯 Título: Agenda de Contatos Inteligente
#
# 📝 Enunciado:
#   Crie uma agenda de contatos avançada com JSON.
#   A classe Agenda deve ter:
#   1. @classmethod.from_json(classe, arquivo) → carrega contatos
#   2. @staticmethod.validar_email(email) → valida formato
#   3. adicionar_contato(nome, email, telefones=[])
#   4. buscar(nome_parcial) → retorna generator ordenado por nome
#   5. Context manager para auto-salvar: with Agenda('contatos.json'):
#   6. Ordenação customizada por frequência de uso
#
# 💡 Dica:
#   defaultdict(list) para telefones. Decore métodos de classe corretamente!
#
# 📥 Exemplo de entrada e saída esperada:
#   with Agenda('contatos.json') as agenda:
#     agenda.adicionar('Ana', 'ana@email.com', ['9999-9999'])
#   Buscar 'ana' → Ana (ana@email.com) [9999-9999]
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================