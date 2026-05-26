from registro import Registro
from ocorrencia import Ocorrencia
from relatorio import Relatorio

ocorrencia_registro = Ocorrencia()
registro = Registro()
relatorio = Relatorio(registro)

while True:
    print("Ocorrencias")
    print("1. Cadastrar Ocorrencia")
    print("2. Ocorrencias Concluidas")
    print("3. Ocorrencias Em Andamento")
    print("4. Ocorrencias Pendentes")
    print("5. Filtro personalizado")
    print("6. Encerrar Ocorrencia")
    print("0. Sair")
    escolha = int(input("Escolha: "))
    if escolha == 1:
        ocorrencia_registro = Ocorrencia()
        ocorrencia_registro.definir_local()
        ocorrencia_registro.definir_data()
        ocorrencia_registro.definir_descricao()
        ocorrencia_registro.definir_status()
        ocorrencia_registro.definir_tipo()
        registro.adicionar(ocorrencia_registro)
        registro.salvar()
    elif escolha == 2:
        relatorio.ocorrencias_concluidas()
    elif escolha == 3:
        relatorio.ocorrencias_andamento()
    elif escolha == 4:
        relatorio.ocorrencias_pendentes()
    elif escolha == 5:
        relatorio.filtro_personalizado()
    elif escolha == 6:
        registro.encerrar()
    elif escolha == 0:
        break
