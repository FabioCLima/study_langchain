# 📚 Documentação Didática - Projeto Roteiro de Viagem

## 🎯 Visão Geral do Projeto

O **Roteiro de Viagem** é um projeto educacional que demonstra como usar o LangChain para criar um sistema inteligente de recomendação de viagens. O projeto recebe um interesse de atividade do usuário (ex: "trekking", "praias históricas") e gera automaticamente:

1. **Um destino recomendado** com justificativa
2. **Lista de restaurantes** (caseiros e sofisticados)
3. **Passeios culturais** da região

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input User    │───▶│  Orchestrator   │───▶│  Output Final   │
│  (interesse)    │    │   (Main Chain)  │    │  (roteiro)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Sub-chains    │
                    │                 │
                    │ ┌─────────────┐ │
                    │ │ Destino     │ │
                    │ └─────────────┘ │
                    │ ┌─────────────┐ │
                    │ │Restaurantes │ │
                    │ └─────────────┘ │
                    │ ┌─────────────┐ │
                    │ │ Passeios    │ │
                    │ └─────────────┘ │
                    └─────────────────┘
```

## 🔧 Componentes Principais

### 1. **Models (Pydantic)**
Localização: `models/pydantic_models.py`

Os modelos Pydantic definem a estrutura dos dados que fluem entre as chains:

```python
class Destino(BaseModel):
    cidade: str = Field(description="Nome da cidade recomendada.")
    motivo: str = Field(description="Motivo da recomendação da cidade.")

class Restaurante(BaseModel):
    nome: str = Field(description="Nome do restaurante.")
    tipo: str = Field(description="Tipo de culinária do restaurante.")
    descricao: str = Field(description="Descrição do restaurante.")
```

**Por que Pydantic?**
- **Validação automática**: Garante que os dados estejam no formato correto
- **Serialização**: Fácil conversão para JSON/dict
- **Documentação**: Os campos são auto-documentados
- **Type Safety**: Integração perfeita com o sistema de tipos do Python

### 2. **Chains (LangChain)**
Localização: `chains/`

#### 2.1 Chain Destino (`chain_destino.py`)
```python
def create_chain_destino(model: ChatOpenAI) -> Callable[[dict[str, Any]], Destino]:
    parser = JsonOutputParser(pydantic_object=Destino)
    
    prompt = ChatPromptTemplate.from_template("""
        O usuário informou um interesse principal de atividade: "{interesse}".
        Sua tarefa é recomendar uma cidade ou região onde essa atividade
        seja muito popular e bem estruturada...
        {format_instructions}
    """)
    
    # Cria a chain usando o operador pipe
    chain: Runnable[dict[str, Any], Destino] = prompt | model | parser
```

**Conceitos importantes:**
- **Pipe Operator (`|`)**: Conecta prompt → modelo → parser em uma única chain
- **JsonOutputParser**: Converte a resposta do LLM para o modelo Pydantic
- **ChatPromptTemplate**: Template estruturado para o prompt

#### 2.2 Chain Restaurantes (`chain_restaurante.py`)
```python
def create_chain_restaurantes(model: ChatOpenAI) -> Callable[[dict[str, Any]], ListaRestaurantes]:
    parser = PydanticOutputParser(pydantic_object=ListaRestaurantes)
    
    prompt_template = """
    Você é um assistente especialista em gastronomia...
    Para a cidade {cidade}, sugira uma lista contendo:
    - 3 restaurantes de comida caseira de boa qualidade
    - 3 restaurantes mais sofisticados
    """
