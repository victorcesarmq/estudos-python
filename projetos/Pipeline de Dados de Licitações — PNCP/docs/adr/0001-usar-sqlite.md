# ADR-001: Usar SQLite em vez de JSON para persistência

## Status
Accepted

## Context
O projeto anterior (BCB) usava JSON local para cache. Com o PNCP, uma coleta de 29 dias já retorna cerca de 29 mil licitações. Carregar esse volume inteiro em memória a cada consulta é ineficiente, e filtrar com pandas puro fica lento à medida que o volume cresce.

## Decision
Persistir os dados coletados em um banco SQLite (`pncp.db`) em vez de arquivo JSON, e usar SQL real (`pd.read_sql`) para consultas.

## Consequences
**Positivo:**
- Consultas rápidas sem carregar todo o dataset na memória
- SQL permite filtros e agregações complexas sem código Python adicional
- O banco persiste entre execuções sem precisar recarregar da API
- Prepara a migração futura para Streamlit, que conecta diretamente em SQLite

**Negativo:**
- Adiciona uma classe (`Banco`) e uma dependência conceitual nova (SQL) ao projeto
- Leve aumento de complexidade inicial comparado a só salvar um JSON
