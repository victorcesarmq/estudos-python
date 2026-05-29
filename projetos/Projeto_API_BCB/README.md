# Analisador de Indicadores Econômicos — BCB

Sistema em Python que consome as APIs públicas do Banco Central do Brasil para análise de SELIC, IPCA e câmbio (PTAX).

---

## O que faz

- Coleta dados da SELIC (taxa diária), IPCA (inflação mensal) e câmbio USD/BRL (cotação oficial PTAX)
- Armazena em cache local — consulta a API uma vez, trabalha com os dados offline
- Exibe gráficos de evolução histórica com matplotlib
- Calcula estatísticas descritivas: média, mínimo, máximo e desvio padrão
- Simula rendimento do Tesouro Selic com juros compostos diários
- Simula perda de poder de compra pela inflação (IPCA)
- Converte valores em reais para dólar por cotação do dia ou média do período
- Filtra por período personalizado com recálculo automático de estatísticas
- Exporta dados filtrados em CSV

---

## APIs utilizadas

| API | Indicador | Endpoint |
|---|---|---|
| SGS | SELIC diária (código 11) | `api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados` |
| SGS | IPCA mensal (código 433) | `api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados` |
| PTAX | Câmbio USD/BRL | `olinda.bcb.gov.br/.../CotacaoDolarPeriodo` |

Sem autenticação. Sem API key.

---

## Estrutura

```
Projeto_API_BCB/
├── main.py          → menu e fluxo principal
├── coletor.py       → coleta via API + cache JSON
├── analisador.py    → estatísticas, filtro e exportação
└── dados/
    ├── dados_selic.json
    ├── dados_ipca.json
    └── dados_cambio.json
```

---

## Como usar

```bash
pip install requests pandas matplotlib
python main.py
```

Na primeira execução o sistema pede o período desejado e coleta os dados. Nas próximas, oferece a opção de usar o cache existente ou coletar um novo período.

---

## Stack

Python 3.14 · Pandas · Matplotlib · Requests · Pathlib · JSON

---

## Conceitos aplicados

- Consumo de APIs REST públicas do governo federal
- Tratamento de séries temporais com pandas
- Visualização de dados com matplotlib
- Juros compostos diários (simulação Tesouro Selic)
- Cálculo de inflação acumulada (IPCA)
- Cache local com persistência em JSON
- Separação de responsabilidades entre classes
- Tratamento de erros HTTP e de input
