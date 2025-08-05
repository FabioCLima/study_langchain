# Multi-Step Workflow em LangChain: Guia Completo

## 📋 Visão Geral

Este exercício demonstra como construir um **workflow multi-etapas** usando o **Language Chain Expression Language (LCEL)** do LangChain. O objetivo é criar um "AI Business Advisor" que:

1. **Aceita** uma indústria como entrada
2. **Gera** uma ideia de negócio
3. **Analisa** pontos fortes e fracos
4. **Formata** os resultados em um relatório estruturado

## 🏗️ Arquitetura do Sistema

### Estratégia de Decomposição

O problema foi **decomposto** em componentes menores e mais gerenciáveis:

```
Input (Industry) 
    ↓
[1] Idea Generation Chain
    ↓
[2] Analysis Chain  
    ↓
[3] Report Generation Chain
    ↓
Output (Structured Report)
```

### Componentes Principais

#### 1. **Idea Generation Chain**
```python
idea_prompt = PromptTemplate(
    template=(
        "You are a creative business advisor. "
        "Generate one innovative business idea in the industry: "
        "{industry}. "
        "Provide a brief description of the idea."
    )
)

idea_chain = (
    idea_prompt 
    | llm 
    | parse_and_log_output_chain
)
```

#### 2. **Analysis Chain**
```python
analysis_prompt = PromptTemplate(
    template=(
        "Analyze the following business idea: "
        "Idea: {idea} "
        "Identify 3 key strengths and 3 potential weaknesses of the idea."
    )
)

analysis_chain = (
    analysis_prompt 
    | llm 
    | parse_and_log_output_chain
)
```

#### 3. **Report Generation Chain**
```python
class AnalysisReport(BaseModel):
    """Strengths and Weaknesses about a business idea"""
    strengths: list = Field(default=[], description="Idea's strength list")
    weaknesses: list = Field(default=[], description="Idea's weaknesse list")

report_chain = (
    report_prompt | llm.with_structured_output(schema=AnalysisReport, method="function_calling")
)
```

## 🔄 RunnablePassthrough: O Coração da Composição

### O que é RunnablePassthrough?

`RunnablePassthrough` é um **operador de fluxo de dados** que permite:
- **Preservar** dados de entrada
- **Adicionar** novos dados ao fluxo
- **Combinar** múltiplas cadeias de forma flexível

### Como Funciona

```python
e2e_chain = ( 
    RunnablePassthrough() 
    | idea_chain
    | RunnableParallel(idea=RunnablePassthrough())
    | analysis_chain
    | report_chain
)
```

### Explicação Detalhada

1. **`RunnablePassthrough()` inicial**: Preserva a entrada original (industry)
2. **`idea_chain`**: Processa a entrada e gera uma ideia
3. **`RunnableParallel(idea=RunnablePassthrough())`**: 
   - Cria um dicionário com a chave "idea"
   - O valor é o resultado da ideia gerada
   - Preserva outros dados do fluxo
4. **`analysis_chain`**: Analisa a ideia gerada
5. **`report_chain`**: Formata tudo em um relatório estruturado

### Exemplo de Fluxo de Dados

```python
# Entrada inicial
{"industry": "agro"}

# Após idea_chain
{
    "industry": "agro",
    "output": "Business idea: AgriLoop Circular Solutions..."
}

# Após RunnableParallel
{
    "industry": "agro", 
    "idea": "Business idea: AgriLoop Circular Solutions...",
    "output": "Business idea: AgriLoop Circular Solutions..."
}

# Após analysis_chain
{
    "industry": "agro",
    "idea": "Business idea: AgriLoop Circular Solutions...",
    "output": "Strengths: [...], Weaknesses: [...]"
}
```

## 🧩 Conceitos-Chave do LCEL

### 1. **Composição com `|` (Pipe)**
```python
chain = prompt | llm | parser
```
- Cada componente se conecta ao próximo
- Dados fluem automaticamente entre etapas

### 2. **RunnableParallel**
```python
RunnableParallel(
    output=parser, 
    log=RunnableLambda(lambda x: logs.append(x))
)
```
- Executa múltiplas operações em paralelo
- Combina resultados em um dicionário

### 3. **RunnableLambda**
```python
RunnableLambda(lambda x: logs.append(x))
```
- Permite funções customizadas no fluxo
- Útil para logging, transformações, etc.

### 4. **Structured Output**
```python
llm.with_structured_output(schema=AnalysisReport, method="function_calling")
```
- Garante saída estruturada e tipada
- Facilita integração com sistemas

## 📊 Sistema de Logging

```python
logs = []

parse_and_log_output_chain = RunnableParallel(
    output=parser, 
    log=RunnableLambda(lambda x: logs.append(x))
)
```

**Benefícios:**
- **Rastreabilidade**: Todas as chamadas são registradas
- **Debugging**: Fácil identificação de problemas
- **Análise**: Métricas de uso e performance

## 🎯 Estrutura de Dados Pydantic

