# Guia para Dominar Chains no LangChain

## 📚 Visão Geral

Chains são o coração do LangChain - elas conectam diferentes componentes (prompts, modelos, parsers) em fluxos de processamento. Este guia apresenta um caminho estruturado para dominar o uso de chains.

## 🎯 Fluxo de Etapas Padrão

### 1. **Imports e Setup**
```python
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI  # type: ignore
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_core.output_parsers import StrOutputParser  # type: ignore
import os

# Setup do ambiente
_ = load_dotenv(find_dotenv())
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não encontrada")
```

### 2. **Configuração do Modelo**
```python
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,  # 0.0 = determinístico, 1.0 = muito criativo
    max_tokens=1000
)  # type: ignore
```

### 3. **Definição do Prompt**
```python
prompt = ChatPromptTemplate.from_template(
    "Você é um assistente especializado em {domain}. "
    "Responda a pergunta: {question}"
)
```

### 4. **Configuração do Output Parser**
```python
output_parser = StrOutputParser()
```

### 5. **Criação da Chain**
```python
# Usando LCEL (LangChain Expression Language)
chain = prompt | model | output_parser
```

### 6. **Execução e Tratamento de Erros**
```python
try:
    response = chain.invoke({"domain": "tech", "question": "O que é AI?"})
except Exception as e:
    print(f"Erro: {e}")
```

### 7. **Validação e Testes**
```python
def validate_response(response: str) -> bool:
    return len(response.strip()) > 10
```

## 🚀 Recomendações para Progressão

### **Nível Iniciante (1-2 semanas)**
1. **Entenda os Conceitos Básicos**
   - O que é uma chain
   - Diferença entre prompt, modelo e parser
   - Como o LCEL funciona (operador `|`)

2. **Pratique com Exemplos Simples**
   - Chain básica: prompt → modelo → parser
   - Experimente diferentes temperatures
   - Teste diferentes modelos

3. **Exercícios Recomendados**
   - Crie uma chain que traduza textos
   - Faça uma chain que resuma parágrafos
   - Implemente uma chain de Q&A simples

### **Nível Intermediário (3-4 semanas)**
1. **Explore Output Parsers Avançados**
   ```python
   from langchain_core.output_parsers import JsonOutputParser
   from pydantic import BaseModel
   
   class Response(BaseModel):
       answer: str
       confidence: float
   
   parser = JsonOutputParser(pydantic_object=Response)
   ```

2. **Use RunnablePassthrough para Dados Dinâmicos**
   ```python
   from langchain_core.runnables import RunnablePassthrough
   
   chain = (
       {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
       | prompt
       | model
       | output_parser
   )
   ```

3. **Implemente Chains Condicionais**
   ```python
   from langchain_core.runnables import RunnableBranch
   
   def route_by_length(input_dict):
       if len(input_dict["text"]) > 100:
           return "summarize"
       return "translate"
   
   chain = RunnableBranch(
       route_by_length,
       {"summarize": summarize_chain, "translate": translate_chain}
   )
   ```

### **Nível Avançado (5-8 semanas)**
1. **Chains Complexas com Múltiplos Passos**
   ```python
   chain = (
       {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
       | prompt
       | model
       | output_parser
       | {"original": RunnablePassthrough(), "processed": RunnablePassthrough()}
       | final_prompt
       | final_model
   )
   ```

2. **Integração com Memória**
   ```python
   from langchain_core.memory import ConversationBufferMemory
   
   memory = ConversationBufferMemory(return_messages=True)
   chain = prompt | model | output_parser
   chain_with_memory = memory | chain
   ```

3. **Chains com Tool Calling**
   ```python
   from langchain_core.tools import tool
   
   @tool
   def search_web(query: str) -> str:
       return f"Resultados para: {query}"
   
   chain = prompt | model.bind_tools([search_web]) | output_parser
   ```

## 🛠️ Melhores Práticas

### **1. Organização do Código**
- Separe cada componente em funções
- Use type hints para clareza
- Documente seus prompts e parâmetros

### **2. Tratamento de Erros**
```python
def safe_chain_execution(chain, input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Tentativa {attempt + 1} falhou: {e}")
```

### **3. Validação de Entrada/Saída**
```python
from pydantic import BaseModel, Field

class ChainInput(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    context: str = Field(default="")

class ChainOutput(BaseModel):
    answer: str
    confidence: float = Field(..., ge=0.0, le=1.0)
```

### **4. Logging e Monitoramento**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_chain_execution(input_data, output, execution_time):
    logger.info(f"Chain executada em {execution_time:.2f}s")
    logger.debug(f"Input: {input_data}")
    logger.debug(f"Output: {output}")
```

## 📊 Métricas de Progresso

### **Checklist Iniciante**
- [ ] Entendo o que é uma chain
- [ ] Posso criar uma chain básica
- [ ] Sei ajustar temperature e outros parâmetros
- [ ] Consigo tratar erros básicos

### **Checklist Intermediário**
- [ ] Uso output parsers avançados
- [ ] Implemento chains condicionais
- [ ] Trabalho com RunnablePassthrough
- [ ] Crio prompts complexos e estruturados

### **Checklist Avançado**
- [ ] Construo chains multi-step complexas
- [ ] Integro com memória e contexto
- [ ] Uso tool calling
- [ ] Implemento validação robusta
- [ ] Otimizo performance e custos

## 🎯 Projetos Práticos Sugeridos

### **Projeto 1: Chatbot Especializado**
- Chain que responde perguntas sobre um domínio específico
- Integração com memória de conversa
- Validação de respostas

### **Projeto 2: Sistema de Análise de Texto**
- Chain que analisa sentimentos
- Chain que extrai entidades
- Chain que gera resumos

### **Projeto 3: Assistente de Código**
- Chain que analisa código Python
- Chain que sugere melhorias
- Chain que explica conceitos de programação

## 🔧 Recursos Adicionais

### **Documentação Oficial**
- [LangChain Core](https://python.langchain.com/docs/langchain_core)
- [LCEL Guide](https://python.langchain.com/docs/langchain_core/expression_language/)
- [Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)

### **Ferramentas Úteis**
- LangSmith para debugging
- LangChain Hub para prompts pré-construídos
- LangGraph para workflows complexos

## 💡 Dicas Finais

1. **Comece Simples**: Não tente construir chains complexas logo no início
2. **Teste Frequentemente**: Valide cada componente individualmente
3. **Documente**: Mantenha um log dos seus experimentos
4. **Otimize**: Monitore custos e performance
5. **Reutilize**: Crie componentes modulares que podem ser reutilizados

---

*Este guia deve ser usado como referência durante sua jornada de aprendizado. Cada pessoa tem seu próprio ritmo - não se pressione para avançar rapidamente. Foque em entender profundamente cada conceito antes de passar para o próximo.*