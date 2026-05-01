# 🚨 Desafio — Sistema de Registro de Ocorrências

> **Pré-requisito:** Antes de começar, volte no projeto `desafio-banco-multiconta` e corrija:
> - [ ] Verificação de CPF duplicado no cadastro
> - [ ] Renomear `self.pessoa` para `self.contas`
> - [ ] Mensagem de erro quando CPF não encontrado

---

## 📋 Sobre o Projeto

Sistema em linha de comando para registro e consulta de ocorrências policiais, inspirado diretamente na operação do **Programa Vigia Mais MT / SSP-MT**.

O sistema permite registrar ocorrências com tipo, local, data e status — consultar por filtros — e gerar um relatório de resumo usando `pandas`.

Este é o projeto ideal para consolidar POO com múltiplas classes interagindo, introduzir `pandas` de forma natural e construir um portfólio com narrativa profissional real.

---

## 🎯 Objetivo de Aprendizado

| Conceito | O que vai praticar |
|---|---|
| POO | Três classes interagindo: `Ocorrencia`, `Registro`, `Relatorio` |
| `dataclasses` | Forma mais limpa de criar classes de dados simples |
| `pandas` | Filtros, agrupamentos e exportação de relatório |
| `datetime` | Registro e comparação de datas |
| `json` + `pathlib` | Persistência — o mesmo padrão do projeto anterior |
| Leitura de traceback | Pandas vai quebrar — você vai precisar ler o erro |

---

## 🗂️ Estrutura de Arquivos Sugerida

```
sistema-ocorrencias/
├── main.py              # Menu principal e fluxo
├── ocorrencia.py        # Classe Ocorrencia — representa uma ocorrência
├── registro.py          # Classe Registro — gerencia todas as ocorrências
├── relatorio.py         # Classe Relatorio — gera relatórios com pandas
├── dados/
│   └── ocorrencias.json # Gerado automaticamente
└── README.md
```

---

## 🧱 As Três Classes

### `Ocorrencia`
Representa uma ocorrência individual. Deve ter:

```
- id          → gerado automaticamente (inteiro sequencial)
- tipo        → ex: "Veículo Irradiado", "Reconhecimento Facial", "Incêndio"
- local       → ex: "Cuiabá", "Várzea Grande"
- data        → datetime — data e hora do registro
- status      → "aberta" ou "encerrada"
- descricao   → texto livre opcional
```

Pensa: quais desses atributos o usuário informa e quais o sistema gera automaticamente?

---

### `Registro`
Gerencia todas as ocorrências — é o equivalente ao `Banco` do projeto anterior. Deve ter:

```
- ocorrencias       → lista de objetos Ocorrencia
- adicionar(...)    → cria e adiciona uma nova ocorrência
- buscar_por_tipo(tipo)    → retorna ocorrências filtradas por tipo
- buscar_por_local(local)  → retorna ocorrências filtradas por local
- encerrar(id)      → muda o status de uma ocorrência para "encerrada"
- salvar()          → persiste em JSON
- carregar()        → lê do JSON ao iniciar
```

---

### `Relatorio`
Recebe a lista de ocorrências e gera análises com `pandas`. Deve ter:

```
- gerar_resumo()         → total por tipo de ocorrência
- gerar_por_local()      → total por local
- gerar_timeline()       → ocorrências por dia
- exportar_csv(caminho)  → salva o relatório em .csv
```

---

## ⚙️ Funcionalidades Obrigatórias

```
[ ] Registrar nova ocorrência (tipo, local, descrição)
[ ] Listar todas as ocorrências abertas
[ ] Buscar por tipo
[ ] Buscar por local
[ ] Encerrar uma ocorrência por ID
[ ] Gerar relatório de resumo com pandas
[ ] Persistência em JSON
```

---

## 💡 Menu Sugerido

```
=============================
  SISTEMA DE OCORRÊNCIAS
=============================
1. Registrar ocorrência
2. Listar ocorrências abertas
3. Buscar por tipo
4. Buscar por local
5. Encerrar ocorrência
6. Relatório
0. Sair
=============================
```

---

## 📁 Formato do JSON

```json
[
    {
        "id": 1,
        "tipo": "Veículo Irradiado",
        "local": "Cuiabá",
        "data": "01/05/2026 14:32:10",
        "status": "encerrada",
        "descricao": "Veículo recuperado pelo 3º BPM"
    },
    {
        "id": 2,
        "tipo": "Reconhecimento Facial",
        "local": "Várzea Grande",
        "data": "01/05/2026 15:10:00",
        "status": "aberta",
        "descricao": ""
    }
]
```

