from coletor import Coletor
from banco import Banco
from analisador import Analisador

coletor = Coletor()
banco = Banco()
analisador = Analisador()

# coletor.solicitar_parametros()
# df = coletor.coletar_todas_paginas()
# banco.inserir_licitacoes(df)
# analisador.top_licitacoes(banco.consultar_top_licitacoes())
# analisador.top_orgaos(banco.consultar_top_orgaos())
print("Municipios disponiveis:")
for municipios in banco.municipios_disponiveis():
    print(municipios)
municipio = input("Escolha um Municipio: ")
analisador.consultar_por_municipio(banco.consultar_por_municipio(municipio))