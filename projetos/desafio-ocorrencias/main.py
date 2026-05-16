from ocorrencia import *
ocorrencia = Ocorrencia()
while True:
    print("Ocorrencias")
    print("1. Cadastrar Ocorrencia")
    print("2. Registro de Ocorrencia")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        ocorrencia.definir_local()
        ocorrencia.definir_data()
