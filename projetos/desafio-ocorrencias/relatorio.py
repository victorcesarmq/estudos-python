from registro import *

class Relatorio():
    def __init__(self, registro):
        self.df_ocorrencias = registro
#--------------------------------FILTROS PRONTOS--------------------------------
    """
    Filtros ja prontos para serem usados. Inclui Ocorrencias concluidas e Em andamento
    """
    def ocorrencias_concluidas(self):
        df_ocorrencias = self.df_ocorrencias.listar()
        df_filtrado = df_ocorrencias[df_ocorrencias["Status"] == "Concluído"]
        print(df_filtrado)

    def ocorrencias_andamento(self):
        df_ocorrencias = self.df_ocorrencias.listar()
        df_filtrado = df_ocorrencias[df_ocorrencias["Status"] == "Em andamento"]
        print(df_filtrado)



# ------------------------------FILTRO PERSONALIZADO-------------------------------
    """
    Permite aplicar múltiplos filtros de forma acumulativa.

    Obs: os valores informados devem ser idênticos aos presentes
    nas ocorrências cadastradas.
    """
    def filtro_personalizado(self):
        df_filtrado: pd.DataFrame = self.df_ocorrencias.listar()
        while True:
            print("\nFiltros:")
            print("1. Status")
            print("2. Local")
            print("3. Tipo")
            print("4. Data")
            print("5. Executar filtro")
            opcao = input("Escolha: ")
            if opcao == "1":
                status = input("Digite o status: ")
                df_filtrado = df_filtrado[df_filtrado["Status"] == status]
            elif opcao == "2":
                local = input("Digite o local: ")
                df_filtrado = df_filtrado[df_filtrado["Local"] == local]
            elif opcao == "3":
                tipo = input("Digite o tipo: ")
                df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo]
            elif opcao == "4":
                data = input("Digite a data: ")
                df_filtrado = df_filtrado[df_filtrado["Data"] == data]
            elif opcao == "5":
                print(df_filtrado)
                return
            else:
                print("Opção inválida")