# 📡 Desafio — Analisador de Licitações Públicas (PNCP)

> **Pré-requisitos antes de começar:**
> ```bash
> pip install requests pandas matplotlib openpyxl
> ```
> SQLite já vem embutido no Python (`import sqlite3`) — não precisa instalar.

---

## 📋 Sobre o Projeto

Sistema que consome a **API pública do Portal Nacional de Contratações Públicas (PNCP)** para buscar, filtrar e analisar licitações do estado de Mato Grosso.

Sem login. Sem credencial. A API de consulta é completamente aberta.

Você já consumiu APIs no projeto BCB (SGS + PTAX). A novidade aqui é: **JSON aninhado**, **paginação com controle de páginas**, **dados muito mais sujos** e **persistência em SQLite** — primeiro contato com banco de dados real. É o projeto que prepara a migração futura para Streamlit.

---

## 🌐 O que é uma API REST?

Uma API REST é uma forma de um programa conversar com outro pela internet.

Você faz uma **requisição HTTP** para uma URL com parâmetros, e recebe uma **resposta em JSON**. É exatamente o que acontece quando você abre um site — mas em vez de HTML, você recebe dados estruturados.

```
Você → GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao?uf=MT&pagina=1
API  → { "data": [ {...}, {...} ], "totalRegistros": 342 }
```

A biblioteca `requests` em Python faz isso em uma linha.

---

## 📦 Introdução ao `requests`

```python
import requests

url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"

parametros = {
    "dataInicial": "20260101",
    "dataFinal": "20260131",
    "uf": "MT",
    "tamanhoPagina": 50,
    "pagina": 1
}

resposta = requests.get(url, params=parametros)

print(resposta.status_code)  # 200 = sucesso
print(resposta.json())        # dicionário Python com os dados
```

**Códigos de status importantes:**
| Código | Significado |
|---|---|
| 200 | Sucesso |
| 204 | Sucesso — sem conteúdo (nenhum resultado encontrado) |
| 400 | Parâmetro inválido ou obrigatório faltando |
| 422 | Entidade não processável |
| 500 | Erro no servidor |

Sempre verifique o status antes de usar os dados:
```python
if resposta.status_code == 200:
    dados = resposta.json()
else:
    print(f"Erro: {resposta.status_code}")
```

---

## 📄 Paginação

A API retorna no máximo 50 registros por página (até 500 com `tamanhoPagina`). Para buscar tudo, você precisa paginar.

A resposta já vem com um campo `paginasRestantes` — use ele para controlar o loop:

```python
pagina = 1
todos_os_dados = []

while True:
    parametros["pagina"] = pagina
    resposta = requests.get(url, params=parametros, timeout=10)
    dados = resposta.json()

    todos_os_dados.extend(dados.get("data", []))

    if dados.get("paginasRestantes", 0) == 0:
        break  # não tem mais páginas

    pagina += 1
    time.sleep(0.5)  # evita bloquear a API
```

**Campos de controle de paginação retornados pela API:**
| Campo | Descrição |
|---|---|
| `totalRegistros` | Total de registros encontrados |
| `totalPaginas` | Total de páginas necessárias |
| `numeroPagina` | Página atual |
| `paginasRestantes` | Quantas páginas ainda faltam |
| `empty` | `true` se não há dados |

---

## 🗂️ Estrutura do Projeto

```
analisador-pncp/
├── main.py           # Menu e fluxo principal
├── coletor.py        # Classe Coletor — requisições à API + paginação
├── banco.py          # Classe Banco — CRUD com SQLite
├── analisador.py     # Classe Analisador — consultas SQL + pandas + gráficos
└── dados/
    └── pncp.db       # Banco SQLite
```

---

## 🧱 As Classes

### `Coletor`
Mesmo padrão do projeto BCB — cada responsabilidade em método separado.

```
Métodos:
- verificar_cache()                              → verifica se banco existe e tem dados
- mostrar_menu()                                 → exibe opções (cache ou novo período)
- solicitar_parametros()                         → pede datas, UF, modalidade
- coletar_pagina(url, parametros, pagina)        → GET de uma página
- coletar_todas_paginas(url, parametros)         → loop com paginasRestantes
- coletar_dados()                                → orquestra tudo
```

**Novidade vs BCB:** a paginação. No BCB cada requisição retorna tudo. No PNCP vem em páginas de 50 — precisa de loop.