```python
class AnalysisReport(BaseModel):
    """Strengths and Weaknesses about a business idea"""
    strengths: list = Field(default=[], description="Idea's strength list")
    weaknesses: list = Field(default=[], description="Idea's weaknesse list")
```

**Vantagens:**
- **Validação automática** de dados
- **Documentação** clara da estrutura
- **Integração** fácil com APIs

## 🚀 Preparação para o Projeto Final

### 1. **Domine os Conceitos Fundamentais**

#### ✅ O que você já entendeu:
- Decomposição de problemas complexos
- Composição de chains com `|`
- Uso básico de prompts e LLMs
- Estruturação de dados com Pydantic

#### 🔄 O que precisa praticar mais:
- **RunnablePassthrough** e fluxo de dados
- **RunnableParallel** para operações paralelas
- **RunnableLambda** para customizações
- **Structured Output** para APIs robustas

### 2. **Próximos Passos Recomendados**

#### A. **Experimente com RunnablePassthrough**
```python
# Exemplo: Preservar dados originais
chain = (
    RunnablePassthrough.assign(
        processed_data=processing_chain
    )
    | final_chain
)
```

#### B. **Explore Operações Paralelas**
```python
# Exemplo: Múltiplas análises simultâneas
parallel_chain = RunnableParallel(
    sentiment=sentiment_analyzer,
    keywords=keyword_extractor,
    summary=summarizer
)
```

#### C. **Implemente Validação Robusta**
```python
from pydantic import BaseModel, validator

class ValidatedOutput(BaseModel):
    content: str
    confidence: float
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v
```

### 3. **Estratégias para o Projeto Final**

#### A. **Arquitetura Modular**
- Divida seu projeto em **módulos independentes**
- Use **interfaces bem definidas** entre componentes
- Implemente **padrões de design** consistentes

#### B. **Gestão de Estado**
```python
# Exemplo: Context Manager
class WorkflowContext:
    def __init__(self):
        self.logs = []
        self.metrics = {}
    
    def add_log(self, entry):
        self.logs.append(entry)
    
    def get_metrics(self):
        return self.metrics
```

#### C. **Tratamento de Erros**
```python
from langchain_core.runnables import RunnableConfig

def safe_chain_with_fallback(chain, fallback_chain):
    def wrapper(input_data, config: RunnableConfig = None):
        try:
            return chain.invoke(input_data, config)
        except Exception as e:
            print(f"Primary chain failed: {e}")
            return fallback_chain.invoke(input_data, config)
    return wrapper
```

#### D. **Testes e Validação**
```python
import pytest
from langchain_core.runnables import RunnableConfig

def test_workflow_chain():
    # Arrange
    test_input = {"industry": "tech"}
    
    # Act
    result = e2e_chain.invoke(test_input)
    
    # Assert
    assert hasattr(result, 'strengths')
    assert hasattr(result, 'weaknesses')
    assert len(result.strengths) > 0
    assert len(result.weaknesses) > 0
```

### 4. **Tecnologias Avançadas para Explorar**

#### A. **Memory e Context**
```python
from langchain_core.memory import BaseMemory

class ConversationMemory(BaseMemory):
    def __init__(self):
        self.messages = []
    
    def load_memory_variables(self, inputs):
        return {"history": self.messages}
    
    def save_context(self, inputs, outputs):
        self.messages.extend([inputs, outputs])
```

#### B. **Callbacks e Observabilidade**
```python
from langchain_core.callbacks import BaseCallbackHandler

class MetricsCallback(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Starting chain: {serialized['name']}")
    
    def on_chain_end(self, outputs, **kwargs):
        print(f"Chain completed with {len(outputs)} outputs")
```

#### C. **Caching e Performance**
```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())
```

### 5. **Checklist para o Projeto Final**

#### ✅ **Funcionalidades Básicas**
- [ ] Workflow multi-etapas bem definido
- [ ] Tratamento de erros robusto
- [ ] Logging e observabilidade
- [ ] Validação de dados de entrada/saída

#### ✅ **Funcionalidades Avançadas**
- [ ] Sistema de memória/contexto
- [ ] Operações paralelas quando apropriado
- [ ] Cache para performance
- [ ] Testes automatizados

#### ✅ **Qualidade de Código**
- [ ] Documentação clara
- [ ] Estrutura modular
- [ ] Configuração flexível
- [ ] Deploy e monitoramento

## 🎓 Conclusão

O **RunnablePassthrough** é essencial para workflows complexos porque permite:
- **Preservar contexto** através das etapas
- **Combinar dados** de múltiplas fontes
- **Manter flexibilidade** na composição de chains

Para o projeto final, foque em:
1. **Arquitetura limpa** e modular
2. **Tratamento robusto de erros**
3. **Observabilidade** completa
4. **Testes** abrangentes
5. **Documentação** detalhada

Lembre-se: **LCEL é sobre composição**. Quanto mais você praticar a combinação de componentes, mais natural se tornará a construção de sistemas complexos.

---

*Este documento serve como referência para seu estudo e pode ser exportado para o Obsidian para consulta futura.* 