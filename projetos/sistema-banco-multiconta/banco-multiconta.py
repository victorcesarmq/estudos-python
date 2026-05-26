
from banco import *
from conta import *

banco = Banco()

while True:
    print("-" * 20)
    print("MENU DE CONTA")
    print("-" * 20)
    print("1 - Cadastrar conta")
    print("2 - Acessar conta")
    print("3 - Sair")
    print("-" * 20)
    escolha = int(input("Escolha: "))
    if escolha == 3: break

    elif escolha == 1:
        banco.cadastrar_conta()

    elif escolha == 2:
        if len(banco.pessoa) == 0:
            print("Nenhuma conta cadastrada.")
        else:
            try:
                print("Contas Disponiveis")
                print("=" * 20)
                for cpf in banco.pessoa:
                    print(cpf)
                print("=" * 20)
                cpf = input("Digite o cpf: ")
                if cpf in banco.pessoa:
                    while True:
                        conta = banco.pessoa[cpf]
                        print("=" * 20)
                        print(f"Conta Atual: {cpf}\n",
                              f"Saldo: {conta.saldo}")
                        print("=" * 20)
                        print("1 - Depositar")
                        print("2 - Saque")
                        print("3 - Extrato")
                        print("4 - Transferencia")
                        print("5 - Sair")
                        print("=" * 20)
                        escolha = int(input("Escolha: "))
                        if escolha == 1:
                            conta.depositar(valor=float(input("Valor do deposito: ")))
                        elif escolha == 2:
                            conta.saque(valor=float(input("Valor do saque: ")))
                        elif escolha == 3:
                            conta.extrato_da_conta()
                        elif escolha == 4:
                            cpf_destino = input("CPF destino: ")
                            if cpf_destino in banco.pessoa:
                                conta.transferir(banco.pessoa[cpf_destino], float(input("Valor: ")))
                            else:
                                print("Conta destino não encontrada")
                        elif escolha == 5: break
            except ValueError:
                print("Valor invalido")