### `Banco`
Gerencia a persistência em SQLite. **Classe nova — não existia nos projetos anteriores.**

```
Métodos:
- criar_tabela()                  → CREATE TABLE IF NOT EXISTS
- inserir_licitacoes(dados)       → INSERT com tratamento de duplicatas
- consultar_todas()               → SELECT * → retorna DataFrame
- consultar_por_modalidade(id)    → SELECT com WHERE
- consultar_por_municipio(nome)   → SELECT com WHERE
- consultar_por_periodo(ini, fim) → SELECT com BETWEEN
- consultar_top_valores(n)        → SELECT ORDER BY ... LIMIT
- consultar_top_orgaos(n)         → SELECT com GROUP BY + COUNT
- contar_registros()              → SELECT COUNT(*)
```

**Fluxo:** API → pandas (normaliza/limpa) → SQLite (persiste) → SQL (consulta) → pandas (exibe/exporta)

### `Analisador`
Recebe dados do `Banco` via SQL e gera análises.

```
Métodos:
- carregar_dados()                → lê do banco via Banco.consultar_todas()
- resumo_por_modalidade()         → usa Banco ou groupby
- top_orgaos(n)                   → usa Banco.consultar_top_orgaos()
- maiores_valores(n)              → usa Banco.consultar_top_valores()
- por_municipio()                 → distribuição por cidade
- calcular_estatisticas()         → média, min, max dos valores
- filtrar_periodo(inicio, fim)    → filtra via SQL
- exportar_csv()                  → exporta filtrado
- exportar_excel()                → exporta com múltiplas abas
```

**Novidade vs BCB:** consultas são feitas com SQL real via `pd.read_sql()`, não só métodos pandas.

---

## ⚙️ Funcionalidades

```
[ ] Coletar licitações de MT em um intervalo de datas
[ ] Paginar automaticamente usando paginasRestantes
[ ] Normalizar JSON aninhado com pd.json_normalize()
[ ] Limpar dados: remover nulos, duplicatas
[ ] Persistir em SQLite (CREATE TABLE, INSERT, SELECT)
[ ] Consultas SQL reais (WHERE, GROUP BY, ORDER BY, LIMIT, BETWEEN)
[ ] Carregar do banco sem buscar da API de novo
[ ] Menu: usar cache ou novo período (padrão BCB)
[ ] Resumo por modalidade (contagem + valor total)
[ ] Top 10 órgãos que mais licitaram
[ ] Top 10 licitações de maior valor estimado
[ ] Distribuição por município
[ ] Filtrar por período personalizado
[ ] Gráfico de barras — licitações por modalidade
[ ] Exportar CSV e Excel
```

---

## 💡 Menu Sugerido

```
=============================
  ANALISADOR PNCP — MT
=============================
1. Coletar dados da API
2. Resumo por modalidade
3. Top 10 órgãos
4. Maiores valores estimados
5. Distribuição por município
6. Filtrar período
7. Gráficos
8. Exportar CSV
9. Exportar Excel
0. Sair
=============================
```

---

## 🔍 Estrutura da Resposta da API

A API retorna um dicionário com os seguintes campos principais:

```json
{
    "data": [ {...}, {...} ],
    "totalRegistros": 342,
    "totalPaginas": 7,
    "numeroPagina": 1,
    "paginasRestantes": 6,
    "empty": false
}
```

Cada item dentro de `data` tem a seguinte estrutura relevante:

```json
{
    "numeroControlePNCP": "...",
    "modalidadeId": 6,
    "modalidadeNome": "Pregão - Eletrônico",
    "situacaoCompraNome": "Divulgada no PNCP",
    "objetoCompra": "Aquisição de materiais de limpeza",
    "valorTotalEstimado": 150000.00,
    "valorTotalHomologado": 148000.00,
    "dataPublicacaoPncp": "2026-01-15",
    "dataAberturaProposta": "2026-01-20T10:00:00",
    "dataEncerramentoProposta": "2026-01-25T10:00:00",
    "orgaoEntidade": {
        "cnpj": "...",
        "razaoSocial": "PREFEITURA DE CUIABÁ",
        "poderId": "E",
        "esferaId": "M"
    },
    "unidadeOrgao": {
        "municipioNome": "Cuiabá",
        "ufSigla": "MT",
        "ufNome": "Mato Grosso"
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

**Modalidades disponíveis (parâmetro obrigatório):**
| Código | Modalidade |
|---|---|
| 1 | Leilão Eletrônico |
| 4 | Concorrência Eletrônica |
| 6 | Pregão Eletrônico ← mais comum |
| 8 | Dispensa de Licitação |
| 9 | Inexigibilidade |

---

## 🐼 Pandas — Novidades vs Projeto BCB

**Normalizar JSON aninhado (NOVO):**
O campo `orgaoEntidade` é um dicionário dentro do dicionário. Para achatar tudo em colunas:

```python
import pandas as pd

