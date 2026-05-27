import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pandas import DataFrame
import json


class Analisar():
    def __init__(self):
        self.path = Path("dados")

        #Datas
        self.dataInicial = None
        self.dataFinal = None

        # DataFrames
        self.indicador_economico: DataFrame = None
        self.df_cambio: DataFrame = None
        self.df_selic: DataFrame = None
        self.df_ipca: DataFrame = None

        # Medias
        self.media_ipca = None
        self.media_selic = None
        self.cambio_mediacompra = None
        self.cambio_mediavenda = None

    def carregar_dados(self):

        with open("dados/dados_ipca.json", "r") as ipca:
            dados_ipca = json.load(ipca)
            self.df_ipca = pd.DataFrame(dados_ipca.values())
            self.df_ipca["data"] = pd.to_datetime(self.df_ipca["data"],format="%d/%m/%Y")
            self.media_ipca = self.df_ipca["valor"].mean()
            print("-----------IPCA-----------")
            print(f"{self.media_ipca:.4f}")

        with open("dados/dados_cambio.json", "r") as cambio:
            dados_cambio = json.load(cambio)
            self.df_cambio = pd.DataFrame(dados_cambio.values())
            self.cambio_mediacompra = self.df_cambio["cotacaoCompra"].mean()
            self.cambio_mediavenda = self.df_cambio["cotacaoVenda"].mean()
            print("-----------CAMBIO-----------")
            print(f"{self.cambio_mediacompra:.4f}")
            print(f"{self.cambio_mediavenda:.4f}")

        with open("dados/dados_selic.json", "r") as selic:
            dados_selic = json.load(selic)
            self.df_selic = pd.DataFrame(dados_selic.values())
            self.df_selic["data"] = pd.to_datetime(self.df_selic["data"],format="%d/%m/%Y")
            self.media_selic = self.df_selic["valor"].mean()
            print("-----------SELIC-----------")
            print(f"{self.media_selic:.4f}")

        return self.df_ipca,self.df_cambio,self.df_selic


    def escolher_DataFrame(self):
        while True:
            print("1. Selic\n2. IPCA\n3. Cambio")
            escolha_df = input("Escolha o Indicador Economico: ").strip().lower()
            try:
                if escolha_df in ["1", "selic"]:
                    self.indicador_economico = self.df_selic
                    break
                elif escolha_df in ["2", "ipca"]:
                    self.indicador_economico = self.df_ipca
                    break
                elif escolha_df in ["3", "cambio"]:
                    self.indicador_economico = self.df_cambio
                    break
                else: raise ValueError
            except ValueError:
                print("\nOPÇÃO INVÁLIDA! Tente novamente.")
        return self.indicador_economico

    def definir_periodo(self,dataInicial=None,dataFinal=None,):
        print("Formato DIA/MES/ANO\nex: 31/01/2021")
        dataInicial = input("Digite a data Inicial: ")
        dataFinal = input("Digite a data Final: ")

        #Datetime Pandas
        dataInicial = pd.to_datetime(dataInicial)
        dataFinal = pd.to_datetime(dataFinal)

        self.dataInicial = dataInicial
        self.dataFinal = dataFinal
        return dataInicial,dataFinal

    def visualizador(self):
        # print(self.indicador_economico.info())
        # print(self.indicador_economico.head())
        pass

    def exportar_csv(self):
        pass