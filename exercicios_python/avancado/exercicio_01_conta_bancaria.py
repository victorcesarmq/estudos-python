# ============================================================
# EXERCÍCIO 01 — NÍVEL AVANÇADO
# ============================================================
# Arquivo: avancado/exercicio_01_conta_bancaria.py
#
# 📚 O que você vai aprender/praticar:
#   - Classes e objetos (__init__, self)
#   - Métodos de instância
#   - Encapsulamento (_privado)
#   - Tratamento de exceções customizadas
#
# 🎯 Título: Sistema Bancário com Classes
#
# 📝 Enunciado:
#   Crie uma classe ContaBancaria completa.
#   A classe deve ter:
#   1. __init__(self, numero, titular, saldo=0)
#   2. depositar(self, valor) → None
#   3. sacar(self, valor) → bool (raise SaldoInsuficienteError se não puder)
#   4. _atualizar_saldo(self) → privado
#   5. __str__() para exibir conta formatada
#   6. Programa principal com menu para testar múltiplas contas
#   7. Exception customizada SaldoInsuficienteError
#
# 💡 Dica:
#   Use assert ou raise em sacar(). Teste com 2 contas diferentes!
#
# 📥 Exemplo de entrada e saída esperada:
#   Conta 001 - João - R$ 0.00
#   1-Depositar 2-Sacar 3-Saldo 0-Sair
#   Depositar R$ 500 → Conta 001 - João - R$ 500.00
#
# ============================================================
# ✏️  ESCREVA SEU CÓDIGO ABAIXO DESTA LINHA
# ============================================================