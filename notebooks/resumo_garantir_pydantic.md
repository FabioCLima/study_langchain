# Como Garantir que a Saída seja um Objeto Pydantic

## 🎯 **OPÇÃO 1: PydanticOutputParser (RECOMENDADO)**

```python
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Destino)
chain = prompt | model | parser
response = chain.invoke({"interesse": "ecoturismo"})

# response será SEMPRE um objeto Pydantic
print(type(response))  # <class '__main__.Destino'>
print(response.cidade)  # ✅ Funciona
```

**✅ Vantagens:**
- Sempre retorna objeto Pydantic
- Mais previsível
- Melhor validação de tipos
- Menos código defensivo

## 🔧 **OPÇÃO 2: Converter dicionário para Pydantic**

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=Destino)
chain = prompt | model | parser
response_dict = chain.invoke({"interesse": "ecoturismo"})

# Converter se necessário
if isinstance(response_dict, dict):
    response_pydantic = Destino(**response_dict)
    print(response_pydantic.cidade)  # ✅ Funciona
```

## 🛠️ **OPÇÃO 3: Função helper**

```python
def garantir_pydantic(response: Any, model_class: type) -> BaseModel:
    if isinstance(response, model_class):
        return response
    elif isinstance(response, dict):
        return model_class(**response)
    else:
        raise ValueError(f"Tipo não suportado: {type(response)}")

# Uso
response_garantido = garantir_pydantic(response_dict, Destino)
```

## 📊 **Comparação dos Parsers**

| Parser | Retorna | Previsibilidade | Validação |
|--------|---------|----------------|-----------|
| `JsonOutputParser` | dict ou Pydantic | Baixa | Básica |
| `PydanticOutputParser` | Sempre Pydantic | Alta | Completa |

## 🎯 **Recomendação**

**Use `PydanticOutputParser` quando:**
- Precisar garantir objetos Pydantic
- Quiser validação de tipos robusta
- Precisar de código mais limpo e previsível

**Use `JsonOutputParser` quando:**
- Precisar de flexibilidade
- Estiver trabalhando com APIs que esperam dicionários
- Quiser compatibilidade com código legado

## 🔄 **Migração do seu código atual**

```python
# ❌ Antes (pode dar erro)
parser_destino = JsonOutputParser(pydantic_object=Destino)

# ✅ Depois (garantido)
parser_destino = PydanticOutputParser(pydantic_object=Destino)
```

Apenas mude o import e o nome da classe - o resto do código permanece igual!