```

**Diferença do PydanticOutputParser:**
- **JsonOutputParser**: Para respostas simples (1 objeto)
- **PydanticOutputParser**: Para respostas complexas (listas, objetos aninhados)

#### 2.3 Chain Passeios (`chain_passeios.py`)
Similar à chain de restaurantes, mas foca em atrações culturais.

### 3. **Orchestrator (`orchestrador.py`)**
Localização: `chains/orchestrador.py`

O orchestrator é o **cérebro** do sistema que coordena todas as chains:

```python
def create_main_chain(model) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    # 1. Cria as sub-chains
    chain_destino = create_chain_destino(model)
    chain_restaurantes = create_chain_restaurantes(model)
    chain_passeios_culturais = create_chain_passeios_culturais(model)
    
    def run_main(inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 2. Executa sequencialmente
        destino = chain_destino(inputs)
        cidade = destino_dict.get("cidade")
        
        # 3. Executa sub-chains em paralelo (conceitual)
        restaurantes = chain_restaurantes({"cidade": cidade})
        passeios = chain_passeios_culturais({"cidade": cidade})
        
        return resultado
```

**Fluxo de execução:**
1. **Input**: `{"interesse": "trekking"}`
2. **Chain Destino**: Retorna cidade + motivo
3. **Chain Restaurantes**: Usa a cidade para sugerir restaurantes
4. **Chain Passeios**: Usa a cidade para sugerir atrações
5. **Output**: Roteiro completo organizado

### 4. **Configuração (`config.py`)**
Localização: `config.py`

```python
class Settings(BaseSettings):
    openai_api_key: SecretStr
    langchain_api_key: SecretStr
    model_name: str = "gpt-4.1"
    temperature: float = 0.3
    max_tokens: int = 1024
```

**Por que Pydantic Settings?**
- **Validação automática** de variáveis de ambiente
- **Type safety** para configurações
- **SecretStr** para chaves sensíveis
- **Validação customizada** (ex: temperatura entre 0-2)

### 5. **Utilitários (`utils/`)**

#### 5.1 LLM Setup (`llm_setup.py`)
```python
def create_model(api_key: Union[str, SecretStr]) -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o", api_key=api_key)
```

#### 5.2 Logger Setup (`logger_setup.py`)
```python
def setup_logger() -> None:
    # Log no console (colorido)
    logger.add(sys.stdout, colorize=True, level="DEBUG")
    
    # Log em arquivo (rotaciona diariamente)
    logger.add("logs/project.log", rotation="1 day", retention="7 days")
```

## 🚀 Como Executar o Projeto

### 1. **Configuração do Ambiente**
```bash
# Criar arquivo .env
OPENAI_API_KEY=sua_chave_aqui
LANGCHAIN_API_KEY=sua_chave_langsmith
```

### 2. **Execução**
```bash
python main.py "trekking na montanha"
```

### 3. **Output Esperado**
```
==================================================
✨ ROTEIRO DE VIAGEM GERADO COM SUCESSO! ✨
==================================================

📍 Destino Recomendado: Chamonix, França
   Motivo: Localizada nos Alpes franceses, oferece trilhas...

🍴 Restaurantes Recomendados:
   - Le Bistrot (Caseiro): Restaurante familiar com...
   - L'Atelier (Sofisticado): Cozinha francesa moderna...

🏛️ Passeios Culturais:
   - Teleférico Aiguille du Midi: Vista panorâmica...
   - Museu Alpin: História do alpinismo...
```

## 🎓 Conceitos LangChain Aprendidos

### 1. **Chain Composition (Composição de Chains)**
```python
# Forma simples
chain = prompt | model | parser

# Forma complexa (orchestrator)
main_chain = create_main_chain(model)
result = main_chain({"interesse": "trekking"})
```

### 2. **Output Parsing**
```python
# Para objetos simples
parser = JsonOutputParser(pydantic_object=Destino)

# Para objetos complexos
parser = PydanticOutputParser(pydantic_object=ListaRestaurantes)
```

### 3. **Prompt Engineering**
```python
prompt = ChatPromptTemplate.from_template("""
    Contexto: {context}
    Tarefa: {task}
    {format_instructions}
""")
```

### 4. **Error Handling e Fallbacks**
```python
try:
    restaurantes = chain_restaurantes({"cidade": cidade})
except Exception:
    # Fallback: lista vazia
    restaurantes = ListaRestaurantes(restaurantes=[])
```

### 5. **Logging e Observabilidade**
```python
project_logger.debug(f"[Chain Destino] Entrada recebida: {inputs}")
project_logger.debug(f"[Chain Destino] Saída gerada: {output}")
```

## 🔍 Code Review - Pontos de Aprendizado

### ✅ **Pontos Fortes**

1. **Separação de Responsabilidades**
   - Cada chain tem uma responsabilidade específica
   - Orchestrator coordena sem misturar lógicas

2. **Type Safety**
   - Uso consistente de type hints
   - Models Pydantic bem definidos

3. **Error Handling**
   - Try/catch em cada sub-chain
   - Fallbacks para evitar falhas totais

4. **Logging Estruturado**
   - Logs em diferentes níveis (DEBUG, INFO)
   - Rastreamento de entrada/saída de cada chain

5. **Configuração Centralizada**
   - Todas as configurações em um lugar
   - Validação automática de parâmetros

### 🚨 **Pontos de Melhoria**

1. **Async/Await**
   ```python
   # Atual (síncrono)
   destino = chain_destino(inputs)
   restaurantes = chain_restaurantes({"cidade": cidade})
   
   # Melhor (assíncrono)
   destino = await chain_destino(inputs)
   restaurantes, passeios = await asyncio.gather(
       chain_restaurantes({"cidade": cidade}),
       chain_passeios_culturais({"cidade": cidade})
   )
   ```

2. **Retry Logic**
   ```python
   from tenacity import retry, stop_after_attempt
   
   @retry(stop=stop_after_attempt(3))
   def chain_with_retry(inputs):
       return chain.invoke(inputs)
   ```

3. **Cache de Resultados**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_chain_destino(interesse: str):
       return chain_destino({"interesse": interesse})
   ```

4. **Validação de Input**
   ```python
   from pydantic import BaseModel, validator
   
   class InputInteresse(BaseModel):
       interesse: str
       
       @validator('interesse')
       def interesse_deve_ter_minimo(cls, v):
           if len(v.strip()) < 3:
               raise ValueError('Interesse deve ter pelo menos 3 caracteres')
           return v.strip()
   ```

## 🎯 Exercícios Práticos

### Exercício 1: Adicionar Nova Chain
Crie uma chain que sugira **hospedagem** baseada na cidade e tipo de viagem.

### Exercício 2: Implementar Cache
Adicione cache para evitar chamadas repetidas à API para a mesma cidade.

### Exercício 3: Chain Condicional
Crie uma chain que sugira diferentes tipos de passeios baseado no clima da cidade.

### Exercício 4: Validação Avançada
Implemente validação que verifica se a cidade sugerida realmente existe.

## 📚 Recursos Adicionais

- [LangChain Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangSmith Tracing](https://smith.langchain.com/)
- [Loguru Documentation](https://loguru.readthedocs.io/)

## 🎉 Conclusão

Este projeto demonstra **padrões fundamentais** do LangChain:
- **Composição de chains** para resolver problemas complexos
- **Output parsing** para estruturar respostas
- **Error handling** para robustez
- **Logging** para observabilidade
- **Configuração** para flexibilidade

É um excelente ponto de partida para entender como construir sistemas de IA conversacional robustos e escaláveis!
