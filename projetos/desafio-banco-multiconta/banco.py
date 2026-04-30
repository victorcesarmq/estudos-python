from pathlib import Path
import json
import datetime as dt
from conta import *

arquivo = Path("historico.json")

class Banco:
    def __init__(self):
        self.pessoa = {}


    def cadastrar_conta(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        nova_conta = Conta(nome, cpf) # cria um objeto Conta passando nome e cpf
        self.pessoa[cpf] = nova_conta  # guarda a conta no dicionário
