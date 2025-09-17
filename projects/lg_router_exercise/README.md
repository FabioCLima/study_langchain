# LangGraph: Roteador de Processamento de Texto

## Descrição

Este projeto é um exemplo prático de como transformar um experimento de um Jupyter Notebook em uma aplicação Python robusta e modular. O objetivo é processar uma string de texto de acordo com uma ação definida pelo usuário (`reverse` ou `upper`).

A principal característica do projeto é o uso de um grafo condicional em **LangGraph**, onde o ponto de entrada é um roteador. Esse roteador, análogo a uma estrutura `if/else` em Python, direciona o fluxo de dados para o nó de processamento correto com base na escolha do usuário.

## 🚀 Funcionalidades Principais

- **Processamento de Texto:** Executa duas operações distintas:  
  - Inverte a ordem dos caracteres de uma string.  
  - Converte todos os caracteres para maiúsculas.  
- **Roteamento Condicional:** Utiliza um roteador como ponto de entrada do grafo para direcionar a execução de forma dinâmica.  
- **Validação de Dados Robusta:** O estado do grafo é definido com **Pydantic**, garantindo validação automática e segurança dos tipos de dados na entrada, rejeitando ações inválidas antes mesmo de o grafo ser executado.  
- **Estrutura Modular:** O código é organizado em módulos com responsabilidades únicas (`settings`, `state`, `nodes`, `graph_builder`), seguindo boas práticas de engenharia de software.  
- **Interface de Terminal Aprimorada:** A saída no terminal é formatada com a biblioteca **Rich** para uma experiência de usuário mais clara e agradável.  

## 🛠️ Tecnologias Utilizadas

- **Orquestração:** LangGraph  
- **Validação de Dados:** Pydantic  
- **Configuração:** Pydantic-Settings e python-dotenv  
- **Qualidade de Código:** Ruff (linting e formatação)  
- **Logging:** Loguru  
- **UI de Terminal:** Rich  

## 📂 Estrutura do Projeto

O projeto é dividido nos seguintes módulos para garantir a separação de responsabilidades:

```bash

lg\_router\_exercise/
├── .env               # Armazena chaves de API e configurações secretas
├── **main**.py        # Permite que o pacote seja executável
├── main.py            # Ponto de entrada principal da aplicação
├── settings.py        # Carrega e valida as configurações do ambiente
├── state.py           # Define a estrutura de dados do estado do grafo com Pydantic
├── nodes.py           # Contém as funções dos nós e a lógica do roteador
└── graph\_builder.py   # Constrói e compila o grafo LangGraph

````

## Como Executar

**1. Clone o Repositório:**

```bash
git clone <url-do-seu-repositorio>
cd lg_router_exercise_directory  # Navegue para o diretório que contém a pasta do projeto
````

**2. Crie e Ative um Ambiente Virtual:**

```sh
python -m venv .venv
source .venv/bin/activate
```

**3. Instale as Dependências:**

```sh
pip install -r requirements.txt
```

Arquivo `requirements.txt`:

```bash
langchain
langgraph
pydantic
pydantic-settings
loguru
rich
python-dotenv
```

**4. Configure o Ambiente:**
Crie um arquivo chamado `.env` na raiz do projeto (`lg_router_exercise/`) e adicione sua chave da API do LangSmith:

```ini
# .env
LANGSMITH_API_KEY="sua_chave_aqui"
```

**5. Execute a Aplicação:**
A partir do diretório que contém a pasta `lg_router_exercise/`, execute o seguinte comando:

```sh
python -m lg_router_exercise.main
```

A saída esperada da estrutura do grafo:

```bash
--- ESTRUTURA DO GRAFO  ---
              +-----------+               
              | __start__ |               
              +-----------+               
              ..           ..             
            ..               ..           
          ..                   ..         
+--------------+           +------------+ 
| reverse_node |           | upper_node | 
+--------------+           +------------+ 
              **           **             
                **       **               
                  **   **                 
                +---------+               
                | __end__ |               
                +---------+               
--------------------------

---

👉 `**main**.py` para `__main__.py` (mais apropriado para execução de pacotes).
```
