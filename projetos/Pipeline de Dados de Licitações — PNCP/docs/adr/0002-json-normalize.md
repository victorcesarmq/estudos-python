# ADR-002: Normalizar JSON aninhado com pd.json_normalize()

## Status
Accepted

## Context
A API do PNCP retorna campos aninhados como `orgaoEntidade` e `unidadeOrgao` — dicionários dentro do dicionário principal de cada licitação. O SQLite não aceita colunas do tipo dicionário ou lista; tentar inserir um DataFrame criado com `pd.DataFrame()` direto causa erro (`sqlite3.ProgrammingError: type 'dict' is not supported`).

## Decision
Usar `pd.json_normalize(dados, sep="_")` para achatar os dicionários aninhados em colunas simples antes de qualquer persistência ou análise.

## Consequences
**Positivo:**
- Todos os campos do órgão e da unidade ficam acessíveis como colunas comuns (`orgaoEntidade_razaoSocial`, `unidadeOrgao_municipioNome`)
- Elimina o erro de inserção no SQLite
- Uma única chamada resolve o achatamento, sem loop manual

**Negativo:**
- Nomes de colunas ficam mais longos e menos legíveis
- Campos que ainda restam como lista (ex: `fontesOrcamentarias`) precisam de tratamento adicional com `astype(str)`
