import datetime as dt
import json
import os

class Ocorrencia():
    def __init__(self):
        self.locais_validos = ["Cuiaba", "Varzea Grande"]
        self.data = None
        self.id = None
        self.local = None
        self.status = None
        self.tipo = None
        self.descricao = None

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def definir_local(self):
        print("Qual o local da Ocorrencia?")
        for numero,i in enumerate(self.locais_validos, start=1): # imprimir lista de locais validos
            print(f"{numero}. {i}")

        local_ocorrencia = input("Digite o nome do local: ")
        try:
            if local_ocorrencia not in self.locais_validos:
                raise ValueError
            print("Local valido") # Imprime Local valido se o local da ocorrencia definido for valido
            self.local = local_ocorrencia
        except:
            print("Local Invalido")
        return

    def definir_data(self):
        print("A ocorrencia aconteceu hoje ou em uma data retrograda?")
        print("1. Agora\n2.Retrograda")
        opcao = int(input("Digite uma opcao: "))

        try:
            if opcao == 1:
                self.data = dt.datetime.now("%d/%m/%Y %H:%M:%S")
            elif opcao == 2:
                data_ocorrencia = input("Digite a data da ocorrencia (DD/MM/AAAA): ")
                hora_ocorrencia = input("Digite a hora da ocorrencia (HH:MM): ")
                self.data = dt.datetime.strptime(f"{data_ocorrencia} {hora_ocorrencia}", "%d/%m/%Y %H:%M")
            else:
                raise ValueError
        except:
            print("Opcao invalida")

        return

    def definir_descricao(self):
        print("Defina a descricao da ocorrencia")
        descricao_ocorrencia = input("Digite uma descricao: ")
        self.descricao = descricao_ocorrencia
        return

    def definir_status(self):
        print("Defina o status da ocorrencia")
        print("1 - Em andamento\n2 - Finalizada")

        try:
            opcao = int(input("Digite uma opcao: "))
            if opcao == 1:
                self.status = "Em andamento"
            elif opcao == 2:
                self.status = "Finalizada"
            else:
                raise ValueError
        except:
            print("Opcao invalida")
        return

    def definir_tipo(self):
        print("Defina o tipo da ocorrencia")
        print("1 - Furto\n 2 - Roubo")
        try:
            opcao = int(input("Digite uma opcao: "))
            if opcao == 1:
                self.tipo = "Furto"
            elif opcao == 2:
                self.tipo = "Roubo"
            else:
                raise ValueError
        except:
            print("Opcao invalida")
        return

    def definir_id(self):
        pass

