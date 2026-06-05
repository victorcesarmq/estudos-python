import sqlite3

class Banco:
    def __init__(self):
        self.conectar = sqlite3.connect("dados/pncp.db")
        self.cursor = self.conectar.cursor()

    def iniciar_banco(self):
        pass
    def criar_tabela(self):
        pass
    def inserir_licitacoes(self, df):
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
                df[col] = df[col].astype(str)
        df.to_sql("licitacoes", self.conectar, if_exists="replace", index=False)
        self.conectar.commit()