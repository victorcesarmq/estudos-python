# pipeline-pncp

Pipeline de coleta e análise de licitações públicas de Mato Grosso via API do PNCP.

---

## O que faz

Coleta licitações do Portal Nacional de Contratações Públicas (PNCP), persiste em banco SQLite e responde perguntas de inteligência de mercado e fiscalização:

- Quais órgãos de MT mais licitaram e quanto gastaram
- Quais municípios concentram maior volume de contratos
- Quais as maiores licitações do período por valor estimado
- Distribuição por modalidade (Pregão, Dispensa, Concorrência)

Sem login. Sem API key. Completamente público.

---

## Quick Start

```bash
pip install requests pandas matplotlib openpyxl
python main.py
```

SQLite já vem embutido no Python — sem instalação adicional.

Na primeira execução o sistema pede o período e coleta os dados. Nas seguintes, carrega do banco local.

---

## Estrutura

```
pipeline-pncp/
├── main.py          → menu principal e fluxo
├── coletor.py       → coleta via API + paginação
├── banco.py         → CRUD com SQLite
├── analisador.py    → consultas SQL + pandas + exportação
└── dados/
    └── pncp.db      → banco SQLite
```

---

## API

**Endpoint:**
```
GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao
```

**Parâmetros obrigatórios:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `dataInicial` | string | Formato `AAAAMMDD` |
| `dataFinal` | string | Formato `AAAAMMDD` |
| `codigoModalidadeContratacao` | int | Ver tabela de modalidades |
| `pagina` | int | Número da página (começa em 1) |

**Parâmetros opcionais:**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `uf` | string | Sigla do estado (ex: `MT`) |
| `tamanhoPagina` | int | Mínimo 10, máximo 500 |

**Resposta:**

```json
{
    "data": [ {...}, {...} ],
    "totalRegistros": 392,
    "totalPaginas": 40,
    "numeroPagina": 1,
    "paginasRestantes": 39,
    "empty": false
}
```

**Códigos de status:**

| Código | Significado |
|---|---|
| 200 | Sucesso |
| 204 | Sucesso — sem dados para esse filtro |
| 400 | Parâmetro inválido ou obrigatório faltando |
| 422 | Entidade não processável |
| 500 | Erro no servidor |

**Modalidades disponíveis:**

| Código | Modalidade |
|---|---|
| 1 | Leilão Eletrônico |
| 4 | Concorrência Eletrônica |
| 6 | Pregão Eletrônico ← mais comum |
| 8 | Dispensa de Licitação |
| 9 | Inexigibilidade |

---

## Arquitetura

### Fluxo de dados

```
API PNCP → Coletor → pd.json_normalize() → Banco (SQLite) → Analisador → Output
```

### Diagrama de classes

```
Coletor                     Banco                      Analisador
───────────────────         ──────────────────────     ───────────────────────
solicitar_parametros()      inserir_licitacoes(df)     carregar_dados()
params_url()                consultar_todas()           resumo_por_modalidade()
coletar_todas_paginas()     consultar_top_orgaos(n)    top_orgaos(n)
                            consultar_top_valores(n)   maiores_valores(n)
                            consultar_por_municipio()  exportar_csv()
                            contar_registros()         exportar_excel()
```

### Paginação

A API limita 50 registros por requisição. O loop usa `paginasRestantes` da resposta:

```
Requisição página 1 → paginasRestantes: 39
Requisição página 2 → paginasRestantes: 38
...
Requisição página 40 → paginasRestantes: 0 → break
```

### Normalização do JSON

Os dados chegam com dicionários aninhados (`orgaoEntidade`, `unidadeOrgao`). O `pd.json_normalize()` os achata em colunas:

```
orgaoEntidade.razaoSocial  →  orgaoEntidade_razaoSocial
unidadeOrgao.municipioNome →  unidadeOrgao_municipioNome
```

---

## Banco de dados

**Schema da tabela principal:**

```sql
CREATE TABLE IF NOT EXISTS licitacoes (
    numeroControlePNCP TEXT PRIMARY KEY,
    modalidadeNome TEXT,
    objetoCompra TEXT,
    valorTotalEstimado REAL,
    valorTotalHomologado REAL,
    dataPublicacaoPncp TEXT,
    orgaoEntidade_razaoSocial TEXT,
    unidadeOrgao_municipioNome TEXT,
    unidadeOrgao_ufSigla TEXT,
    situacaoCompraNome TEXT
);
```

