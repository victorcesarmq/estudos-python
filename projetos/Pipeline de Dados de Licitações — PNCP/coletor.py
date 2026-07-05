import os
import requests
import json
import pandas as pd
import sqlite3
from pathlib import Path
import time
import utils

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
                r.raise_for_status()
                print(r.status_code)
                if r.status_code == 200:
                    dados = r.json()
                    todos_dados.extend(dados.get("data", []))
                    if dados.get("paginasRestantes", 0) == 0:
                        df_dados = pd.json_normalize(todos_dados)
                        df_dados.to_json(f"./dados/df_dados", orient='records', date_format="iso", indent=4)
                        break
                    pagina += 1
                    time.sleep(1)

                elif r.status_code == 204:
                    print('Sem dados para o periodo informado')
                    df_dados = pd.DataFrame()
                    return df_dados
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            df_dados = pd.DataFrame()
            return df_dados
        return df_dados

