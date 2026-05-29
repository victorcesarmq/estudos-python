from coletor import Coletor
from analisador import Analisador
import pandas as pd
import matplotlib.pyplot as plt

coletor = Coletor()
analisador = Analisador()

# INICIO agora vai
coletor.coletar_dados()

# Carrega os JSONs em DataFrames
analisador.carregar_dados()

while True:

    print("==============================")
    print("ANALISADOR BCB — INDICADORES")
    print("==============================")
    print("1. Coletar dados")
    print("2. Histórico SELIC")
    print("3. Histórico IPCA")
    print("4. Histórico Câmbio")
    print("5. Comparativo SELIC vs IPCA")
    print("6. Simulador de rendimento")
    print("7. Filtrar período - MIN/MEDIA/MAX")
    print("8. Exportar CSV")
    print("0. Sair")
    print("==============================")

    try:

        opcao = int(input("Escolha uma opcao: "))

        # COLETAR NOVOS DADOS
        if opcao == 1:

            coletor.coletar_dados()
            # Recarrega os dados atualizados
            analisador.carregar_dados()

        # HISTORICO SELIC
        elif opcao == 2:
            plt.style.use("seaborn-v0_8-darkgrid")
            plt.plot(analisador.df_selic_filtrado["data"], analisador.df_selic_filtrado["valor"])
            plt.title("SELIC — Taxa Diária")
            plt.xlabel("Data")
            plt.ylabel("Taxa (%)")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

        # HISTORICO IPCA
        elif opcao == 3:
            plt.style.use("seaborn-v0_8-darkgrid")
            plt.plot(analisador.df_ipca_filtrado["data"], analisador.df_ipca_filtrado["valor"])
            plt.title("IPCA — Taxa Diária")
            plt.xlabel("Data")
            plt.ylabel("Taxa (%)")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

        # HISTORICO CÂMBIO
        elif opcao == 4:
            plt.style.use("seaborn-v0_8-darkgrid")
            plt.plot(analisador.df_cambio_filtrado["dataHoraCotacao"], analisador.df_cambio_filtrado["cotacaoCompra"], label="Compra", color="steelblue")
            plt.plot(analisador.df_cambio_filtrado["dataHoraCotacao"], analisador.df_cambio_filtrado["cotacaoVenda"], label="Venda", color="tomato")
            plt.legend()
            plt.title("Taxa de Cambio Compra/Venda")
            plt.xlabel("Data")
            plt.ylabel("Taxa (%)")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

        # COMPARATIVO
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

        # SIMULADOR
        elif opcao == 6:

            print("==============================")
            print("SIMULACAO DE INVESTIMENTO")
            print("==============================")

            print("1. Simular valor em dolar")
            print("2. Simular investimento em Tesouro Selic")
            print("3. Simular inflacao poder de Compra")

            opcao_investimento = input("Opcao: ")

            # DOLLAR
            if opcao_investimento == "1":
                print("1. Cotacao de um dia especifico")
                print("2. Media de um periodo")

                tipo_consulta = input("Opcao: ")

                quantidade_em_reais = float(input("Digite a quantidade em Reais: "))

                print("Deseja vender ou comprar dollar?")
                print("1. Vender")
                print("2. Comprar")

                escolher_transacao = input("Opcao: ")

                # COTAÇÃO DE UM DIA
                if tipo_consulta == "1":
                    print(f"Entre {coletor.dataInicial} - {coletor.dataFinal}")
                    data_escolhida = input("Digite a data (DD/MM/AAAA): ")

                    data_escolhida = pd.to_datetime(data_escolhida, format="%d/%m/%Y")

                    # Cria coluna apenas com a data
                    analisador.df_cambio_filtrado["data"] = analisador.df_cambio_filtrado["dataHoraCotacao"].dt.date

                    df_filtrado = analisador.df_cambio_filtrado[analisador.df_cambio_filtrado["data"] == data_escolhida.date()]

                    # Verifica se encontrou cotação
                    if df_filtrado.empty:
                        print("Nenhuma cotacao encontrada para essa data!")

                    else:
                        # Usa a ultima cotação do dia
                        cotacao = df_filtrado.iloc[-1]
                        if escolher_transacao == "1":
                            retorno_em_dollar = quantidade_em_reais / cotacao["cotacaoVenda"]

                            print(f"Cotacao na data da venda: {cotacao['cotacaoVenda']:.4f}")
                            print(f"Valor aproximado em dollar: {retorno_em_dollar:.2f}")

                        elif escolher_transacao == "2":
                            retorno_em_dollar = quantidade_em_reais / cotacao["cotacaoCompra"]

                            print(f"Cotacao na data da compraompra: {cotacao['cotacaoCompra']:.4f}")
                            print(f"Valor aproximado em dollar: {retorno_em_dollar:.2f}")

                        else:
                            print("Opcao invalida!")


                # MÉDIA DE UM PERIODO
                elif tipo_consulta == "2":
                    print("Formato DIA/MES/ANO")
                    print("Ex: 31/01/2024")
                    print(f"Entre {coletor.dataInicial} - {coletor.dataFinal}")
                    dataInicial = input("Digite a data inicial: ")
                    dataFinal = input("Digite a data final: ")

                    dataInicial = pd.to_datetime(dataInicial, format="%d/%m/%Y")
                    dataFinal = pd.to_datetime(dataFinal, format="%d/%m/%Y")

                    df_filtrado = analisador.df_cambio_filtrado[(analisador.df_cambio_filtrado["dataHoraCotacao"] >= dataInicial) & (analisador.df_cambio_filtrado["dataHoraCotacao"] <= dataFinal)]

                    # Verifica se encontrou dados
                    if df_filtrado.empty:
                        print("Nenhuma cotacao encontrada nesse periodo!")

                    else:
                        if escolher_transacao == "1":
                            cotacao_media = df_filtrado["cotacaoVenda"].mean()

                            retorno_em_dollar = quantidade_em_reais / cotacao_media

                            print(f"Cotacao media de venda: {cotacao_media:.4f}")
                            print(f"Valor aproximado em dollar: {retorno_em_dollar:.2f}")

                        elif escolher_transacao == "2":
                            cotacao_media = df_filtrado["cotacaoCompra"].mean()

                            retorno_em_dollar = quantidade_em_reais / cotacao_media

                            print(f"Cotacao media de compra: {cotacao_media:.4f}")
                            print(f"Valor aproximado em dollar: {retorno_em_dollar:.2f}")

                        else:
                            print("Opcao invalida!")
                else:
                    print("Opcao invalida!")
            elif opcao_investimento == "2":
                print(f"Filtrando entre {coletor.dataInicial} - {coletor.dataFinal}")
                print("Para escolher outra data volte ao menu inicial e escolha a opcao 1")
                quantidade_em_reais = int(input("Digite o valor inicial em R$: "))


                #Calculo de juros compostos
                fatores = 1 + (analisador.df_selic_filtrado["valor"] / 100)
                fator_acumulado = fatores.prod()
                valor_final = quantidade_em_reais * fator_acumulado
                rendimento = valor_final - quantidade_em_reais

                print(f"Valor final: R${valor_final:.2f}")
                print(f"Rendimento: R${rendimento:.2f}")
            elif opcao_investimento == "3":
                print(f"Filtrando entre {coletor.dataInicial} - {coletor.dataFinal}")
                print("Para escolher outra data volte ao menu inicial e escolha a opcao 1")
                quantidade_em_reais = int(input("Digite o valor inicial em R$: "))

                # Calculo de inflacao
                fatores = 1 + (analisador.df_ipca_filtrado["valor"] / 100)
                fator_acumulado = fatores.prod()
                valor_final = quantidade_em_reais / fator_acumulado
                rendimento = valor_final - quantidade_em_reais

                print(f"Poder Final de compra: R${valor_final:.2f}")
                print(f"Quantidade corroida pela inflacao: R${abs(rendimento):.2f}")


        # FILTRAR PERIODO
        elif opcao == 7:
            print("Formato DIA/MES/ANO")
            print(f"Entre {coletor.dataInicial} - {coletor.dataFinal}")
            dataInicial = input("Digite a data Inicial: ")
            dataFinal = input("Digite a data Final: ")

            analisador.filtrar_periodo(dataInicial, dataFinal)

        # EXPORTAR CSV
        elif opcao == 8:
            analisador.exportar_csv()
        # SAIR
        elif opcao == 0:
            break
        else:
            raise ValueError
    except ValueError:

        print("Opcao invalida!")