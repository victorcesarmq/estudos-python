import pandas as pd
from pathlib import Path
from pandas import DataFrame
import json



class Analisador:

    def __init__(self):

        # Caminho da pasta de dados
        self.path = Path("dados")

        # Datas do filtro atual
        self.dataInicial = None
        self.dataFinal = None

        # DataFrames originais
        self.df_cambio: DataFrame = None
        self.df_selic: DataFrame = None
        self.df_ipca: DataFrame = None

        # DataFrames filtrados
        self.df_cambio_filtrado: DataFrame = None
        self.df_selic_filtrado: DataFrame = None
        self.df_ipca_filtrado: DataFrame = None

        # DataFrame selecionado
        self.indicador_economico: DataFrame = None

        # Estatísticas IPCA
        self.media_ipca = None
        self.min_ipca = None
        self.max_ipca = None
        self.desvio_ipca = None

        # Estatísticas SELIC
        self.media_selic = None
        self.min_selic = None
        self.max_selic = None
        self.desvio_selic = None

        # Estatísticas Câmbio
        self.cambio_mediacompra = None
        self.cambio_mediavenda = None

        self.cambio_mincompra = None
        self.cambio_minvenda = None

        self.cambio_maxcompra = None
        self.cambio_maxvenda = None

        self.cambio_compradesvio = None
        self.cambio_vendadesvio = None

    # CARREGA JSONS
    def carregar_dados(self):

        # IPCA
        with open(self.path / "dados_ipca.json", "r") as ipca:

            dados_ipca = json.load(ipca)

            self.df_ipca = pd.DataFrame(list(dados_ipca.values()))

            self.df_ipca["data"] = pd.to_datetime(self.df_ipca["data"])

        # CÂMBIO
        with open(self.path / "dados_cambio.json", "r") as cambio:

            dados_cambio = json.load(cambio)

            self.df_cambio = pd.DataFrame(list(dados_cambio.values()))

            self.df_cambio["dataHoraCotacao"] = pd.to_datetime(self.df_cambio["dataHoraCotacao"])

        # SELIC
        with open(self.path / "dados_selic.json", "r") as selic:

            dados_selic = json.load(selic)

            self.df_selic = pd.DataFrame(list(dados_selic.values()))

            self.df_selic["data"] = pd.to_datetime(self.df_selic["data"])

        # Copias iniciais
        self.df_ipca_filtrado = self.df_ipca.copy()

        self.df_selic_filtrado = self.df_selic.copy()

        self.df_cambio_filtrado = self.df_cambio.copy()

        # Estatísticas
        self.calcular_estatisticas()

        return self.df_ipca, self.df_cambio, self.df_selic

    # CALCULA ESTATÍSTICAS
    def calcular_estatisticas(self):

        # IPCA
        self.media_ipca = self.df_ipca_filtrado["valor"].mean()

        self.min_ipca = self.df_ipca_filtrado["valor"].min()

        self.max_ipca = self.df_ipca_filtrado["valor"].max()

        self.desvio_ipca = self.df_ipca_filtrado["valor"].std()

        # SELIC
        self.media_selic = self.df_selic_filtrado["valor"].mean()

        self.min_selic = self.df_selic_filtrado["valor"].min()

        self.max_selic = self.df_selic_filtrado["valor"].max()

        self.desvio_selic = self.df_selic_filtrado["valor"].std()

        # CÂMBIO
        self.cambio_mediacompra = self.df_cambio_filtrado["cotacaoCompra"].mean()

        self.cambio_mediavenda = self.df_cambio_filtrado["cotacaoVenda"].mean()

        self.cambio_mincompra = self.df_cambio_filtrado["cotacaoCompra"].min()

        self.cambio_minvenda = self.df_cambio_filtrado["cotacaoVenda"].min()

        self.cambio_maxcompra = self.df_cambio_filtrado["cotacaoCompra"].max()

        self.cambio_maxvenda = self.df_cambio_filtrado["cotacaoVenda"].max()

        self.cambio_compradesvio = self.df_cambio_filtrado["cotacaoCompra"].std()

        self.cambio_vendadesvio = self.df_cambio_filtrado["cotacaoVenda"].std()

        # PRINTs

        print("-----------IPCA-----------")
        print(f"Media: {self.media_ipca:.4f}")
        print(f"Minimo: {self.min_ipca:.4f}")
        print(f"Maxima: {self.max_ipca:.4f}")
        print(f"Desvio padrao: {self.desvio_ipca:.4f}")

        print("-----------CAMBIO-----------")
        print(f"Valor MEDIO Compra: {self.cambio_mediacompra:.4f}")
        print(f"Valor MEDIO Venda: {self.cambio_mediavenda:.4f}")
        print(f"Valor Minimo Compra: {self.cambio_mincompra:.4f}")
        print(f"Valor Minimo Venda: {self.cambio_minvenda:.4f}")
        print(f"Desvio Compra: {self.cambio_compradesvio:.4f}")
        print(f"Desvio Venda: {self.cambio_vendadesvio:.4f}")

        print("-----------SELIC-----------")
        print(f"Media: {self.media_selic:.4f}")
        print(f"Minimo: {self.min_selic:.4f}")
        print(f"Maxima: {self.max_selic:.4f}")
        print(f"Desvio padrao: {self.desvio_selic:.4f}")

    # ESCOLHER DATAFRAME
    def escolher_DataFrame(self):

        while True:

            print("1. Selic")
            print("2. IPCA")
            print("3. Cambio")

            escolha_df = input("Escolha o Indicador Economico: ").strip().lower()

            try:

                if escolha_df in ["1", "selic"]:

                    self.indicador_economico = self.df_selic_filtrado

                    break

                elif escolha_df in ["2", "ipca"]:

                    self.indicador_economico = self.df_ipca_filtrado

                    break

                elif escolha_df in ["3", "cambio"]:

                    self.indicador_economico = self.df_cambio_filtrado

                    break

                else:
                    raise ValueError

            except ValueError:

                print("\nOPÇÃO INVÁLIDA!")

        return self.indicador_economico

    # FILTRAR PERÍODO
    def filtrar_periodo(self, dataInicial, dataFinal):

        try:

            self.dataInicial = pd.to_datetime(dataInicial, format="%d/%m/%Y")

            self.dataFinal = pd.to_datetime(dataFinal, format="%d/%m/%Y") + pd.Timedelta(days=1)

            # SELIC
            self.df_selic_filtrado = self.df_selic[(self.df_selic["data"] >= self.dataInicial) &(self.df_selic["data"] <= self.dataFinal)]

            # IPCA
            self.df_ipca_filtrado = self.df_ipca[(self.df_ipca["data"] >= self.dataInicial) & (self.df_ipca["data"] <= self.dataFinal)]

            # CÂMBIO
            self.df_cambio_filtrado = self.df_cambio[(self.df_cambio["dataHoraCotacao"] >= self.dataInicial) & (self.df_cambio["dataHoraCotacao"] <= self.dataFinal)]

            # Recalcula estatísticas
            self.calcular_estatisticas()

            print(f"Periodo filtrado:{self.dataInicial.strftime('%d/%m/%Y')} até {(self.dataFinal - pd.Timedelta(days=1)).strftime('%d/%m/%Y')}")

        except ValueError:

            print("DATA INVALIDA!")

        except Exception as erro:

            print(f"Erro ao filtrar periodo: {erro}")

    # EXPORTAR CSV
    def exportar_csv(self):

        self.df_selic_filtrado.to_csv(self.path / "selic_filtrado.csv", index=False)

        self.df_ipca_filtrado.to_csv(self.path / "ipca_filtrado.csv", index=False)

        self.df_cambio_filtrado.to_csv(self.path / "cambio_filtrado.csv", index=False)

        print("CSV exportado com sucesso!")