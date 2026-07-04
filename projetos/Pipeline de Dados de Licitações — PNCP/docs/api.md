# API Reference — PNCP

## Endpoint

```
GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao
```

## Request

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

**Exemplo:**

```python
import requests

url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
params = {
    "dataInicial": "20260101",
    "dataFinal": "20260131",
    "codigoModalidadeContratacao": 6,
    "uf": "MT",
    "tamanhoPagina": 50,
    "pagina": 1
}

r = requests.get(url, params=params, timeout=30)
```

## Response

**200 OK**

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

**Campos de controle de paginação:**

| Campo | Descrição |
|---|---|
| `totalRegistros` | Total de registros encontrados |
| `totalPaginas` | Total de páginas necessárias |
| `numeroPagina` | Página atual |
| `paginasRestantes` | Quantas páginas ainda faltam |
| `empty` | `true` se não há dados |

**Item de `data`:**

```json
{
    "numeroControlePNCP": "26989715000102-1-002674/2025",
    "modalidadeId": 6,
    "modalidadeNome": "Pregão - Eletrônico",
    "situacaoCompraNome": "Divulgada no PNCP",
    "objetoCompra": "Aquisição de materiais de limpeza",
    "valorTotalEstimado": 150000.00,
    "valorTotalHomologado": 148000.00,
    "dataPublicacaoPncp": "2026-01-15",
    "orgaoEntidade": {
        "cnpj": "...",
        "razaoSocial": "..."
    },
    "unidadeOrgao": {
        "municipioNome": "...",
        "ufSigla": "MT"
    }
}
```

**Campos mais úteis para análise:**

- `modalidadeNome` — tipo de licitação
- `orgaoEntidade.razaoSocial` — nome do órgão
- `valorTotalEstimado` — valor estimado em R$
- `valorTotalHomologado` — valor final homologado
- `objetoCompra` — o que está sendo comprado
- `unidadeOrgao.municipioNome` — município
- `situacaoCompraNome` — situação (Divulgada, Revogada, Anulada, Suspensa)

## Errors

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 204 | Sucesso — sem dados para esse filtro |
| 400 | Parâmetro inválido ou obrigatório faltando (ex: `codigoModalidadeContratacao` ausente) |
| 422 | Entidade não processável |
| 500 | Erro no servidor |

## Modalidades disponíveis

| Código | Modalidade |
|---|---|
| 1 | Leilão Eletrônico |
| 4 | Concorrência Eletrônica |
| 6 | Pregão Eletrônico ← mais comum |
| 8 | Dispensa de Licitação |
| 9 | Inexigibilidade |
