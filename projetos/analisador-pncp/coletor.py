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

    def verificar_cache(self):
        return Path("dados/dados_teste.json").exists()

    def definir_url(self):
        url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
        return url

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

        while True:
            params = self.params_url()
            params["pagina"] = pagina

            r = requests.get(
                self.definir_url(),
                params=params,
                timeout=30
            )
            print(r.status_code)
            print(r.text)
            if r.status_code == 200:
                dados = r.json()
                todos_dados.extend(dados.get("data", []))
                print(todos_dados)

                if dados.get("paginasRestantes", 0) == 0:
                    df_dados = pd.DataFrame(todos_dados)
                    df_dados.to_json("./dados/dados_teste.json",
                                     orient="records",
                                     date_format="iso",
                                     indent=4,
                                     force_ascii=False
                                     )
                    break
                pagina += 1
                time.sleep(0.5)
            else:
                print(f"Erro: {r.status_code}")


