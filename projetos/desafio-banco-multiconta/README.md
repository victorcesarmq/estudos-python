# 🏦 Sistema Bancário Multi-Conta

Sistema bancário em linha de comando desenvolvido em Python, com suporte a múltiplas contas, persistência de dados em JSON e histórico de transações.

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como exercício prático de **Programação Orientada a Objetos (POO)** em Python, cobrindo conceitos como classes, herança, encapsulamento, manipulação de arquivos e persistência de dados.

O sistema simula operações bancárias reais: cadastro de clientes, depósitos, saques e extrato — com os dados salvos localmente em arquivos JSON, garantindo que nenhuma informação seja perdida ao fechar o programa.

## ⚙️ Funcionalidades

- Cadastro de múltiplas contas com nome e CPF
- Acesso individual por CPF
- Depósito com registro no histórico
- Saque com validação de saldo e limite
- Extrato com data, hora e tipo de operação
- Persistência automática em JSON por conta

## 🗂️ Estrutura do Projeto

```
desafio-banco-multiconta/
├── banco-multiconta.py   # Menu principal e fluxo do programa
├── banco.py              # Classe Banco — gerencia todas as contas
├── conta.py              # Classe Conta — operações individuais
└── *.json                # Gerados automaticamente pelo programa
```

## 🧠 Conceitos Aplicados

| Conceito | Onde foi aplicado |
|---|---|
| Classes e objetos | `Banco`, `Conta` |
| `__init__` e `self` | Inicialização de atributos em ambas as classes |
| Dicionários | `self.pessoa {cpf: Conta}` no `Banco` |
| Persistência com JSON | Histórico e saldo por conta + cadastro no Banco |
| `pathlib` | Manipulação de caminhos de arquivo |
| `datetime` | Registro de data e hora em cada transação |
| Separação de responsabilidades | Cada classe cuida do seu próprio estado |

## ▶️ Como Executar

**Pré-requisitos:** Python 3.10+

```bash
# Clone o repositório
git clone https://github.com/victorcesarmq/estudos-python.git

# Acesse a pasta do projeto
cd estudos-python/projetos/desafio-banco-multiconta

# Execute
python banco-multiconta.py
```

## 💡 Exemplo de Uso

```
--------------------
MENU DE CONTA
--------------------
1 - Cadastrar conta
2 - Acessar conta
3 - Sair
--------------------
Escolha: 1
Nome: Victor Cesar
CPF: 067.164.481-52

--------------------
MENU DE CONTA
--------------------
Escolha: 2
Contas Disponíveis: 067.164.481-52
Digite o CPF: 067.164.481-52

Conta Atual: 067.164.481-52
Saldo: R$0.00
1 - Depositar
2 - Saque
3 - Extrato
4 - Sair
```

## 📁 Formato dos Arquivos JSON

Cada conta gera um arquivo `{cpf}.json`:

```json
{
    "CPF": "067.164.481-52",
    "Nome": "Victor Cesar",
    "saldo": 800.0,
    "historico": [
        {
            "Id-transacao": 1,
            "Valor": 1000.0,
            "Data": "01/05/2026 14:32:10",
            "Operacao": "Deposito"
        },
        {
            "Id-transacao": 2,
            "Valor": 200.0,
            "Data": "01/05/2026 14:33:05",
            "Operacao": "Saque"
        }
    ]
}
```

## 🚧 Melhorias Futuras

- [ ] Verificação de CPF duplicado no cadastro
- [ ] Herança com `ContaCorrente` e `ContaPoupança`
- [ ] Transferência entre contas
- [ ] Relatório de movimentações com `pandas`
- [ ] Interface gráfica com `tkinter`

## 👨‍💻 Autor

**Victor Cesar de Morais Queiroz**  
Estudante de Engenharia de Dados | Cuiabá - MT  
[GitHub](https://github.com/victorcesarmq)
