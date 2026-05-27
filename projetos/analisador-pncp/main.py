import requests

url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
params = {
    "dataInicial": "20260101",
    "dataFinal": "20260131",
    "codigoModalidadeContratacao": 6,
    "uf": "MT",
    "tamanhoPagina": 10,
    "pagina": 1
}

r = requests.get(url, params=params, timeout=10)
print(r.status_code)
print(r.text)
print(r.json())