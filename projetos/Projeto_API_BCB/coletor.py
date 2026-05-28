import requests
import json
import pandas as pd
from pathlib import Path
import datetime as dt
'''
url padrao
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dadosx?formato=json&dataInicial={dd/MM/yyyy}&dataFinal={dd/MM/yyyy}
https ://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/[codigo_recurso]?$format=json&[Outros Parâmetros]
'''


class Coletor:
    def __init__(self):
        self.dataInicial = None
        self.dataFinal= None
        self.path = Path("dados")
        self.path.mkdir(parents=True, exist_ok=True)

    def coletar_dados(self, dataInicial=None, dataFinal=None):

        #Carregar as datas Inicial/Final
        if Path("dados/dados_ipca.json").exists():
            with open("dados/dados_ipca.json", "r") as ipca:
                dados_ipca = json.load(ipca)
                df_data = pd.DataFrame(dados_ipca.values())
                df_data["data"] = pd.to_datetime(df_data["data"], format="%d/%m/%Y")
                self.dataInicial = df_data["data"].iloc[0]
                self.dataFinal = df_data["data"].iloc[-1]
                pd.to_datetime(self.dataInicial)
                pd.to_datetime(self.dataFinal)
            print("1. Usar período já carregado")
            print("2. Novo período")
            print(f"Periodo Atual: {self.dataInicial.strftime('%d/%m/%Y')} - {self.dataFinal.strftime('%d/%m/%Y')}")
        else:
            print("Nenhum periodo definido!")
            print("2. Novo período")
        while True:
            escolha = input("Escolha uma opcao: ")
            try:
                if escolha == "1":
                    if not Path("dados/dados_ipca.json").exists():
                        print("Nenhum dado carregado ainda. Escolha a opção 2.")
                    else:
                        print("Dados já existem. Carregando do cache.")
                        break

                elif escolha == "2":
                    # Data
                    print("Formato DIA/MES/ANO\nex: 31/01/2021")
                    dataInicial = dataInicial if dataInicial is not None else input("Digite a data inicial: ")
                    dataFinal = dataFinal if dataFinal is not None else input("Digite a data final: ")
                        # Data Cambio
                    data_objetoInicial = dt.datetime.strptime(dataInicial, "%d/%m/%Y")
                    dataInicial_ptax = data_objetoInicial.strftime("%m-%d-%Y")
                    data_objetoFinal = dt.datetime.strptime(dataFinal, "%d/%m/%Y")
                    dataFinal_ptax = data_objetoFinal.strftime("%m-%d-%Y")
                    # URL's
                    url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"
                    url_ipca = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
                    url_cambio = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='{dataInicial_ptax}',dataFinalCotacao='{dataFinal_ptax}')?$format=json"
                    parametros = {
                        "formato": "json",
                        "dataInicial": dataInicial,
                        "dataFinal": dataFinal
                    }
                    # GET SELIC
                    r_selic = requests.get(url_selic, params=parametros)
                    dados_selic = r_selic.json()
                    # Tratamento de Dados SELIC
                    df_selic = pd.DataFrame(dados_selic)
                    df_selic["valor"] = df_selic["valor"].str.replace(",", ".")
                    df_selic["valor"] = pd.to_numeric(df_selic["valor"])
                    df_selic["data"] = pd.to_datetime(df_selic["data"], format="%d/%m/%Y")  # OQ ESSA LINHA FAZ
                    df_selic["data"] = df_selic["data"].dt.strftime("%d/%m/%Y")
                    df_selic.to_json("./dados/dados_selic.json", orient="index", date_format="iso", indent=4)

                    # GET IPCA
                    r_ipca = requests.get(url_ipca, params=parametros)
                    dados_ipca = r_ipca.json()

                    # Tratamento de Dados IPCA
                    df_ipca = pd.DataFrame(dados_ipca)
                    df_ipca["valor"] = df_ipca["valor"].str.replace(",", ".")
                    df_ipca["valor"] = pd.to_numeric(df_ipca["valor"])
                    df_ipca["data"] = pd.to_datetime(df_ipca["data"], format="%d/%m/%Y")
                    df_ipca["data"] = df_ipca["data"].dt.strftime("%d/%m/%Y")
                    df_ipca.to_json("./dados/dados_ipca.json", orient="index", date_format="iso", indent=4)

                    # GET CAMBIO
                    r_cambio = requests.get(url_cambio)
                    dados_cambio = r_cambio.json()

                    # TRATAMENTO CAMBIO
                    df_cambio = pd.DataFrame(dados_cambio["value"])
                    df_cambio["dataHoraCotacao"] = pd.to_datetime(df_cambio["dataHoraCotacao"])
                    df_cambio["dataHoraCotacao"] = df_cambio["dataHoraCotacao"].dt.strftime("%d/%m/%Y")
                    df_cambio.to_json("./dados/dados_cambio.json", orient="index", date_format="iso", indent=4)
                    break
                else:
                    raise ValueError
            except ValueError:
                print("OPCAO INVALIDA INVALIDO")

        return dataInicial, dataFinal






