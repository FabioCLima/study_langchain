# 🎯 Exercícios Práticos - Roteiro de Viagem

## 🚀 Exercício 1: Adicionar Chain de Hospedagem

### Objetivo
Criar uma nova chain que sugira hospedagem baseada na cidade e tipo de viagem.

### Passos

#### 1.1 Criar Modelo Pydantic
```python
# models/pydantic_models.py
class Hospedagem(BaseModel):
    nome: str = Field(description="Nome do hotel/pousada")
    tipo: str = Field(description="Tipo de hospedagem (hotel, pousada, hostel, resort)")
    categoria: str = Field(description="Categoria (econômica, média, luxo)")
    descricao: str = Field(description="Descrição da hospedagem")
    preco_medio: str = Field(description="Faixa de preço (ex: R$ 100-200)")

class ListaHospedagem(BaseModel):
    hospedagens: list[Hospedagem]
```

#### 1.2 Criar Chain de Hospedagem
```python
# chains/chain_hospedagem.py
def create_chain_hospedagem(model: ChatOpenAI) -> Callable[[dict[str, Any]], ListaHospedagem]:
    parser = PydanticOutputParser(pydantic_object=ListaHospedagem)
    
    prompt = ChatPromptTemplate.from_template("""
        Para a cidade {cidade}, sugira 3 opções de hospedagem considerando:
        - Tipo de viagem: {tipo_viagem}
        - Diferentes faixas de preço
        - Variedade de tipos (hotel, pousada, hostel)
        
        {format_instructions}
    """)
    
    chain: Runnable[dict[str, Any], ListaHospedagem] = prompt | model | parser
    return chain
```

## 🔄 Exercício 2: Implementar Cache

### Objetivo
Adicionar cache para evitar chamadas repetidas à API para a mesma cidade.

### Implementação Básica
```python
# utils/cache_manager.py
from functools import lru_cache
import hashlib
import json

class SimpleCache:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._cache = {}
    
    def _generate_key(self, chain_name: str, **kwargs) -> str:
        """Gera chave única para o cache"""
        sorted_params = sorted(kwargs.items())
        params_str = json.dumps(sorted_params, sort_keys=True)
        return f"chain_{chain_name}_{hashlib.md5(params_str.encode()).hexdigest()}"
    
    def get(self, chain_name: str, **kwargs):
        key = self._generate_key(chain_name, **kwargs)
        return self._cache.get(key)
    
    def set(self, chain_name: str, value, **kwargs):
        key = self._generate_key(chain_name, **kwargs)
        if len(self._cache) >= self.max_size:
            # Remove item mais antigo
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[key] = value

# Instância global
simple_cache = SimpleCache()
```

## 🌦️ Exercício 3: Chain Condicional Baseada no Clima

### Objetivo
Criar uma chain que sugira diferentes tipos de passeios baseado no clima da cidade.

### Implementação
```python
# chains/chain_passeios_condicional.py
def create_chain_passeios_condicional(model: ChatOpenAI) -> Callable[[dict[str, Any]], ListaAtracoes]:
    chain_passeios = create_chain_passeios_culturais(model)
    
    def run_conditional(inputs: dict[str, Any]) -> ListaAtracoes:
        cidade = inputs["cidade"]
        clima = inputs.get("clima", "neutro")
        
        # Ajustar prompt baseado no clima
        if clima == "chuvoso":
            prompt_ajustado = f"""
            Para a cidade {cidade} (clima chuvoso), sugira 3 passeios INDOOR:
            - Museus, teatros, centros culturais
            - Atividades que não sejam afetadas pela chuva
            """
        elif clima == "ensolarado":
            prompt_ajustado = f"""
            Para a cidade {cidade} (clima ensolarado), sugira 3 passeios AO AR LIVRE:
            - Parques, trilhas, praças
            - Atividades que aproveitem o bom tempo
            """
        else:
            prompt_ajustado = f"""
            Para a cidade {cidade} (clima {clima}), sugira 3 passeios culturais
            considerando as condições climáticas atuais.
            """
        
        # Executar chain com prompt ajustado
        return chain_passeios(inputs)
    
    return run_conditional
```

## ✅ Exercício 4: Validação Avançada de Cidade

### Objetivo
Implementar validação que verifica se a cidade sugerida realmente existe.

### Implementação
```python
# chains/chain_validacao.py
from models.pydantic_models import ValidacaoCidade

class ValidacaoCidade(BaseModel):
    cidade: str
    existe: bool
    pais: str
    coordenadas: Optional[str] = None
    populacao: Optional[str] = None
    justificativa: str

def create_chain_validacao(model: ChatOpenAI) -> Callable[[dict[str, Any]], ValidacaoCidade]:
    parser = PydanticOutputParser(pydantic_object=ValidacaoCidade)
    
    prompt = ChatPromptTemplate.from_template("""
        Valide se a cidade "{cidade}" realmente existe:
        
        - existe: true/false
        - pais: país onde está localizada
        - coordenadas: latitude,longitude (se existir)
        - populacao: população aproximada
        - justificativa: explicação da validação
        
        {format_instructions}
    """)
    
    chain: Runnable[dict[str, Any], ValidacaoCidade] = prompt | model | parser
    return chain
```

## 🔧 Exercício 5: Implementar Retry Logic

### Objetivo
Adicionar lógica de retry para tornar as chains mais robustas.

### Implementação
```python
# utils/retry_decorator.py
import time
from functools import wraps
from typing import Callable, Any

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        project_logger.warning(
                            f"Tentativa {attempt + 1} falhou: {e}. "
                            f"Tentando novamente em {delay}s..."
                        )
                        time.sleep(delay)
                    else:
                        project_logger.error(f"Todas as {max_attempts} tentativas falharam")
                        raise last_exception
            
            return None
        
        return wrapper
    return decorator
```

## 🎯 Exercício 6: Chain de Análise de Sentimento

### Objetivo
Criar uma chain que analise o sentimento do interesse do usuário para personalizar as recomendações.

### Implementação
```python
# models/pydantic_models.py
class AnaliseSentimento(BaseModel):
    interesse: str
    sentimento: str  # "positivo", "neutro", "negativo"
    intensidade: str  # "baixa", "média", "alta"
    emocoes: list[str]  # ["aventura", "tranquilidade", "cultura"]
    recomendacao_personalizada: str

# chains/chain_sentimento.py
def create_chain_sentimento(model: ChatOpenAI) -> Callable[[dict[str, Any]], AnaliseSentimento]:
    parser = PydanticOutputParser(pydantic_object=AnaliseSentimento)
    
    prompt = ChatPromptTemplate.from_template("""
        Analise o sentimento e emoções por trás do interesse: "{interesse}"
        
        Considere:
        - Sentimento geral (positivo/neutro/negativo)
        - Intensidade da emoção
        - Emoções específicas (aventura, tranquilidade, cultura, etc.)
        - Recomendação personalizada baseada na análise
        
        {format_instructions}
    """)
    
    chain: Runnable[dict[str, Any], AnaliseSentimento] = prompt | model | parser
    return chain
```

## 🎉 Conclusão dos Exercícios

Estes exercícios demonstram como:

1. **Estender** o sistema com novas funcionalidades
2. **Melhorar** a robustez com cache e retry
3. **Implementar** lógica condicional baseada em dados externos
4. **Validar** dados de entrada de forma robusta
5. **Personalizar** respostas baseado em análise de sentimento

Cada exercício pode ser implementado independentemente, permitindo aprendizado incremental e gradual do LangChain!
