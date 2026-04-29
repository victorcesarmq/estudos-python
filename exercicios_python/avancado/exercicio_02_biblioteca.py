# ============================================================
# EXERCÍCIO 02 — NÍVEL AVANÇADO
# ============================================================
# Arquivo: avancado/exercicio_02_biblioteca.py
#
# 📚 O que você vai aprender/praticar:
#   - Herança (super(), override)
#   - Polimorfismo
#   - Métodos especiais (__str__, __len__)
#   - Classes abstratas (ABC)
#
# 🎯 Título: Sistema de Biblioteca com Herança
#
# 📝 Enunciado:
#   Crie um sistema de biblioteca com hierarquia de classes.
#   Deve ter:
#   1. Classe abstrata ItemBiblioteca (titulo, autor, ano, __str__)
#   2. Livro(ItemBiblioteca): isbn, paginas, emprestar/devolver
#   3. Revista(ItemBiblioteca): edicao, emprestar/devolver
#   4. Biblioteca: lista_itens, adicionar_item, buscar_por_autor
#   5. Implemente __len__ para contar itens disponíveis
#   6. Teste com menu interativo
#
# 💡 Dica:
#   Use @abstractmethod. Sobrescreva métodos da superclasse!
#
# 📥 Exemplo de entrada e saída esperada:
#   Livro: "Python Avançado", Autor: João Silva
#   Revista: "TechNews #45", Autor: Maria Santos
#   Total disponível: 2
#   Buscar por João: 1 resultado
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================