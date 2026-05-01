from pathlib import Path
import json
import datetime as dt



class Conta:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.limite = 500
        arquivo = Path(f"{self.cpf}.json")
        if arquivo.exists() and arquivo.stat().st_size > 0:
            with open(arquivo, "r", encoding="utf-8") as f:
             dados = json.load(f)
             self.saldo = dados["saldo"]
             self.historico = dados["historico"] # {"Id-transacao":, "Data":, "Valor":, "Operacao":} estrutura de dicionario
        else:
            self.saldo = 0  # Saldo disponivel da conta
            self.historico = []


    def depositar(self, valor):
        if valor <= 0:
            print("Erro: Valor deve ser positivo")
            return
        self.saldo += valor
        print("Deposito realizado com sucesso!")
        self.historico.append({"Id-transacao": len(self.historico) + 1,
                               "Valor": valor,
                               "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                               "Operacao": "Deposito"
                             })
        with open(f"{self.cpf}.json", "w", encoding="utf-8") as f:
            dados = {
                "CPF": self.cpf,
                "Nome": self.nome,
                "saldo": self.saldo,
                "historico": self.historico
            }
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def saque(self, valor):
        if valor > self.saldo:
            print("Erro: voce ta quebrado pai")
            return
        elif valor > self.limite:
            print("Erro: limite de saque atingido")
            return
        self.saldo -= valor
        print("Saque realizado com sucesso!")
        self.historico.append({"Id-transacao": len(self.historico) + 1,
                                   "Valor": valor,
                                   "Data": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   "Operacao": "Saque"
                             })
        with open(f"{self.cpf}.json", "w", encoding="utf-8") as f:
            dados = {
                "CPF": self.cpf,
                "Nome": self.nome,
                "saldo": self.saldo,
                "historico": self.historico
            }
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def extrato_da_conta(self):
        if len(self.historico) == 0:
            print("Conta nao possui movimentacoes")
            return
        for i in self.historico:
            print("-" * 35)
            print(f"Id da transacao: {i['Id-transacao']} \n"
                  f"Valor: R${i['Valor']} \n"
                  f"Data: {i['Data']} \n"
                  f"Operacao Realizada: {i['Operacao']}")
            print("-" * 35)

    def limite_da_conta(self, valor):
        self.limite = valor
        print("Limite da conta ATUALIZADO com sucesso!")

    def limite_excedido(self, valor):
        if  valor > self.limite:
            print("Erro: Limite de transferencia excedido")
            return