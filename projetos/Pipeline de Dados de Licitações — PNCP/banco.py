import sqlite3
import utils

class Banco:
    def __init__(self):
        self.conectar = sqlite3.connect("dados/pncp.db")
        self.cursor = self.conectar.cursor()

    def iniciar_banco(self):
        pass

    def criar_tabela(self): #Atualmente inutil e nao utilizada no fluxo do codigo
        self.cursor.execute(
            '''CREATE TABLE if NOT EXISTS licitacoes (
            anoCompra INTEGER NOT NULL,
            dataInclusao TEXT NOT NULL,
            dataPublicacaoPncp TEXT NOT NULL,
            dataAtualizacao TEXT NOT NULL,
            dataAberturaProposta TEXT NOT NULL,
            dataEncerramentoProposta TEXT NOT NULL,
            objetoCompra TEXT NOT NULL,
            valorTotalEstimado REAL,
            valorTotalHomologado REAL,
            orgaoEntidade.cnpj TEXT NOT NULL,
            orgaoEntidade.razaoSocial TEXT NOT NULL,
            orgaoEntidade.esferaId TEXT NOT NULL,
            situacaoCompraNome TEXT NOT NULL,
            modalidadeNome TEXT NOT NULL,);
                                ''')

    def inserir_licitacoes(self, df):
        if utils.empty(df):
            print("Sem dados para o banco")
        else:
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
                    df[col] = df[col].astype(str)
            df.to_sql("licitacoes", self.conectar, if_exists="replace", index=False)
            self.conectar.commit()

    def consultar_todas(self):
        self.cursor.execute("SELECT * FROM licitacoes")
        result = self.cursor.fetchall()
        return result

    def consultar_top_licitacoes(self): # Top 10 Licitacoes decrescente por valor estimado
        self.cursor.execute(
            '''
            SELECT processo,"unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome"  FROM licitacoes order by valorTotalEstimado DESC LIMIT 10 ;
            ''')
        result = self.cursor.fetchall()
        return result

    def consultar_top_orgaos(self): # Top 10 Órgãos decrescente por valor estimado
        self.cursor.execute(
            '''
            SELECT processo,"unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome" FROM licitacoes GROUP BY "unidadeOrgao.nomeUnidade" order by valorTotalEstimado DESC LIMIT 10 ;
            ''')
        result = self.cursor.fetchall()
        return result

    def consultar_por_municipio(self, municipio):
        self.cursor.execute(
            '''
            SELECT "unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome" FROM licitacoes WHERE "unidadeOrgao.municipioNome" = ?;
            '''), (municipio,)
        result = self.cursor.fetchall()
        return result

    def municipios_disponiveis(self):
        self.cursor.execute(
            '''
            SELECT DISTINCT "unidadeOrgao.municipioNome" FROM licitacoes;
            ''')
        result = self.cursor.fetchall()
        return result