---

## 🐼 Introdução ao Pandas

Pandas é uma biblioteca para análise de dados tabulares. Pensa nela como uma planilha Excel dentro do Python.

**Conceito central: o DataFrame**
Um DataFrame é uma tabela com linhas e colunas. Você cria um a partir de uma lista de dicionários:

```python
import pandas as pd

dados = [
    {"tipo": "Incêndio", "local": "Cuiabá"},
    {"tipo": "Incêndio", "local": "Várzea Grande"},
    {"tipo": "Veículo Irradiado", "local": "Cuiabá"},
]

df = pd.DataFrame(dados)
print(df)
#                tipo          local
# 0          Incêndio         Cuiabá
# 1          Incêndio  Várzea Grande
# 2  Veículo Irradiado        Cuiabá
```

**Filtrar:**
```python
# Só ocorrências em Cuiabá
df[df["local"] == "Cuiabá"]
```

**Contar por categoria:**
```python
# Quantas ocorrências de cada tipo
df.groupby("tipo").size()
```

**Exportar:**
```python
df.to_csv("relatorio.csv", index=False, encoding="utf-8")
```

---

## 🪤 Armadilhas Comuns

**1. Salvar objetos em JSON**
Assim como no projeto anterior, JSON não salva objetos Python.
Você precisará converter cada `Ocorrencia` para dicionário antes de salvar
e recriar os objetos ao carregar. Como você fez no `Banco`.

**2. Salvar e carregar `datetime`**
`datetime` não é serializável em JSON diretamente. Converte para string ao salvar:
```python
"data": ocorrencia.data.strftime("%d/%m/%Y %H:%M:%S")
```
E converte de volta ao carregar:
```python
data = dt.datetime.strptime(dados["data"], "%d/%m/%Y %H:%M:%S")
```

**3. ID sequencial**
O ID da próxima ocorrência deve ser `len(self.ocorrencias) + 1`.
Mas cuidado: se você deletar ocorrências no meio, isso quebra. Por ora não se preocupe com deleção.

**4. Pandas com lista vazia**
Se não houver ocorrências e você tentar criar um DataFrame, vai receber um erro ou um DataFrame vazio.
Sempre valide antes:
```python
if len(self.ocorrencias) == 0:
    print("Nenhuma ocorrência registrada.")
    return
```

---

## 🔍 Hábito a Desenvolver Neste Projeto

Antes de me chamar com um erro, faça isso:

1. Leia a **última linha** do traceback — ela diz o tipo do erro
2. Leia a **linha apontada** no seu código
3. Pergunte a si mesmo: *"o que eu esperava e o que está acontecendo de fato?"*
4. Tente pelo menos uma correção antes de pedir ajuda

Pandas vai gerar erros de coluna não encontrada, tipo incompatível e índice errado. Todos são legíveis. Este projeto vai te treinar a resolver isso sozinho.

---

## 🚀 Ordem de Execução Recomendada

```
1. Cria a classe Ocorrencia com todos os atributos
2. Testa criando um objeto manualmente no terminal
3. Cria a classe Registro com adicionar() e listar()
4. Testa adicionar e listar antes de qualquer outra coisa
5. Adiciona persistência (salvar e carregar)
6. Testa fechar e abrir — verifica se os dados voltam
7. Adiciona os filtros (buscar_por_tipo, buscar_por_local)
8. Adiciona encerrar()
9. Monta o main.py com o menu
10. Por último: cria a classe Relatorio com pandas
```

> **Regra:** só avança para o próximo passo depois de testar o anterior.

---

## 🚧 Melhorias Futuras (para versões posteriores)

- [ ] Filtro por data (ocorrências das últimas 24h, da última semana)
- [ ] Paginação na listagem (mostrar 10 por vez)
- [ ] Dashboard visual com `matplotlib`
- [ ] Exportação para Excel com `openpyxl`
- [ ] Versão web com `Flask` ou `FastAPI`

---

## 👨‍💻 Contexto Profissional

Este projeto é diretamente inspirado no trabalho operacional do **Programa Vigia Mais MT** na SSP-MT, onde ocorrências como veículos irradiados, reconhecimentos faciais e mandados de prisão são registrados e monitorados em tempo real.

No README final do projeto, documente essa conexão — é um diferencial real no portfólio.

---

*Qualquer dúvida é só chamar. Mas tenta resolver o traceback primeiro.*
