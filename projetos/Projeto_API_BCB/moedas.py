import requests
import pandas as pd

url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json"

r = requests.get(url)
dadosJson = r.json()
df_dados = pd.DataFrame(dadosJson["value"])
print(df_dados.to_string(index=False))
df_dados.to_json(
    "dadosmoedas.json",
    orient="records",
    force_ascii=False,
    indent=4
)

{'@odata.context': 'https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#_CotacaoDolarPeriodo', 'value': [{'cotacaoCompra': 4.0207, 'cotacaoVenda': 4.0213, 'dataHoraCotacao': '2020-01-02 13:11:10.762'}, {'cotacaoCompra': 4.0516, 'cotacaoVenda': 4.0522, 'dataHoraCotacao': '2020-01-03 13:06:22.606'}, {'cotacaoCompra': 4.0548, 'cotacaoVenda': 4.0554, 'dataHoraCotacao': '2020-01-06 13:03:22.271'}, {'cotacaoCompra': 4.0835, 'cotacaoVenda': 4.0841, 'dataHoraCotacao': '2020-01-07 13:06:14.601'}, {'cotacaoCompra': 4.0666, 'cotacaoVenda': 4.0672, 'dataHoraCotacao': '2020-01-08 13:03:56.075'}, {'cotacaoCompra': 4.0738, 'cotacaoVenda': 4.0744, 'dataHoraCotacao': '2020-01-09 13:03:52.663'}, {'cotacaoCompra': 4.0739, 'cotacaoVenda': 4.0745, 'dataHoraCotacao': '2020-01-10 13:10:19.927'}]}