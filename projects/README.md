# Projeto RAG de Recomendação de Filmes com LangChain

Este projeto demonstra a construção de um assistente de recomendação de filmes utilizando a arquitetura **RAG (Retrieval-Augmented Generation)** com a biblioteca LangChain. A aplicação supera as limitações de um LLM genérico, fornecendo recomendações precisas e contextualizadas, baseadas em uma base de conhecimento controlada.

## ✨ Funcionalidades

* **Recomendações Baseadas em Dados:** As sugestões são geradas a partir de um catálogo de filmes pré-definido (`movie_catalog.json`), garantindo precisão e evitando "alucinações".
* **Busca Semântica:** Utiliza embeddings e um `VectorStore` para encontrar os filmes mais relevantes baseados no significado da descrição do usuário, não apenas em palavras-chave.
* **Interface Interativa:** Um chatbot de terminal permite que o usuário converse com o assistente e peça múltiplas recomendações.
* **Geração de Catálogo Dinâmica:** Inclui um script auxiliar que usa um LLM para gerar dinamicamente o catálogo de filmes, tornando a criação da base de conhecimento rápida e escalável.

## 🏛️ Arquitetura da Solução

O projeto é dividido em dois fluxos arquiteturais principais: um processo offline para preparação dos dados e um processo online para interação com o usuário.

**1. Fluxo de Geração de Dados (Offline)**
Este fluxo é executado uma única vez para criar a base de conhecimento.

`[Execução de gerar_catalogo.py]` → `[Input de Gênero]` → `[Chain Geradora (Prompt | LLM | Parser)]` → `[Criação do data/movie_catalog.json]`

**2. Fluxo da Aplicação RAG (Online)**
Este é o fluxo principal da aplicação, que é executado para interagir com o usuário.

`[Execução de main.py]` → `[Setup (Carregar JSON → Indexar no VectorStore → Criar Chain)]` → `[Loop Interativo]`

O ciclo RAG dentro do loop funciona da seguinte forma:
`[Pergunta do Usuário]` → `[Retriever busca no VectorStore]` → `[Contexto + Pergunta]` → `[Prompt Formatado]` → `[LLM Gera Resposta]`

## 📁 Estrutura do Projeto

```
movie_project_rag/
├── .env
├── data/
│   └── movie_catalog.json
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── logger.py
│   ├── models.py
│   └── rag_chain.py
├── gerar_catalogo.py
└── main.py
```

## 🚀 Módulos do Projeto (Deep Dive)

Cada módulo foi projetado com uma responsabilidade única para manter o código organizado e manutenível.

### `core/settings.py`
* **Responsabilidade:** Gerenciar configurações da aplicação de forma centralizada.
* **Detalhes:** Utiliza `pydantic-settings` para carregar configurações de variáveis de ambiente, como o `LOG_LEVEL`. Isso permite alterar o comportamento da aplicação sem modificar o código.

### `core/logger.py`
* **Responsabilidade:** Configurar uma instância de logger padronizada para todo o projeto.
* **Detalhes:** Utiliza a biblioteca `loguru` para criar logs formatados, coloridos e fáceis de ler, com base no nível definido em `settings.py`.

### `core/models.py`
* **Responsabilidade:** Definir os "contratos de dados" da aplicação.
* **Detalhes:** Utiliza Pydantic para criar modelos como `Filme` e `CatalogoFilmes`. Esses modelos garantem que os dados (seja lendo do JSON ou recebendo de um LLM) tenham uma estrutura validada e consistente.

### `gerar_catalogo.py`
* **Responsabilidade:** Ser um script utilitário e independente para criar a base de conhecimento (`data/movie_catalog.json`).
* **Detalhes:** É uma ferramenta de setup. Ele interage com o usuário para pedir um gênero de filme e, em seguida, utiliza uma chain LangChain (`Prompt | LLM | PydanticOutputParser`) para gerar uma lista estruturada de filmes e salvá-la em um arquivo JSON.

