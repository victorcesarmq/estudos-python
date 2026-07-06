import sqlite3
import pandas as pd




class Analisador:
    def __init__(self):
        pass

    def top_licitacoes(self,dados_brutos):
        colunas = ["Orgao", "Valor Estimado", "Valor Homologado", "Municipio"]
        df = pd.DataFrame(dados_brutos, columns=colunas)
        df['Valor Estimado'] = df['Valor Estimado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df['Valor Homologado'] = df['Valor Homologado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', None)
        print(df)

    def top_orgaos(self,dados_brutos):
        colunas = ["Processo", "Orgao", "Valor Estimado", "Valor Homologado", "Municipio"]
        df = pd.DataFrame(dados_brutos, columns=colunas)
        df['Valor Estimado'] = df['Valor Estimado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df['Valor Homologado'] = df['Valor Homologado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', None)
        print(df)

    def consultar_por_municipio(self,dados_brutos):
        colunas = ["Orgao", "Valor Estimado", "Valor Homologado", "Municipio"]
        df = pd.DataFrame(dados_brutos, columns=colunas)
        df['Valor Estimado'] = df['Valor Estimado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df['Valor Homologado'] = df['Valor Homologado'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', None)
