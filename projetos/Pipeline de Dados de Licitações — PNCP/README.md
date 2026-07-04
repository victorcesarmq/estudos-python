# pipeline-pncp

Pipeline de coleta e análise de licitações públicas de Mato Grosso via API do PNCP.

## Quick Start

```bash
pip install requests pandas matplotlib openpyxl
python main.py
```

SQLite já vem embutido no Python — sem instalação adicional.

Na primeira execução o sistema pede o período e coleta os dados. Nas seguintes, carrega do banco local.

## O que faz

Coleta licitações do Portal Nacional de Contratações Públicas (PNCP), persiste em banco SQLite e responde:

- Quais órgãos de MT mais licitaram e quanto gastaram
- Quais municípios concentram maior volume de contratos
- Quais as maiores licitações do período por valor estimado
- Distribuição por modalidade (Pregão, Dispensa, Concorrência)

Sem login. Sem API key. Completamente público.

## Documentação

- [Referência da API](./docs/api.md)
- [Arquitetura e schema do banco](./docs/architecture.md)
- [Armadilhas conhecidas](./docs/pitfalls.md)
- [Decisões de arquitetura (ADRs)](./docs/adr/README.md)

## Stack

Python 3.14 · Pandas · Matplotlib · Requests · SQLite · Pathlib
