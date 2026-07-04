# ADR-003: Separar responsabilidade entre Coletor e Banco

## Status
Accepted

## Context
Numa versão inicial, a classe `Banco` instanciava e chamava o `Coletor` internamente dentro de `inserir_licitacoes()`. Isso acoplava coleta e persistência na mesma classe, dificultando testar ou substituir qualquer uma das duas partes isoladamente.

## Decision
O `Coletor` apenas coleta e retorna um DataFrame. O `Banco` apenas recebe um DataFrame e persiste. A orquestração entre os dois acontece no `main.py`, não dentro das classes.

## Consequences
**Positivo:**
- Cada classe tem uma única responsabilidade
- `Coletor` pode ser testado sem precisar de banco
- `Banco` pode receber dados de qualquer fonte, não só do `Coletor`

**Negativo:**
- O `main.py` precisa conhecer e orquestrar ambas as classes explicitamente