df = pd.json_normalize(dados, sep="_")
# orgaoEntidade.razaoSocial vira orgaoEntidade_razaoSocial
# unidadeOrgao.municipioNome vira unidadeOrgao_municipioNome
```

**Remover duplicatas (NOVO):**
```python
df = df.drop_duplicates(subset=["numeroControlePNCP"])
```

**Remover nulos antes de ordenar (NOVO):**
```python
df = df.dropna(subset=["valorTotalEstimado"])
```

**Top N por valor (já conhece a lógica, método novo):**
```python
df.nlargest(10, "valorTotalEstimado")
```

**Contagem por grupo (já usou groupby):**
```python
df.groupby("modalidadeNome")["valorTotalEstimado"].agg(["count", "sum", "mean"])
```

**Exportar Excel com múltiplas abas (NOVO):**
```python
with pd.ExcelWriter("relatorio_pncp.xlsx") as writer:
    df_resumo.to_excel(writer, sheet_name="Resumo", index=False)
    df_top_orgaos.to_excel(writer, sheet_name="Top Órgãos", index=False)
    df_maiores.to_excel(writer, sheet_name="Maiores Valores", index=False)
```

---

## 🗄️ SQLite — Primeiro Banco de Dados

SQLite é um banco de dados que vive em um único arquivo `.db`. Já vem embutido no Python — `import sqlite3`. Sem servidor, sem instalação, sem configuração.

**Criar conexão e tabela:**
```python
import sqlite3

conn = sqlite3.connect("dados/pncp.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS licitacoes (
        numero_controle TEXT PRIMARY KEY,
        modalidade_nome TEXT,
        objeto_compra TEXT,
        valor_estimado REAL,
        valor_homologado REAL,
        data_publicacao TEXT,
        orgao_nome TEXT,
        municipio TEXT,
        uf TEXT,
        situacao TEXT
    )
