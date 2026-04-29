import json
from pathlib import Path

class Conta:
    def __init__(self):
        self.historico = [] # {"Id-transacao":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
        self.saldo = saldo # Saldo disponivel da conta
        self.limite = limite


    def depositar(self, valor):
        if valor <= 0:
            print("Erro: Valor deve ser positivo")
            return


        self.saldo += valor

    def saque(self, valor):
        if valor > self.saldo:
            print("Erro: voce ta quebrado pai")
            return
        elif valor > self.limite:
            print("Erro: limite de saque atingido")
            return
        valor <= self.saldo
        self.saldo -= valor
        print("Saque realizado com sucesso!")



    def extrato_da_conta(self):
        self.saldo

    def limite_da_conta(self, valor):
        if  valor > self.limite:
            print("Erro: Limite de transferencia excedido")
            return
        else:
            print("Transferencia em cont")

conta = Conta()

print("MENU")
print("1. Sacar \n"
      "2. Depositar \n"
      "3. Extrato \n"
      "4. Cadastro de Usuario \n"
      "0. Sair")
while True:
    try:
        opcao = int(input("Escolha uma operacao (0 para sair): "))
        if opcao == 1:
            valor = float(input(f"Quanto desejar sacar: R$"))
            conta.saque(valor)
        elif opcao == 2:
            valor = float(input(f"Quanto deseja depositar : R$"))
            conta.depositar(valor)
        elif opcao == 0: break
    except ValueError:
        print("Erro: valor invalido")




