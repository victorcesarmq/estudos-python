# Armadilhas conhecidas

| # | Problema | Solução |
|---|---|---|
| 1 | `codigoModalidadeContratacao` obrigatório | Sempre incluir — sem ele a API retorna 400 |
| 2 | `valorTotalEstimado` pode ser `None` ou `0` | `dropna()` + filtrar `> 0` antes de ordenar |
| 3 | JSON aninhado quebra o `to_sql()` | Usar `pd.json_normalize()` antes de inserir no banco |
| 4 | API instável — timeout frequente | `timeout=30`, `try/except requests.RequestException` |
| 5 | Rate limiting com muitas requisições | `time.sleep(0.5)` entre páginas |
| 6 | Dados duplicados entre páginas | `drop_duplicates(subset=["numeroControlePNCP"])` |
| 7 | Status 204 ≠ erro | Tratar separado do 400/500 — significa "sem resultados" |
| 8 | Colunas com listas quebram `to_sql()` | Converter listas restantes com `astype(str)` antes de inserir |

## Melhorias futuras

- [ ] Filtro por palavra-chave no objeto da compra (ex: "câmera", "CFTV", "TI")
- [ ] Comparativo entre modalidades (Pregão vs Dispensa)
- [ ] Comparativo entre períodos (mês a mês)
- [ ] Consultar contratos via endpoint `/v1/contratos`
- [ ] Dashboard web com Streamlit (banco SQLite já pronto para conectar)
- [ ] Agendamento de coleta mensal automática
