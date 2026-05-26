import requests
import json
import pandas as pd

'''
url padrao
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={dd/MM/yyyy}&dataFinal={dd/MM/yyyy}
'''


class Coletor:
    def __init__(self):
        self.dataInicial = None
        self.dataFinal = None

    def coletor(self, dataInicial, dataFinal):
        url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"
        url_ipca = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
        url_cambio = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='{dataInicial}',dataFinal='{dataFinal}')?$format=json"
        print("Formato DIA/MES/ANO\nex: 31/01/2021")

        # --- ALTERADO: Correção da sintaxe do operador ternário para a data inicial ---
        dataInicial = dataInicial if dataInicial is not None else input("Digite a data inicial: ")
        # --- ALTERADO: Correção da sintaxe do operador ternário para a data final ---
        dataFinal = dataFinal if dataFinal is not None else input("Digite a data final: ")

        parametros = {
            "formato": "json",
            "dataInicial": dataInicial,
            "dataFinal": dataFinal
        }

        # SELIC
        r_selic = requests.get(url_selic, params=parametros)
        dados_selic = r_selic.json()
        df_selic = pd.DataFrame(dados_selic)  # A partir daqui vira um DataFrame do pandas.
        df_selic["valor"] = df_selic["valor"].str.replace(",", ".")  # A API recebe o valor apenas com virgula.
        df_selic["valor"] = pd.to_numeric(df_selic["valor"])  # valores se tornam float
        df_selic["data"] = pd.to_datetime(df_selic["data"],format="%d/%m/%Y")  # converter para o formato datetime do pandas
        df_selic.to_json("dados_selic.json", orient="records",date_format="iso")  # salva o arquivo em json e aplica o formato iso na coluna "data"

        # IPCA
        r_ipca = requests.get(url_ipca, params=parametros)
        dados_ipca = r_ipca.json()
        df_ipca = pd.DataFrame(dados_ipca)
        df_ipca["valor"] = df_ipca["valor"].str.replace(",", ".")
        df_ipca["valor"] = pd.to_numeric(df_ipca["valor"])
        df_ipca["data"] = pd.to_datetime(df_ipca["data"], format="%d/%m/%Y")
        df_ipca.to_json("dados_ipca.json", orient="records",date_format="iso")

        # Cambio
        r_cambio = requests.get(url_cambio)
        dados_cambio = r_cambio.json()
        df_cambio = pd.DataFrame(dados_cambio)
        df_cambio["valor"] = df_cambio["valor"].str.replace(",", ".")
        df_cambio["valor"] = pd.to_numeric(df_cambio["valor"])
        df_cambio["data"] = pd.to_datetime(df_cambio["data"], format="%d/%m/%Y")
        df_cambio.to_csv("dados_cambio.csv", index=False)


    def salvar_json(self):
        pass