**Consultas SQL utilizadas:**

```sql
-- Top 10 órgãos que mais licitaram
SELECT orgaoEntidade_razaoSocial, COUNT(*) as total, SUM(valorTotalEstimado) as valor_total
FROM licitacoes
GROUP BY orgaoEntidade_razaoSocial
ORDER BY total DESC
LIMIT 10;

-- Maiores valores por licitação
SELECT objetoCompra, valorTotalEstimado, orgaoEntidade_razaoSocial
FROM licitacoes
WHERE valorTotalEstimado > 0
ORDER BY valorTotalEstimado DESC
LIMIT 10;

-- Distribuição por município
SELECT unidadeOrgao_municipioNome, COUNT(*) as total
FROM licitacoes
GROUP BY unidadeOrgao_municipioNome
ORDER BY total DESC;

-- Filtro por período
SELECT * FROM licitacoes
WHERE dataPublicacaoPncp BETWEEN '2025-01-01' AND '2025-06-30';
```

---

## Decisões de arquitetura

### ADR-001: SQLite em vez de JSON

**Status:** Aceito

**Contexto:** O projeto BCB anterior usava JSON local. Com 29 mil licitações por mês, carregar tudo em memória é inviável e filtrar com pandas é ineficiente.

**Decisão:** Persistir em SQLite e consultar via SQL.

**Consequências:**
- Positivo: consultas rápidas sem carregar tudo na memória; SQL para filtros complexos; prepara para migração ao Streamlit.
- Negativo: adiciona a classe `Banco` ao projeto; leve aumento de complexidade inicial.

---

### ADR-002: `pd.json_normalize()` em vez de `pd.DataFrame()` direto

**Status:** Aceito

**Contexto:** A API retorna campos aninhados (`orgaoEntidade`, `unidadeOrgao`) que o SQLite não aceita como dicionários.

**Decisão:** Usar `pd.json_normalize()` para achatar antes de inserir no banco.

**Consequências:**
- Positivo: todos os campos ficam acessíveis como colunas; sem necessidade de converter manualmente.
- Negativo: nomes de colunas ficam longos (`orgaoEntidade_razaoSocial`).

---

### ADR-003: Responsabilidade separada entre Coletor e Banco

**Status:** Aceito

**Contexto:** Versão inicial do Banco chamava o Coletor internamente, acoplando coleta e persistência.

**Decisão:** O `main.py` orquestra — Coletor coleta e retorna DataFrame, Banco recebe DataFrame e persiste.

**Consequências:**
- Positivo: cada classe faz uma coisa; mais fácil testar e substituir.
- Negativo: o `main.py` precisa conhecer ambas as classes.

---

## Armadilhas conhecidas

| # | Problema | Solução |
|---|---|---|
| 1 | `codigoModalidadeContratacao` obrigatório | Sempre incluir — sem ele retorna 400 |
| 2 | `valorTotalEstimado` pode ser `None` ou `0` | `dropna()` + filtrar `> 0` antes de ordenar |
| 3 | JSON aninhado quebra o `to_sql()` | Usar `pd.json_normalize()` antes de inserir |
| 4 | API instável — timeout frequente | `timeout=30`, `try/except RequestException` |
| 5 | Rate limiting com muitas requisições | `time.sleep(0.5)` entre páginas |
| 6 | Dados duplicados entre páginas | `drop_duplicates(subset=["numeroControlePNCP"])` |
| 7 | Status 204 ≠ erro | Tratar separado do 400/500 |
| 8 | Colunas com listas quebram `to_sql()` | Converter listas restantes com `astype(str)` |

---

## Stack

Python 3.14 · Pandas · Matplotlib · Requests · SQLite · Pathlib

---

## Melhorias futuras

- [ ] Filtro por palavra-chave no objeto da compra (ex: "câmera", "CFTV", "TI")
- [ ] Comparativo entre modalidades (Pregão vs Dispensa)
- [ ] Comparativo entre períodos (mês a mês)
- [ ] Consultar contratos via endpoint `/v1/contratos`
- [ ] Dashboard web com Streamlit (banco SQLite já pronto para conectar)
- [ ] Agendamento de coleta mensal automática
