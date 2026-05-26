import requests
import json
import pandas as pd
from pathlib import Path
'''
url padrao
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={dd/MM/yyyy}&dataFinal={dd/MM/yyyy}
https ://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/[codigo_recurso]?$format=json&[Outros Parâmetros]
'''


class Coletor:
    def __init__(self):
        self.dataInicial = None
        self.dataFinal = None
        self.path = Path("./dados")
        self.path.mkdir(parents=True, exist_ok=True)

    def coletor(self, dataInicial=None, dataFinal=None):

        #Data
        print("Formato DIA/MES/ANO\nex: 31/01/2021")
        dataInicial = dataInicial if dataInicial is not None else input("Digite a data inicial: ")
        dataFinal = dataFinal if dataFinal is not None else input("Digite a data final: ")

        #Data Cambio
        dataInicial_ptax = dataInicial.replace("/","-")
        dataFinal_ptax = dataFinal.replace("/","-")

        #URL's
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

        #Tratamento de Dados SELIC
        df_selic = pd.DataFrame(dados_selic)  # A partir daqui vira um DataFrame do pandas.
        df_selic["valor"] = df_selic["valor"].str.replace(",", ".")  # A API recebe o valor apenas com virgula.
        df_selic["valor"] = pd.to_numeric(df_selic["valor"])  # valores se tornam float
        df_selic["data"] = pd.to_datetime(df_selic["data"],format="%d/%m/%Y")  # converter para o formato datetime do pandas
        df_selic.to_json("./dados/dados_selic.json", orient="index",date_format="iso", indent=4)  # salva o arquivo em json e aplica o formato iso na coluna "data"

        # GET IPCA
        r_ipca = requests.get(url_ipca, params=parametros)
        dados_ipca = r_ipca.json()

        #Tratamento de Dados IPCA
        df_ipca = pd.DataFrame(dados_ipca)
        df_ipca["valor"] = df_ipca["valor"].str.replace(",", ".")
        df_ipca["valor"] = pd.to_numeric(df_ipca["valor"])
        df_ipca["data"] = pd.to_datetime(df_ipca["data"], format="%d/%m/%Y")
        df_ipca.to_json("./dados/dados_ipca.json", orient="index",date_format="iso", indent=4)

        # Cambio
        r_cambio = requests.get(url_cambio)
        dados_cambio = r_cambio.json()
        # print(dados_cambio)
        df_cambio = pd.DataFrame(dados_cambio["value"])
        df_cambio.to_json("./dados/dados_cambio.json",orient="index", date_format="iso", indent=4)
        return dataInicial, dataFinal

coletor = Coletor()
coletor.coletor()