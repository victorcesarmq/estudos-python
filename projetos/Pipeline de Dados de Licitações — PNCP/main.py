from coletor import Coletor
from banco import Banco

coletor = Coletor()
banco = Banco()
coletor.solicitar_parametros()
df = coletor.coletar_todas_paginas
banco.inserir_licitacoes(df)