# pipeline-pncp

Pipeline de coleta e análise de licitações públicas de Mato Grosso via API do PNCP.

## Status

v1 (atual): Coletor + Banco em Python, Power BI (via ODBC) fazendo a análise e o dashboard.
v2 (pausada, revisão em 2026-08-08): ETL completo com Analisador + main.py + Streamlit. Código já existe, só não está em uso agora.

## Quick Start

```bash
pip install requests pandas
python main.py
```

SQLite já vem embutido no Python — sem instalação adicional.

A coleta e a carga funcionam como antes. A análise mudou de lugar: em vez do terminal, agora é o Power BI conectado no `dados/pncp.db` via ODBC (driver `sqliteodbc`, 64-bit).

## O que faz

Coleta licitações do Portal Nacional de Contratações Públicas (PNCP), persiste em banco SQLite e responde:

- Quais órgãos de MT mais licitaram e quanto gastaram
- Quais municípios concentram maior volume de contratos
- Quais as maiores licitações do período por valor estimado
- Distribuição por modalidade (Pregão, Dispensa, Concorrência)
- Valor estimado x homologado por mês (Power BI)

Sem login. Sem API key. Completamente público.

## Documentação

- [Referência da API](./docs/api.md)
- [Arquitetura e schema do banco](./docs/architecture.md)
- [Armadilhas conhecidas](./docs/pitfalls.md)
- [Decisões de arquitetura (ADRs)](./docs/adr/README.md)

## Stack

v1: Python 3.14 · Pandas · Requests · SQLite · Pathlib · Power BI (ODBC / `sqliteodbc`)
v2 (pausada): + Matplotlib · openpyxl · Streamlit
