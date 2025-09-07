# Guia de Estudo e Documentação do Projeto Movie-Project

Olá, eu do futuro! Este documento detalha a arquitetura, as decisões de design e os principais aprendizados do nosso primeiro projeto de pipeline de dados com LangChain.

## Como Executar

1.  **Dependências**: Certifique-se de que todas as dependências do `pyproject.toml` (incluindo `pandas`) estejam instaladas em seu ambiente virtual.
    ```bash
    pip install -e .
    ```
2.  **Arquivo `.env`**: Crie um arquivo `.env` na raiz do projeto com suas chaves de API:
    ```env
    OPENAI_API_KEY="sk-..."
    LANGCHAIN_API_KEY="lsv2_..."
    LANGCHAIN_PROJECT="Movie Project"
    MODEL_TEMPERATURE=0.3
    ```
3.  **Execução**: Use a linha de comando para rodar o script, passando o gênero desejado.
    ```bash
    python main.py --genre "Ficção Científica"
    ```

## Saída de Dados com Pandas

Um dos objetivos finais do projeto foi transformar a saída do LLM em um formato útil para análise de dados.

1.  **Conversão**: Após receber a lista de objetos `MovieInfoData` do orquestrador, nós a convertemos em um DataFrame do Pandas com uma única linha de código:
    ```python
    df = pd.DataFrame([movie.model_dump() for movie in detailed_results])
    ```
2.  **Visualização**: O `main.py` exibe a tabela formatada do DataFrame diretamente no console, permitindo uma verificação visual imediata dos dados.
3.  **Salvando em CSV**: Em vez de construir o CSV manualmente, usamos o método nativo e robusto do Pandas, que lida automaticamente com cabeçalhos e formatação:
    ```python
    df.to_csv(csv_filepath, index=False, encoding="utf-8")
    ```

## Entendendo a Aleatoriedade (Temperatura vs. Cache)

Durante o desenvolvimento, notamos que executar o script duas vezes com o mesmo gênero resultava na mesma lista de filmes. A razão para isso é uma combinação de dois fatores:

1.  **Temperatura Baixa (0.3)**: A temperatura controla a "criatividade" do LLM. Um valor baixo (como 0.3) torna o modelo mais determinístico, favorecendo as respostas mais prováveis e factuais. Ele tenderá a sugerir os filmes mais famosos de um gênero consistentemente. Para obter mais variedade, poderíamos aumentar a temperatura para `0.7` ou `0.8` no arquivo `.env`.

2.  **Cache (A Causa Principal)**: LangChain e as APIs da OpenAI utilizam um **cache** para otimizar custos e velocidade. Se você envia uma requisição **idêntica** (mesmo prompt, modelo, temperatura, etc.) em um curto espaço de tempo, a API retorna a resposta anterior que está armazenada, em vez de gerar uma nova. Esta é a principal razão pela qual os resultados eram idênticos. Para forçar uma nova geração, basta fazer uma pequena alteração no prompt ou aumentar a temperatura.

## Como Planejar um Projeto de IA como Este (Roteiro)

A nossa jornada de tutoria nos ensinou um fluxo de trabalho eficaz para construir aplicações de IA.

**Passo 1: Defina o Objetivo Final (Comece pelo Fim)**
* **Pergunta**: "Qual é o artefato final que eu quero?"
* **Resposta no Projeto**: "Quero um arquivo CSV com uma lista de filmes e seus detalhes, gerado a partir de um gênero."

**Passo 2: Modele Seus Dados (A Abordagem "Schema-First")**
* **Pergunta**: "Qual é a 'forma' exata dos dados que eu quero no meu CSV?"
* **Resposta no Projeto**: Criamos as classes `MovieList` e `MovieInfoData` em `core/models.py`. Isso define um contrato claro antes mesmo de falar com o LLM.

**Passo 3: Decomponha o Problema em Tarefas Atômicas**
* **Pergunta**: "Quais são as chamadas individuais ao LLM que eu preciso fazer?"
* **Resposta no Projeto**:
    * Tarefa A: "Dado um gênero, me dê uma lista de títulos." -> `chain_suggestion.py`
    * Tarefa B: "Dado um título, me dê seus detalhes." -> `chain_details.py`

**Passo 4: Orquestre o Fluxo de Dados (Desenhe o Grafo)**
* **Pergunta**: "Como as saídas de uma tarefa se conectam às entradas de outra?"
* **Resposta no Projeto**: Criamos o `core/orchestrator.py`. Mapeamos o fluxo: a saída da Tarefa A (lista de títulos) se torna a entrada para múltiplas execuções paralelas da Tarefa B.

**Passo 5: Crie a Interface do Usuário (O Ponto de Entrada)**
* **Pergunta**: "Como um humano vai interagir com meu sistema?"
* **Resposta no Projeto**: Construímos o `main.py` com `argparse` para criar uma interface de linha de comando clara e robusta.

**Passo 6: Configure a Base (Ferramentas e Setup)**
* **Pergunta**: "Como garanto que meu projeto é seguro, consistente e fácil de depurar?"
* **Resposta no Projeto**: Criamos `settings.py` (para configurações e chaves), `logger.py` (para logs) e configuramos `Ruff`/`Pyright` (para qualidade de código).

Este roteiro, combinado com o auxílio da IA para refinar código, explicar conceitos e depurar, é um caminho poderoso para aumentar sua produtividade e construir aplicações cada vez mais complexas.