""")
conn.commit()
```

**Inserir dados do DataFrame:**
```python
df.to_sql("licitacoes", conn, if_exists="append", index=False)
```

**Consultar com SQL real e receber DataFrame:**
```python
df = pd.read_sql("SELECT * FROM licitacoes WHERE uf = 'MT'", conn)
```

**Consultas úteis:**
```sql
-- Top 10 órgãos que mais licitaram
SELECT orgao_nome, COUNT(*) as total, SUM(valor_estimado) as valor_total
FROM licitacoes
GROUP BY orgao_nome
ORDER BY total DESC
LIMIT 10;

-- Licitações acima de R$ 1 milhão
SELECT objeto_compra, valor_estimado, orgao_nome
FROM licitacoes
WHERE valor_estimado > 1000000
ORDER BY valor_estimado DESC;

-- Total por modalidade
SELECT modalidade_nome, COUNT(*) as total, AVG(valor_estimado) as media
FROM licitacoes
GROUP BY modalidade_nome;

-- Filtro por período
SELECT * FROM licitacoes
WHERE data_publicacao BETWEEN '2025-01-01' AND '2025-06-30';
```

**Fechar conexão:**
```python
conn.close()
```

**Por que SQLite e não JSON?**
- JSON carrega tudo na memória — SQLite consulta só o que precisa
- SQL permite filtros complexos sem escrever código Python
- O banco persiste entre execuções sem precisar recarregar
- Prepara para bancos maiores (PostgreSQL, MySQL) no futuro
- Streamlit conecta direto no SQLite — migração imediata

---

## 🪤 Armadilhas Comuns

**1. `codigoModalidadeContratacao` é obrigatório**
Sem ele a API retorna erro 400. Use 6 (Pregão Eletrônico) como padrão — é a modalidade mais comum.

**2. Campo `valorTotalEstimado` pode ser `None` ou `0`**
Algumas licitações têm orçamento sigiloso. Antes de ordenar por valor:
```python
df = df.dropna(subset=["valorTotalEstimado"])
df = df[df["valorTotalEstimado"] > 0]
```

**3. JSON aninhado — `orgaoEntidade` e `unidadeOrgao` são dicionários**
Usar `pd.json_normalize()` em vez de `pd.DataFrame()` direto. Sem isso os campos ficam como dicts dentro de colunas.

**4. API instável**
O PNCP é um servidor do governo — sai do ar periodicamente. Sempre use `try/except` com `requests.RequestException` e `timeout=15`.

**5. Rate limiting**
Muitas requisições seguidas podem gerar timeout. Use `time.sleep(0.5)` entre páginas.

**6. Dados duplicados entre páginas**
Em raros casos a API retorna o mesmo registro em duas páginas. Usa `drop_duplicates(subset=["numeroControlePNCP"])` depois de coletar tudo.

**7. Status 204 = sem dados**
Diferente de erro — significa que não há licitações naquele filtro. Trate separado do 400/500.

---

## 🚀 Ordem de Execução Recomendada

```
1. Testa a API no navegador — confirma que está no ar
2. Testa uma requisição no Python — imprime o primeiro item de "data"
3. Cria a classe Coletor com coletar_pagina() para uma página
4. Testa — verifica se os dados chegam corretamente
5. Adiciona paginação com coletar_todas_paginas()
6. Normaliza com pd.json_normalize() e limpa os dados
7. Cria a classe Banco com criar_tabela() e inserir_licitacoes()
8. Testa — insere dados e consulta com SELECT
9. Adiciona consultas SQL: por modalidade, por município, top valores
10. Cria o Analisador usando Banco como fonte de dados
11. Implementa gráficos e exportação
12. Monta o main.py com o menu
```

> **Regra que você já conhece:** só avança quando o passo anterior estiver testado e funcionando.

---

## 🧪 Teste Rápido Antes de Começar

Antes de escrever qualquer classe, testa no terminal interativo do Python ou num arquivo `.py` simples:

```python
import requests

url = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
params = {
    "dataInicial": "20260101",
    "dataFinal": "20260131",
    "codigoModalidadeContratacao": 6,  # obrigatório — 6 = Pregão Eletrônico
    "uf": "MT",
    "tamanhoPagina": 10,
    "pagina": 1
}

r = requests.get(url, params=params, timeout=10)
print(r.status_code)
print(r.json()["data"][0])       # primeiro resultado
print(r.json()["totalRegistros"]) # total de licitações encontradas
print(r.json()["paginasRestantes"]) # quantas páginas ainda faltam
```

Se retornar 200 e um dicionário com dados — você está pronto para começar.

> **Atenção:** `codigoModalidadeContratacao` é obrigatório — sem ele a API retorna erro 400.

---

## 🚧 Melhorias Futuras

- [ ] Filtro por município (Cuiabá, Várzea Grande, Rondonópolis)
- [ ] Filtro por palavra-chave no objeto da compra (ex: "câmera", "CFTV", "TI")
- [ ] Comparativo entre modalidades (Pregão vs Dispensa — quem gasta mais?)
- [ ] Comparativo entre períodos (mês a mês)
- [ ] Consultar contratos via endpoint `/v1/contratos`
- [ ] Dashboard web com Streamlit (próximo projeto — banco SQLite já estará pronto)

---

## 💼 Diferencial no Portfólio

Este projeto demonstra:
- Consumo de API REST pública com paginação
- Normalização de JSON aninhado (`pd.json_normalize`)
- Limpeza de dados reais (nulos, duplicatas, valores zerados)
- Persistência em banco de dados SQLite com SQL real
- Consultas SQL: WHERE, GROUP BY, ORDER BY, LIMIT, BETWEEN
- Análise exploratória com agrupamentos e rankings
- Visualização com matplotlib
- Exportação para Excel com múltiplas abas
- Domínio de dados públicos brasileiros — **nicho com poucos concorrentes**

**Conexão com sua experiência:** você trabalhou na SSP-MT e agora na prefeitura com CFTV. Analisar licitações públicas de MT é um projeto que nenhum outro candidato júnior tem no portfólio.

No README, documente insights reais: "Em 2025, os órgãos de MT publicaram X pregões eletrônicos totalizando R$ Y milhões. Os 3 órgãos que mais licitaram foram Z."

---

*Testa a requisição primeiro. Depois é só chamar.*