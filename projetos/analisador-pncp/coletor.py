import os
import requests
import json
import pandas as pd
import sqlite3
from pathlib import Path

class coletor:
    def __init__(self):

        # Caminho padrão da pasta de dados
        self.path = Path("dados")

        #Parametros
        self.dataInicial = None
        self.dataFinal = None
        self.codigoModalidadeContratacao = None
        self.uf = None
        self.tamanhoPagina = None
        self.pagina = None


    def definir_url(self):
        url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
        return url

    def params_url(self):
        '''
        dataInicial/FINAL = 20260101 (ANO/MES/DIA)
        '''

        params = {
            "dataInicial": "20260101",
            "dataFinal": "20260131",
            "codigoModalidadeContratacao": 6,
            "uf": "MT",
            "tamanhoPagina": 10,
            "pagina": 1
        }
        return params

    def coletar_dados(self):
        r = requests.get(self.definir_url(), params=self.params_url(), timeout=10)
        print(r.status_code)
        print(r.text)
        print(r.json())
        if r.status_code == 200:
            dados = r.json()
            df_dados = pd.DataFrame(dados)
            df_dados
        else:
            print(f"Erro: {r.status_code}")