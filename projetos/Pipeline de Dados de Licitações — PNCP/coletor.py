import os
import requests
import json
import pandas as pd
import sqlite3
from pathlib import Path
import time

class Coletor:
    def __init__(self):

        # Caminho padrão da pasta de dados
        self.path = Path("dados")

        #Parametros
        self.dataInicial = None
        self.dataFinal = None
        self.codigoModalidadeContratacao = None
        self.uf = None

    def solicitar_parametros(self):

        print("ANO/MES/DIA")

        self.dataInicial = (input("Digita a data inicial: ")
                            .replace("-", "")
                            .replace("/", "")
                            .replace(" ", ""))

        self.dataFinal = (input("Digita a data final: ")
                          .replace("-", "")
                          .replace("/", "")
                          .replace(" ", ""))

        print(self.dataInicial, self.dataFinal)

    def params_url(self):
        '''
        dataInicial/dataFinal = 20260101 (ANO/MES/DIA)
        '''

        params = {
            "dataInicial": self.dataInicial,
            "dataFinal": self.dataFinal,
            "codigoModalidadeContratacao": 6,
            "uf": "MT",
            "tamanhoPagina": 10,
            "pagina": 1
        }
        return params

    def coletar_todas_paginas(self):
        pagina = 1
        todos_dados = []
        
        try:
            while True:
                params = self.params_url()
                params["pagina"] = pagina

                r = requests.get(
                    "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao",
                    params=params,
                    timeout=30
                )

                if r.status_code == 200:
                    dados = r.json()
                    todos_dados.extend(dados.get("data", []))

                    if dados.get("paginasRestantes", 0) == 0:
                        df_dados = pd.json_normalize(todos_dados)
                        break
                    pagina += 1
                    time.sleep(1)
                elif r.status_code == 204:
                    print('Sem dados para o periodo informado')
                else:
                    print(f"Erro {r.status_code}: {r.text}")
                    break
        except requests.exceptions.Timeout:
            print('A API do PNCP esta fora do ar no momento')
            df = pd.DataFrame()
            return df
        return df_dados

