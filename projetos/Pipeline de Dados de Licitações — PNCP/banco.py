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
            "anoCompra" INTEGER NOT NULL,
            "dataInclusao" TEXT NOT NULL,
            "dataPublicacaoPncp" TEXT NOT NULL,
            "dataAtualizacao" TEXT NOT NULL,
            "dataAberturaProposta" TEXT NOT NULL,
            "dataEncerramentoProposta" TEXT NOT NULL,
            "objetoCompra" TEXT NOT NULL,
            "valorTotalEstimado" REAL,
            "valorTotalHomologado" REAL,
            "orgaoEntidade.cnpj" TEXT NOT NULL,
            "orgaoEntidade.razaoSocial" TEXT NOT NULL,
            "orgaoEntidade.esferaId" TEXT NOT NULL,
            "situacaoCompraNome" TEXT NOT NULL,
            "modalidadeNome" TEXT NOT NULL);
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
            SELECT processo,"unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome"
            FROM licitacoes
            order by valorTotalEstimado
            DESC LIMIT 10;
            ''')
        result = self.cursor.fetchall()
        return result

    def consultar_top_orgaos(self): # Top 10 Órgãos decrescente por valor estimado
        self.cursor.execute(
            '''
            SELECT processo,"unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome" 
            FROM licitacoes 
            GROUP BY "unidadeOrgao.nomeUnidade" 
            order by valorTotalEstimado 
            DESC LIMIT 10 ;
            ''')
        result = self.cursor.fetchall()
        return result

    def consultar_por_municipio(self): # Consultar por Municipio
        self.imprimir_municipios_disponiveis()
        try:
            municipio = input("Escolha um Municipio: ")
            if municipio.replace(" ", "").isalpha():
                self.cursor.execute(
                    '''
                    SELECT "unidadeOrgao.nomeUnidade",valorTotalEstimado,valorTotalHomologado,"unidadeOrgao.municipioNome" 
                    FROM licitacoes 
                    WHERE "unidadeOrgao.municipioNome" = ? AND valorTotalEstimado != 0 AND valorTotalHomologado != 0
                    order by valorTotalEstimado DESC;
                    ''',
                    (municipio,)
                )
                result = self.cursor.fetchall()
                return result
            else:
                raise ValueError("Município inválido. Por favor, insira apenas letras e espacos.")
        except ValueError as e:
            print(e)


    def buscar_municipios_disponiveis(self) -> list:
        self.cursor.execute(
            '''
            SELECT DISTINCT "unidadeOrgao.municipioNome" 
            FROM licitacoes
            ;
            ''')
        result = self.cursor.fetchall()
        lista_municipios = [i[0] for i in result]
        return lista_municipios

    def imprimir_municipios_disponiveis(self):
        lista_municipios = self.buscar_municipios_disponiveis()
        for indice in range(0, len(lista_municipios), 8):
            pedaco = lista_municipios[indice:indice + 8]
            pedaco = [f"{item:<29}" for item in pedaco]
            print(" ".join(pedaco))