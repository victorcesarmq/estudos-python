import datetime as dt

class conta:
    def __init__(self):
        self.transacoes = []  # {"Id":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
        self.saldo = 0  # variavel global

    def depositar(self, valor): # depositar valor
        if valor <= 0:
            print("Valor Invalido")
            return
        self.saldo += valor
        self.transacoes.append({"Id": len(self.transacoes) + 1,
                                "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                "Valor": valor,
                                "Operacao": "Deposito"
        })
        print("-" * 30)
        print(f"Operacao finalizada com sucesso!\nDeposito realizado no valor de: R${valor}")
        print("-" * 30)


    def sacar(self, valor): # sacar valor
        if valor <= 0:
            print("Valor Invalido")
            return
        elif valor > self.saldo:
            print("Error: Saldo Indisponivel, operacao nao realizada")
            return
        self.saldo -= valor

        self.transacoes.append({"Id": len(self.transacoes) + 1,
                           "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                           "Valor": valor,
                           "Operacao": "Saque"
        })
        print("-" * 30)
        print(f"Operacao finalizada com sucesso!\nSaque realizado no valor de: R${valor}")
        print("-" * 30)

    def exibir_extrato(self): # extrato
        for i in self.transacoes:
            print("-" * 20)
            print(f"Id:{i['Id']} \nData da transacao: {i['Data']} \nValor: R${i['Valor']:0.2f} \nOperacao realizada: {i['Operacao']}")
            print("-" * 20)
        print(f"Saldo: R${self.saldo:0.2f}")

conta = conta()
print("MENU")
print("1. Sacar \n2. Depositar \n3. Extrato \n0. Sair")
while True:
    try:
        opcao = int(input("Escolha uma operacao (0 para sair): "))
        if opcao == 1:
            valor = float(input(f"Quanto desejar sacar: R$"))
            conta.sacar(valor)
        elif opcao == 2:
            valor = float(input(f"Quanto deseja depositar : R$"))
            conta.depositar(valor)
        elif opcao == 3:
            conta.exibir_extrato()
        elif opcao == 0: break
    except ValueError:
        print("Erro: valor invalido")
