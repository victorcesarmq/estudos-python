import datetime as dt

transacoes = [] # {"Id":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
saldo = 0 #variavel global



def depositar(valor): # depositar valor
    global saldo
    if valor <= 0:
        print("Valor Invalido")
    else:
        print("-" * 30)
        print(f"Operacao finalizada com sucesso!\nDeposito realizado no valor de: R${valor}")
        print("-" * 30)
        saldo += valor
        transacoes.append({"Id": len(transacoes) + 1, "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Valor": valor, "Operacao": "Deposito"})
    return saldo

def sacar(valor): # sacar valor
    global saldo

    if valor > saldo:
        print("Error: Saldo Indisponivel, operacao nao realizada")
        return valor
    elif valor <= 0:
        print("Valor Invalido")
    else:

        saldo -= valor
        print("-" * 30)
        print(f"Operacao finalizada com sucesso!\nSaque realizado no valor de: R${valor}")
        print("-" * 30)

        transacoes.append({"Id": len(transacoes) + 1, "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Valor": valor, "Operacao": "Saque"})
    return saldo

def exibir_extrato(): # extrato
    for i in transacoes:
        print("-" * 20)
        print(f"Id:{i['Id']} \nData da transacao: {i['Data']} \nValor: R${i['Valor']:0.2f} \nOperacao realizada: {i['Operacao']}")
        print("-" * 20)
    print(f"Saldo: R${saldo:0.2f}")


print("MENU")
print("1. Sacar \n2. Depositar \n3. Extrato \n0. Sair")
while True:
    try:
        opcao = int(input("Escolha uma operacao (0 para sair): "))
        if opcao == 1:
            valor = float(input(f"Quanto desejar sacar: R$"))

            sacar(valor)
        elif opcao == 2:
            valor = float(input(f"Quanto deseja depositar : R$"))
            depositar(valor)
        elif opcao == 3:
            exibir_extrato()
        elif opcao == 0: break
    except ValueError:
        print("Erro: valor invalido")
