from registro import Registro
from ocorrencia import Ocorrencia
from relatorio import Relatorio
import pandas as pd
from pathlib import Path
import datetime as dt
import os
import json

ocorrencia_registro = Ocorrencia()
registro = Registro()
relatorio = Relatorio(registro)

path_df_ocorrencias = Path(__file__).parent / "dados" / "ocorrencias.json"

while True:
    print("Ocorrencias")
    print("1. Cadastrar Ocorrencia")
    print("2. Filtro de Ocorrencias")
    print("3. Filtro personalizado")
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
        relatorio.ocorrencias_concluidas()
    if escolha == 3:
        relatorio.filtro_personalizado()
