# ADR-004: Migrar de ETL em Python para ELT com Power BI

## Status
Accepted

## Context
O plano original (v2) era um ETL completo em Python: `Coletor` extrai, `Banco` carrega e serve consultas de negócio via SQL, `Analisador` formata e apresenta os resultados no terminal (depois Streamlit). Esse caminho gerava retrabalho de visualização (construir do zero o que uma ferramenta de BI já resolve) e não refletia a stack real usada por Analistas de Dados no mercado. Também havia saturação acumulada com o projeto sem uma versão "pronta" visível.

Antes de trocar a camada de apresentação era preciso validar se o schema do banco aguentava ser exposto externamente — os bugs conhecidos do `Banco` (`GROUP BY` com colunas não agregadas em `consultar_top_orgaos`, parâmetro solto em `consultar_por_municipio`) afetam qualquer consumidor, não só o Analisador em Python.

## Decision
Priorizar `Coletor` + `Banco` (Extract + Load) conectados ao Power BI via ODBC (`sqliteodbc`, driver "SQLite3 ODBC Driver" 64-bit) para a camada de Transform + apresentação — ELT em vez de ETL. `Analisador` e `main.py` ficam pausados, código preservado, não descartados: retomam quando o ETL completo (ou outra visualização) voltar a ser prioridade.

Teste de diagnóstico feito antes de decidir: conectar o Power BI direto no SQLite via ODBC sem corrigir nada antes, pra ver se o schema aguentava.

## Consequences
**Positivo:**
- Caminho mais curto até uma versão concluída e demonstrável.
- Alinha o projeto de portfólio com a stack real de mercado (BI) em vez de visualização customizada.
- Elimina estruturalmente uma classe de bug: o Power BI força escolher uma função de agregação (Soma/Máximo/Contagem) por coluna fora do agrupamento, o que o SQL solto do `Banco` não força — o bug de `GROUP BY` do `top_orgaos()` não se replica no Power BI.

**Negativo:**
- `Analisador`/`main.py`/Streamlit ficam sem uso ativo, mesmo com código já escrito.
- Duas versões documentadas em paralelo (v1 atual, v2 pausada) — README e `architecture.md` precisam deixar claro o que é "existe" vs "intenção" pra não confundir leitor.
- Dependência de driver ODBC externo (`sqliteodbc`) e de bitness correta (64-bit) — ponto de fricção de setup que não existiria com Analisador em Python puro.
