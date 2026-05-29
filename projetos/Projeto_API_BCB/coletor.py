import requests
import pandas as pd
import json
import datetime as dt
from pathlib import Path

class Coletor:

    def __init__(self):

        # Datas utilizadas no período atual
        self.dataInicial = None
        self.dataFinal = None

        # Caminho padrão da pasta de dados
        self.path = Path("dados")

    # VERIFICA SE JÁ EXISTEM DADOS SALVOS
    def verificar_cache(self):

        return Path("dados/dados_ipca.json").exists()

    # CARREGA PERÍODO JÁ EXISTENTE
    def carregar_periodo_existente(self):

        with open("dados/dados_ipca.json", "r") as ipca:

            dados_ipca = json.load(ipca)

            # values() precisa virar lista
            df_data = pd.DataFrame(list(dados_ipca.values()))

            # Converte coluna para datetime
            df_data["data"] = pd.to_datetime(df_data["data"])

            # Garante ordem correta
            df_data = df_data.sort_values(by="data")

            # Define período atual
            self.dataInicial = df_data["data"].iloc[0]
            self.dataFinal = df_data["data"].iloc[-1]

    # MOSTRA MENU
    def mostrar_menu(self):

        if self.verificar_cache():

            print("1. Usar período já carregado")
            print("2. Novo período")

            print("IMPORTANTE")
            print(f"TODOS OS DADOS APRESENTADOS E SOLICITADOS DEVEM ESTAR ENTRE AS DATAS: {self.dataInicial.strftime('%d/%m/%Y')} - {self.dataFinal.strftime('%d/%m/%Y')}")
            print("Caso queira um periodo diferente escolha a opcao 2")
        else:

            print("Nenhum periodo definido!")
            print("2. Novo período")

    # SOLICITA DATAS AO USUÁRIO
    def solicitar_datas(self):

        print("Formato DIA/MES/ANO")
        print("ex: 31/01/2021")

        # ALTERAÇÃO:
        # Sempre pede novamente os valores
        # para evitar loop infinito após erro
        dataInicial = input("Digite a data inicial: ")

        dataFinal = input("Digite a data final: ")

        return dataInicial, dataFinal

    # CONVERTE DATAS PARA PTAX
    def converter_datas_ptax(self, dataInicial, dataFinal):

        data_objetoInicial = dt.datetime.strptime(dataInicial, "%d/%m/%Y")

        data_objetoFinal = dt.datetime.strptime(dataFinal, "%d/%m/%Y")

        dataInicial_ptax = data_objetoInicial.strftime("%m-%d-%Y")

        dataFinal_ptax = data_objetoFinal.strftime("%m-%d-%Y")

        return dataInicial_ptax, dataFinal_ptax

    # MONTA URLs DAS APIs
    def montar_urls(self, dataInicial_ptax, dataFinal_ptax):

        url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"

        url_ipca = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"

        url_cambio = (
            "https://olinda.bcb.gov.br/olinda/servico/"
            "PTAX/versao/v1/odata/"
            f"CotacaoDolarPeriodo(dataInicial='{dataInicial_ptax}',"
            f"dataFinalCotacao='{dataFinal_ptax}')?$format=json"
        )

        return url_selic, url_ipca, url_cambio

    # MONTA PARÂMETROS DAS APIs
    def montar_parametros(self, dataInicial, dataFinal):

        parametros = {
            "formato": "json",
            "dataInicial": dataInicial,
            "dataFinal": dataFinal
        }

        return parametros

    # TRATAMENTO PADRÃO SELIC/IPCA
    def tratar_dataframe_taxa(self, df):

        df["valor"] = df["valor"].str.replace(",", ".", regex=False)

        df["valor"] = pd.to_numeric(df["valor"])

        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

        return df

    # SALVA DATAFRAME EM JSON
    def salvar_json(self, df, nome_arquivo):

        df.to_json(f"./dados/{nome_arquivo}", orient="index", date_format="iso", indent=4)

    # BAIXAR DADOS SELIC
    def baixar_selic(self, url_selic, parametros):

        r_selic = requests.get(url_selic, params=parametros)

        r_selic.raise_for_status()

        dados_selic = r_selic.json()

        df_selic = pd.DataFrame(dados_selic)

        df_selic = self.tratar_dataframe_taxa(df_selic)

        self.salvar_json(df_selic, "dados_selic.json")

    # BAIXAR DADOS IPCA
    def baixar_ipca(self, url_ipca, parametros):

        r_ipca = requests.get(url_ipca, params=parametros)

        r_ipca.raise_for_status()

        dados_ipca = r_ipca.json()

        df_ipca = pd.DataFrame(dados_ipca)

        df_ipca = self.tratar_dataframe_taxa(df_ipca)

        self.salvar_json(df_ipca, "dados_ipca.json")

    # BAIXAR DADOS CÂMBIO
    def baixar_cambio(self, url_cambio):

        r_cambio = requests.get(url_cambio)

        r_cambio.raise_for_status()

        dados_cambio = r_cambio.json()

        df_cambio = pd.DataFrame(dados_cambio["value"])

        df_cambio["dataHoraCotacao"] = pd.to_datetime(df_cambio["dataHoraCotacao"])

        self.salvar_json(df_cambio, "dados_cambio.json")

    # FUNÇÃO PRINCIPAL
    def coletar_dados(self):

        # Verifica cache existente
        if self.verificar_cache():

            # Carrega período já salvo
            self.carregar_periodo_existente()

        # Mostra menu
        self.mostrar_menu()

        while True:

            escolha = input("Escolha uma opcao: ").strip()

            try:

                # USAR CACHE
                if escolha == "1":

                    if not self.verificar_cache():

                        print("Nenhum dado carregado ainda.")

                        continue

                    print("Dados já existem. Carregando do cache.")

                    break

                # NOVO PERÍODO
                elif escolha == "2":

                    # ALTERAÇÃO:
                    # Sempre solicita novamente as datas
                    # para evitar reutilizar valores inválidos
                    dataInicial, dataFinal = self.solicitar_datas()

                    # Converte datas
                    dataInicial_ptax, dataFinal_ptax = self.converter_datas_ptax(dataInicial, dataFinal)

                    # Monta URLs
                    url_selic, url_ipca, url_cambio = self.montar_urls(dataInicial_ptax, dataFinal_ptax)

                    # Monta parâmetros
                    parametros = self.montar_parametros(dataInicial, dataFinal)

                    # Baixa dados
                    self.baixar_selic(url_selic, parametros)

                    self.baixar_ipca(url_ipca, parametros)

                    self.baixar_cambio(url_cambio)

                    print("Dados coletados com sucesso!")

                    break

                else:
                    raise ValueError

            # ERRO DE INPUT/DATA
            except ValueError:

                print("OPCAO OU DATA INVALIDA!")


            # ERRO DE REQUEST
            except requests.RequestException as erro:

                print(f"Erro na requisição: {erro}")

            # ERRO GERAL
            except Exception as erro:

                print(f"Erro inesperado: {erro}")