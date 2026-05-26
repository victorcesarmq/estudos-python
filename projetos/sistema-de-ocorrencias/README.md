# 🚨 Sistema de Registro de Ocorrências

Sistema em linha de comando para registro, consulta e análise de ocorrências policiais, desenvolvido em Python com foco em Programação Orientada a Objetos, persistência de dados em JSON e análise com pandas.

## 📋 Sobre o Projeto

Inspirado diretamente na operação do **CIOSP / SSP-MT**, este sistema simula o fluxo real de registro de ocorrências — desde o cadastro com local, data e tipo, até a consulta por filtros e geração de relatórios.

O projeto foi desenvolvido como evolução do [Sistema Bancário Multi-Conta](https://github.com/victorcesarmq/estudos-python/tree/main/projetos/desafio-banco-multiconta), aplicando os mesmos conceitos de POO e persistência em um domínio mais próximo da experiência profissional do autor.

## ⚙️ Funcionalidades

- Cadastro de ocorrências com tipo, local, data, status e descrição
- Data retroativa ou automática (data/hora atual)
- Validação de entradas com loop até dado válido
- Listagem de ocorrências concluídas
- Listagem de ocorrências em andamento
- Filtro personalizado acumulativo por status, local, tipo e data
- Persistência automática em JSON
- Relatórios gerados com pandas

## 🗂️ Estrutura do Projeto

```
desafio-ocorrencias/
├── main.py          # Menu principal e fluxo do programa
├── ocorrencia.py    # Classe Ocorrencia — atributos e métodos de definição
├── registro.py      # Classe Registro — gerencia todas as ocorrências
├── relatorio.py     # Classe Relatorio — filtros e análises com pandas
└── dados/
    └── ocorrencias.json  # Gerado automaticamente pelo programa
```

## 🧠 Conceitos Aplicados

| Conceito | Onde foi aplicado |
|---|---|
| Classes e objetos | `Ocorrencia`, `Registro`, `Relatorio` |
| `__init__` e `self` | Inicialização de atributos em todas as classes |
| Separação de responsabilidades | Cada classe com escopo bem definido |
| Injeção de dependência | `Relatorio` recebe `Registro` como parâmetro |
| Persistência com JSON | Salvar e carregar ocorrências entre sessões |
| `pathlib` | Caminhos relativos independentes do sistema |
| `datetime` | Registro e conversão de datas |
| `pandas` | Filtros, agrupamentos e relatórios |
| Validação com `while True` | Entradas inválidas pedem nova tentativa |

## ▶️ Como Executar

**Pré-requisitos:** Python 3.10+ e pandas instalado

```bash
pip install pandas

git clone https://github.com/victorcesarmq/estudos-python.git
cd estudos-python/projetos/sistema-de-ocorrencias
python main.py
```

## 💡 Exemplo de Uso

```
Ocorrencias
1. Cadastrar Ocorrencia
2. Ocorrencias Concluidas
3. Ocorrencias Em Andamento
4. Filtro personalizado
5. Sair
Escolha: 1

Qual o local da Ocorrencia?
1. Cuiaba
2. Varzea Grande
Digite o nome do local: Cuiaba
Local valido

A ocorrencia aconteceu hoje ou em uma data retrograda?
1. Agora
2. Retrograda
Digite uma opcao: 1

Defina a descricao da ocorrencia
Digite uma descricao: Furto de veículo no estacionamento

Defina o status da ocorrencia
1 - Em andamento
2 - Finalizada
Digite uma opcao: 1

Defina o tipo da ocorrencia
1 - Furto
2 - Roubo
Digite uma opcao: 1
```

## 📁 Formato do JSON

```json
[
    {
        "Id": 1,
        "tipo": "Furto",
        "local": "Cuiaba",
        "descricao": "Furto de veículo no estacionamento",
        "data": "19/05/2026 14:32:10",
        "status": "Em andamento"
    }
]
```

## 🔍 Filtro Personalizado

O filtro personalizado permite combinar múltiplos critérios de forma acumulativa — cada filtro aplicado reduz o conjunto de resultados até a execução final.

```
Filtros:
1. Status
2. Local
3. Tipo
4. Data
5. Executar filtro
```

## 🚧 Melhorias Futuras

- [x] Encerrar ocorrência por ID
- [ ] Busca por intervalo de datas
- [ ] Exportação do relatório em CSV/Excel

## 🧱 Arquitetura

```
main.py
  ├── Ocorrencia     → coleta e valida dados de uma ocorrência
  ├── Registro       → gerencia a lista e persiste em JSON
  └── Relatorio(Registro) → consome o Registro e gera análises
```

O `Relatorio` recebe o objeto `Registro` já existente como parâmetro — sem duplicar o carregamento do JSON.

## 👨‍💻 Contexto Profissional

Este projeto é inspirado no trabalho operacional da **CIOSP/Secretaria de Segurança Publica de Mato Grosso**, onde ocorrências como veículos irradiados, reconhecimentos faciais e mandados de prisão são registrados.

A estrutura de dados e os tipos de ocorrência refletem cenários reais vivenciados durante o estágio técnico realizado no programa entre 2023 e 2025.

## 👨‍💻 Autor

**Victor Cesar de Morais Queiroz**
Estudante de Engenharia de Dados | Cuiabá - MT
[GitHub](https://github.com/victorcesarmq)
