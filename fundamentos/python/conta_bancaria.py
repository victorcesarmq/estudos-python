import json
import pandas
import datetime as dt

transacoes = [] # {"Id":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
saldo = 0 #variavel global



def depositar(valor): # depositar valor
    global saldo
    print(f"Depositou: R${valor}")
    saldo += valor
    transacoes.append({"Id": len(transacoes) + 1, "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Valor": valor, "Operacao": "Deposito"})
    return saldo

def sacar(valor): # sacar valor
    global saldo
    print(f"Sacou: R${valor}")
    if valor > saldo:
        print("Error: Saldo Indisponivel, operacao nao realizada")
        return valor
    saldo -= valor
    transacoes.append({"Id": len(transacoes) + 1, "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Valor": valor, "Operacao": "Saque"})
    return saldo

def exibir_extrato(): # extrato
    print(f"Saldo: R${saldo}\n {transacoes}")

print("MENU")
print("1. Sacar \n2. Depositar \n3. Extrato \n4. Sair")
while True:
    try:
        opcao = int(input("Escolha uma operacao: "))
        if opcao == 1:
            valor = int(input(f"Quanto desejar sacar: R$"))
            sacar(valor)
        elif opcao == 2:
            valor = int(input(f"Quanto deseja depositar : R$"))
            depositar(valor)
        elif opcao == 3:
            exibir_extrato()
        elif opcao == 4: break
    except ValueError:
        print("Digite uma opcao valida!")
