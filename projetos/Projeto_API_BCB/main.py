import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from coletor import Coletor
from analisador import Analisador

coletor = Coletor()
analisador = Analisador()

# Se nao tiver nenhum dado salvo ele manda requisicao e salva como json
coletor.coletar_dados()
analisador.carregar_dados() # aqui ele so carrega os dados como DataFrame
analisador.escolher_DataFrame()
print("==============================")
print("ANALISADOR BCB — INDICADORES")
print("==============================")
print("1. Coletar dados")
print("2. Histórico SELIC")
print("3. Histórico IPCA")
print("4. Histórico Câmbio")
print("5. Comparativo SELIC vs IPCA")
print("6. Simulador de rendimento")
print("7. Gráficos")
print("8. Exportar Excel")
print("0. Sair")
print("==============================")

while True:
    try:
        print("Escolha uma opcao:")
        opcao = int(input())
        if opcao == 1:
            coletor.coletar_dados()
        elif opcao == 2:
            print(analisador.df_selic)
        elif opcao == 3:
            print(analisador.df_ipca)
        elif opcao == 4:
            print(analisador.df_cambio)
        elif opcao == 5:
            print("==============================")
            print("COMPARATIVO MIN-MEDIA-MAX")
            print("==============================")
            print("SELIC")
            print(f"MINIMO: {analisador.min_selic:.4f}")
            print(f"MEDIA: {analisador.media_selic:.4f}")
            print(f"MAXIMO: {analisador.max_selic:.4f}")
            print(f"Desvio padrao: {analisador.desvio_selic:.4f}")
            print("==============================")
            print("IPCA")
            print(f"MINIMO: {analisador.min_ipca:.4f}")
            print(f"MEDIA: {analisador.media_ipca:.4f}")
            print(f"MAXIMO: {analisador.max_ipca:.4f}")
            print(f"Desvio padrao: {analisador.desvio_ipca:.4f}")

        elif opcao == 6:
            print("==============================")
            print("SIMULACAO DE INVESTIMENTO")
            print("==============================")
            print("1. Simular valor em dolar")
            print("2. Simular investimento em Tesouro Selic")
            print("3. Simular inflacao poder de Compra")
        elif opcao == 7:
            pass
        elif opcao == 8:
         analisador.exportar_csv()
        elif opcao == 0:
            break
        else:
            raise ValueError
    except ValueError:
        print("Opcao invalida!")

