from registro import Registro
from ocorrencia import Ocorrencia

import pandas as pd
from pathlib import Path
import datetime as dt
import os
import json

ocorrencia_registro = Ocorrencia()
registro = Registro()

path_df_ocorrencias = Path(__file__).parent / "dados" / "ocorrencias.json"

while True:
    print("Ocorrencias")
    print("1. Cadastrar Ocorrencia")
    print("2. Ocorrencias em Andamento")
    print("3. Ocorrencias Concluidas")
    print("4. Ocorrencias Especifica")
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
        df_ocorrencias = registro.listar()

        df_filtrado = df_ocorrencias[df_ocorrencias["Status"] == "Em andamento"]
        print(df_filtrado)

    if escolha == 3:
        df_ocorrencias = registro.listar()

        df_filtrado = df_ocorrencias[df_ocorrencias["Status"] == "Concluído"]
        print(df_filtrado)
    if escolha == 4:
        escolha = int(input("ID da ocorrencia"))
        df_ocorrencias = registro.listar()
        df_filtrado = df_ocorrencias[df_ocorrencias["Id"] == escolha][["Descrição","Data"]]
        print(df_filtrado)