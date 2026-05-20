from registro import *
from ocorrencia import *

ocorrencia_registro = Ocorrencia()
registro = Registro()

while True:
    print("Ocorrencias")
    print("1. Cadastrar Ocorrencia")
    print("2. Registro de Ocorrencia")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        ocorrencia_registro.definir_local()
        ocorrencia_registro.definir_data()
        ocorrencia_registro.definir_descricao()
        ocorrencia_registro.definir_status()
        ocorrencia_registro.definir_tipo()
        registro.adicionar(ocorrencia_registro)
        registro.salvar()
    if escolha == 2:
        registro.listar()