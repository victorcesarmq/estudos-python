# estudos-python

Registro da minha evolução em Python — da lógica básica a projetos aplicados em dados.

---

## Estrutura

```
fundamentos/          → exercícios e scripts de estudo
hackerrank/           → desafios da plataforma
projetos/
  ├── sistema-banco-multiconta/   → sistema bancário com múltiplas contas e persistência
  ├── sistema-de-ocorrencias/     → registro e análise de ocorrências com pandas
  ├── Projeto_API_BCB/            → analisador de indicadores econômicos via API do BCB
  └── analisador-pncp/            → análise de licitações públicas (em desenvolvimento)
```

---

## Projetos

### Sistema Bancário Multi-Conta
Sistema em linha de comando com múltiplas contas por CPF, operações de depósito, saque e transferência, extrato com histórico e persistência automática em JSON.

`OOP` `herança` `pathlib` `datetime` `json`

---

### Sistema de Registro de Ocorrências
Inspirado na operação do Programa Vigia Mais MT / SSP-MT. Cadastro de ocorrências com tipo, local, data e status. Filtros acumulativos e relatório com pandas.

`OOP` `pandas` `json` `separação de responsabilidades`

---

### Analisador de Indicadores Econômicos — BCB
Consome a API pública do Banco Central do Brasil para buscar e analisar SELIC, IPCA e câmbio (PTAX). Estatísticas descritivas, cache local e simulador de rendimento em desenvolvimento.

`requests` `pandas` `PTAX` `matplotlib` `API REST`

---

## Stack

Python 3.14 · Pandas · Matplotlib · Requests · Pathlib · JSON

---

## Status

Em desenvolvimento contínuo.