### `core/rag_chain.py`
* **Responsabilidade:** O cérebro da lógica RAG. Encapsula toda a complexidade de carregar, indexar e construir a chain de recomendação.
* **Detalhes:**
    * `load_catalog()`: Carrega os dados do `movie_catalog.json` usando `pathlib` para garantir a portabilidade do caminho do arquivo. Valida os dados carregados, transformando-os em uma lista de objetos Pydantic `Filme`.
    * `create_vector_store()`: Realiza a etapa de **Indexação**. Transforma cada objeto `Filme` em um `Document` LangChain, gera os embeddings para as sinopses e os armazena em um `InMemoryVectorStore`.
    * `create_rag_chain()`: Constrói a chain RAG final usando a LangChain Expression Language (LCEL). Utiliza um `RunnableParallel` para buscar o contexto (`retriever`) e passar a pergunta do usuário (`RunnablePassthrough`) simultaneamente para o prompt, que então alimenta o LLM para a geração da resposta final.

### `main.py`
* **Responsabilidade:** Ponto de entrada (`entrypoint`) e orquestração da aplicação.
* **Detalhes:**
    1.  Adiciona a raiz do projeto ao `sys.path` para garantir que os imports funcionem de forma robusta.
    2.  Executa a fase de **Setup**: chama as funções de `core/rag_chain.py` para carregar os dados, criar o `VectorStore` e montar a chain RAG.
    3.  Inicia um **Loop Interativo**: aguarda a entrada do usuário, invoca a chain RAG com a pergunta e exibe a resposta, até que o usuário decida sair.

## ⚙️ Instalação e Uso

Siga os passos abaixo para executar o projeto.

### Pré-requisitos
* Python 3.10+

### 1. Clone o Repositório
```bash
git clone <url-do-seu-repositorio>
cd movie_project_rag
```

### 2. Crie um Ambiente Virtual e Instale as Dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```
*(Nota: Para criar o arquivo `requirements.txt`, execute `pip freeze > requirements.txt` no seu ambiente ativado.)*

### 3. Configure as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione sua API Key da OpenAI:
```
OPENAI_API_KEY="sk-..."
```

### 4. Uso da Aplicação

**Passo 1: Gerar o Catálogo de Filmes**
Primeiro, execute o script para criar a sua base de conhecimento.
```bash
python gerar_catalogo.py
```
O script irá pedir para você digitar um gênero de filme. Após a execução, um arquivo `data/movie_catalog.json` será criado.

**Passo 2: Executar o Assistente de Recomendação**
Com o catálogo criado, inicie a aplicação principal.
```bash
python main.py
```
Aguarde as mensagens de setup. Quando o assistente estiver pronto, descreva o tipo de filme que você procura e pressione Enter. Para sair, digite `sair`.

## 💡 Conceitos Chave

Este projeto demonstra vários conceitos importantes de IA e engenharia de software:
* **Arquitetura RAG:** Para reduzir alucinações e basear as respostas do LLM em fontes de dados confiáveis.
* **LangChain Expression Language (LCEL):** Para compor `chains` de forma declarativa e poderosa.
* **Separação de Responsabilidades:** Cada módulo tem um propósito claro, tornando o código mais limpo e modular.
* **Validação de Dados com Pydantic:** Para garantir a integridade e a estrutura dos dados em todo o fluxo da aplicação.
* **Robustez e Portabilidade:** Uso de `pathlib` e manipulação do `sys.path` para criar uma aplicação que funciona de forma consistente em diferentes ambientes.

## 🔮 Melhorias Futuras

* **Persistência do VectorStore:** Substituir o `InMemoryVectorStore` por uma solução persistente como `ChromaDB` ou `FAISS` para que o índice não precise ser recriado a cada execução.
* **Memória Conversacional:** Adicionar memória à `chain` para que o assistente se lembre de interações passadas na mesma sessão.
* **Interface Gráfica:** Criar uma interface web simples usando `Streamlit` ou `FastAPI` para tornar a interação mais amigável.
* **Metadados Ricos:** Expandir os metadados dos filmes no catálogo (adicionando ano, diretor, gênero, etc.) para permitir buscas e filtros mais complexos.