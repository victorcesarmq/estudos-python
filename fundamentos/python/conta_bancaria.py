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

depositar(100)
sacar(100)
exibir_extrato()