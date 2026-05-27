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

