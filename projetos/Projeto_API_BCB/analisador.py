import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pandas import DataFrame
import json


class Analisador():
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

        #Minimas
        self.min_ipca = None
        self.min_selic = None
        self.cambio_minvenda = None
        self.cambio_mincompra = None

        #Maximas
        self.max_ipca = None
        self.max_selic = None
        self.cambio_maxcompra = None
        self.cambio_maxvenda = None

        #Desvio Padrao
        self.ipca_desvio = None
        self.selic_desvio = None
        self.cambio_vendadesvio = None
        self.cambio_compradesvio = None

    def carregar_dados(self):
        #IPCA
        with open("dados/dados_ipca.json", "r") as ipca:
            dados_ipca = json.load(ipca)
            self.df_ipca = pd.DataFrame(dados_ipca.values())
            self.df_ipca["data"] = pd.to_datetime(self.df_ipca["data"],format="%d/%m/%Y")

            # media
            self.media_ipca = self.df_ipca["valor"].mean()

            # Max
            self.max_ipca = self.df_ipca["valor"].max()

            # Min
            self.min_ipca = self.df_ipca["valor"].min()

            #Desvio
            self.desvio_ipca = self.df_ipca["valor"].std()
            print("-----------IPCA-----------")
            print(f"Media:{self.media_ipca:.4f}")
            print(f"Minimo:{self.min_ipca:.4f}")
            print(f"Maxima:{self.max_ipca:.4f}")
            print(f"Desvio padrao:{self.desvio_ipca:.4f}")

        #Cambio
        with open("dados/dados_cambio.json", "r") as cambio:
            dados_cambio = json.load(cambio)
            self.df_cambio = pd.DataFrame(dados_cambio.values())

            #media
            self.cambio_mediacompra = self.df_cambio["cotacaoCompra"].mean()
            self.cambio_mediavenda = self.df_cambio["cotacaoVenda"].mean()

            #Max
            self.cambio_maxcompra = self.df_cambio["cotacaoCompra"].max()
            self.cambio_maxvenda = self.df_cambio["cotacaoVenda"].max()

            #Min
            self.cambio_mincompra = self.df_cambio["cotacaoCompra"].min()
            self.cambio_minvenda = self.df_cambio["cotacaoVenda"].min()

            #Desvio
            self.cambio_vendadesvio = self.df_cambio["cotacaoVenda"].std()
            self.cambio_compradesvio = self.df_cambio["cotacaoCompra"].std()
            print("-----------CAMBIO-----------")
            print(f"Valor MEDIO de Compra: {self.cambio_mediacompra:.4f}")
            print(f"Valor MEDIO de Venda: {self.cambio_mediavenda:.4f}")
            print(f"Valor Minimo de Compra: {self.cambio_mincompra:.4f}")
            print(f"Valor Minimo de Venda: {self.cambio_minvenda:.4f}")
            print(f"Desvio padrao de Compra: {self.cambio_vendadesvio:.4f}")
            print(f"Desvio padrao de Venda:{self.cambio_compradesvio:.4f}")

        #Selic
        with open("dados/dados_selic.json", "r") as selic:
            dados_selic = json.load(selic)
            self.df_selic = pd.DataFrame(dados_selic.values())
            self.df_selic["data"] = pd.to_datetime(self.df_selic["data"],format="%d/%m/%Y")

            # media
            self.media_selic = self.df_selic["valor"].mean()

            # Max
            self.max_selic = self.df_selic["valor"].max()

            # Min
            self.min_selic = self.df_selic["valor"].min()

            # Desvio
            self.desvio_selic = self.df_selic["valor"].std()

            print("-----------SELIC-----------")
            print(f"Media:{self.media_selic:.4f}")
            print(f"Minimo:{self.min_selic:.4f}")
            print(f"Maxima:{self.max_selic:.4f}")
            print(f"Desvio padrao:{self.desvio_selic:.4f}")

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

    def exportar_csv(self):
        selic_excel
        ipca_excel
        cambio_excel
        pass
