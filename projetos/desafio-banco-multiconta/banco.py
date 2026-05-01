from pathlib import Path
import json
import datetime as dt
from conta import *

class Banco:
    def __init__(self):
        banco_pessoas = Path(f"Banco.json")
        self.pessoa = {}
        if banco_pessoas.exists() and banco_pessoas.stat().st_size > 0:
            with open("Banco.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                for cpf, nome in dados.items():
                    self.pessoa[cpf] = Conta(nome, cpf)


    def cadastrar_conta(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        nova_conta = Conta(nome, cpf) # cria um objeto nova_conta passando nome e cpf pra classe Conta
        if cpf in self.pessoa:
            print("Ja existe uma conta cadastrada nesse CPF")
            return
        else:
            self.pessoa[cpf] = nova_conta  # guarda a conta no dicionário
            self.salvar() #salva a conta, preciso adicionar uma verificacao depois

    def salvar(self): #salva a conta no Banco.json
        dados = {}
        for cpf, conta in self.pessoa.items():
            dados[cpf] = conta.nome
        with open("Banco.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)