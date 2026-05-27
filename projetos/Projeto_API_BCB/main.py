from coletor import Coletor
from analisador import Analisar

coletor = Coletor()
analisar = Analisar()

# Se nao tiver nenhum dado salvo ele manda requisicao e salva como json
coletor.coletar_dados()
analisar.carregar_dados() # aqui ele so carrega os dados como DataFrame
analisar.escolher_DataFrame()
analisar.visualizador()
analisar.exportar_csv()