import json
from pathlib import Path

class Conta:
    def __init__(self,titular):
        self.extrato = [] # {"Id-transacao":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
        self.numero = numero # numero da conta
        self.saldo = saldo # Saldo disponivel da conta
        self.limite = limite
        self.titular = []# {"CPF":} estrutura de dicionario



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



    def extrato(self):
        self.saldo

    def limite_da_conta(self, valor):
        if  valor > self.limite:
            print("Erro: Limite de transferencia excedido")
            return
        else:
            print("Transferencia em cont")

    def cadastrar(self):
        self.titular = input("Informe o CPF do titular: ")
        self.nome = input("Informe o nome do titular: ")



class ContaPoupanca:
    def __init__(self):
        super().__init__(titular)

conta = Conta()

print("MENU")
print("1. Sacar \n2. Depositar \n3. Extrato \n0. Sair")
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




