import sqlite3
import utils
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
class Banco:
    def __init__(self):
        self.conectar = sqlite3.connect("dados/pncp.db")
        self.cursor = self.conectar.cursor()

    def iniciar_banco(self):
        pass
    def criar_tabela(self):
        self.cursor.execute(
            '''CREATE TABLE if not exists licitacoes
                                ''')
        pass
    def inserir_licitacoes(self, df):
        if utils.empty(df):
<<<<<<< Updated upstream
            print("Sem dados para colocar no banco")
=======
            print("Sem dados para o banco")
>>>>>>> Stashed changes
        else:
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
                    df[col] = df[col].astype(str)
            df.to_sql("licitacoes", self.conectar, if_exists="replace", index=False)
            self.conectar.commit()
