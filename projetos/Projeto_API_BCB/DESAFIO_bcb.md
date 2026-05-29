# 📊 Desafio — Analisador de Indicadores Econômicos (Banco Central do Brasil)

> **Pré-requisitos:**
> ```bash
> pip install requests pandas matplotlib
> ```

---

## 📋 Sobre o Projeto

Sistema que consome a **API pública do Banco Central do Brasil** para buscar, comparar e analisar três indicadores econômicos:

- **SELIC** — taxa básica de juros (via SGS, código 11)
- **IPCA** — índice oficial de inflação (via SGS, código 433)
- **Câmbio USD/BRL** — cotação do dólar compra/venda (via PTAX)

Sem login. Sem API key. Completamente público.

---

## 🌐 APIs Utilizadas

### SGS (SELIC e IPCA)
```
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{CODIGO}/dados?formato=json&dataInicial={dd/MM/yyyy}&dataFinal={dd/MM/yyyy}
```

| Código | Indicador | Periodicidade |
|---|---|---|
| 11 | SELIC diária | Diária |
| 433 | IPCA | Mensal |

Resposta: `[{"data": "02/01/2024", "valor": "0.04556"}, ...]`

### PTAX (Câmbio)
```
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='{MM-DD-YYYY}',dataFinalCotacao='{MM-DD-YYYY}')?$format=json
```

Resposta: `{"value": [{"cotacaoCompra": 4.95, "cotacaoVenda": 4.96, "dataHoraCotacao": "2024-01-02 13:11:10"}, ...]}`

**Atenção:** PTAX usa formato `MM-DD-YYYY` e o parâmetro final é `dataFinalCotacao`, não `dataFinal`.

---

## 🗂️ Estrutura do Projeto

```
Projeto_API_BCB/
├── main.py          # Menu principal e fluxo
├── coletor.py       # Classe Coletor — requisições + cache
├── analisador.py    # Classe Analisador — estatísticas + filtro + exportação
└── dados/
    ├── dados_selic.json
    ├── dados_ipca.json
    └── dados_cambio.json
```

---

## 🧱 As Classes

### `Coletor`
Responsável por buscar os dados das APIs e salvar localmente.

```
Métodos:
- verificar_cache()              → verifica se já existem dados salvos
- carregar_periodo_existente()   → lê datas do cache existente via iloc
- mostrar_menu()                 → exibe opções (usar cache ou novo período)
- solicitar_datas()              → pede datas ao usuário
- converter_datas_ptax()         → converte DD/MM/YYYY → MM-DD-YYYY
- montar_urls()                  → monta URLs das 3 APIs
- montar_parametros()            → monta dict de parâmetros do SGS
- tratar_dataframe_taxa()        → converte valor e data (SELIC/IPCA)
- salvar_json()                  → salva DataFrame em JSON
- baixar_selic/ipca/cambio()     → GET + tratamento + salvar
- coletar_dados()                → função principal — orquestra tudo
```

### `Analisador`
Carrega JSONs, calcula estatísticas, filtra período e exporta.

```
Métodos:
- carregar_dados()           → lê os 3 JSONs e cria DataFrames
- calcular_estatisticas()    → média, min, max, desvio dos 3 indicadores
- escolher_DataFrame()       → menu de seleção de indicador
- filtrar_periodo()          → filtra DataFrames por data e recalcula estatísticas
- exportar_csv()             → exporta os 3 indicadores filtrados em CSV
```

---

## ⚙️ Funcionalidades

```
[x] Coletar SELIC, IPCA e câmbio para um período informado
[x] Salvar em JSON local (cache)
[x] Carregar do cache sem buscar da API de novo
[x] Menu de escolha: usar cache ou novo período
[x] Histórico visual com matplotlib (SELIC, IPCA, câmbio)
[x] Comparativo SELIC vs IPCA (min, média, max, desvio)
[x] Simulador de rendimento Tesouro Selic (juros compostos)
[x] Simulador de perda de poder de compra (IPCA)
[x] Conversor de câmbio (cotação do dia ou média do período)
[x] Filtro de período com recálculo de estatísticas
[x] Exportar para CSV
[ ] Exportar para Excel (.xlsx) com múltiplas abas
```

---

## 💡 Menu Implementado

```
==============================
ANALISADOR BCB — INDICADORES
==============================
1. Coletar dados
2. Histórico SELIC (gráfico)
3. Histórico IPCA (gráfico)
4. Histórico Câmbio (gráfico compra/venda)
5. Comparativo SELIC vs IPCA
6. Simulador de rendimento
   ├── 1. Simular valor em dólar
   ├── 2. Simular Tesouro Selic
   └── 3. Simular inflação poder de compra
7. Filtrar período - MIN/MEDIA/MAX
8. Exportar CSV
0. Sair
==============================
```

---

## 💰 Lógicas de Simulação

### Tesouro Selic (juros compostos diários)
```python
fatores = 1 + (df_selic["valor"] / 100)
fator_acumulado = fatores.prod()
valor_final = valor_inicial * fator_acumulado
```

### Inflação — perda de poder de compra
```python
fatores = 1 + (df_ipca["valor"] / 100)
fator_acumulado = fatores.prod()
valor_final = valor_inicial / fator_acumulado
```

### Câmbio — conversão por cotação do dia ou média
```python
# Cotação do dia
retorno_em_dollar = quantidade_em_reais / cotacao["cotacaoVenda"]

# Média do período
cotacao_media = df_filtrado["cotacaoCompra"].mean()
retorno_em_dollar = quantidade_em_reais / cotacao_media
```

---

## 🪤 Armadilhas Encontradas

1. **`valor` chega como string** — sempre converter com `pd.to_numeric()` ou `.str.replace(",", ".")`
2. **PTAX usa `MM-DD-YYYY`** — converter com `dt.datetime.strptime().strftime()`
3. **PTAX resposta em `["value"]`** — acessar `r.json()["value"]`, não `r.json()` direto
4. **`to_json()` retorna None** — nunca fazer `df = df.to_json(...)`, isso destrói o DataFrame
5. **SGS limita 10 anos** — sempre informar `dataInicial` e `dataFinal`
6. **SELIC diária vs IPCA mensal** — periodicidades diferentes, cuidado com comparações diretas
7. **`dataFinalCotacao`** — o parâmetro PTAX para data final NÃO é `dataFinal`

---

## 🚧 Melhorias Futuras

- [ ] Exportar para Excel (.xlsx) com múltiplas abas
- [ ] Comparativo câmbio vs IPCA
- [ ] Projeção simples de inflação futura (média móvel)
- [ ] Versão com Google Cloud Storage
- [ ] Dashboard web com Flask ou Streamlit
- [ ] Expectativas de Mercado (API BCB) — comparar projeções vs realizado

---

*Projeto desenvolvido como parte da trilha de estudos em Engenharia de Dados.*