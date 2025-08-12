# Guia de Estilo de Documentação - Google Style

## 📚 Por que Documentação Estilo Google?

A documentação estilo Google é uma convenção amplamente adotada no Python que torna o código **muito mais legível** para o seu "eu futuro" e outros desenvolvedores.

### 🎯 **Benefícios:**

- ✅ **Auto-documentação**: O código se explica sozinho
- ✅ **Facilita revisão**: Seu "eu futuro" agradece!
- ✅ **Padrão da indústria**: Usado por Google, Facebook, etc.
- ✅ **Compatível com ferramentas**: Sphinx, PyDoc, IDEs
- ✅ **Facilita debugging**: Entender o que cada função faz

## 📝 **Estrutura da Documentação**

### **1. Docstring do Módulo (Topo do arquivo)**
```python
"""
Nome do módulo.

Descrição detalhada do que o módulo faz.

Exemplo de uso:
    from meu_modulo import minha_funcao
    resultado = minha_funcao(parametro)
"""
```

### **2. Docstring da Classe**
```python
class MinhaClasse:
    """
    Descrição da classe.
    
    Esta classe faz X, Y e Z para resolver o problema A.
    
    Attributes:
        atributo1 (tipo): Descrição do atributo
        atributo2 (tipo): Descrição do atributo
    
    Example:
        # Como criar uma instância
        obj = MinhaClasse()
        obj.fazer_algo()
    
    Note:
        Informações importantes sobre uso ou limitações.
    """
```

### **3. Docstring de Funções/Métodos**
```python
def minha_funcao(param1: str, param2: int) -> bool:
    """
    Descrição do que a função faz.
    
    Esta função recebe X e Y, processa Z e retorna W.
    
    Args:
        param1 (str): Descrição do primeiro parâmetro
        param2 (int): Descrição do segundo parâmetro
    
    Returns:
        bool: Descrição do que é retornado
    
    Raises:
        ValueError: Quando param2 é negativo
        TypeError: Quando param1 não é string
    
    Example:
        resultado = minha_funcao("texto", 42)
        if resultado:
            print("Sucesso!")
    
    Note:
        Esta função é thread-safe e pode ser chamada múltiplas vezes.
    """
```

### **4. Docstring de Atributos**
```python
class MinhaClasse:
    atributo: str = "valor_padrao"
    """Descrição do atributo e seu propósito."""
    
    outro_atributo: int
    """
    Descrição mais detalhada do atributo.
    
    Este atributo é usado para X e deve ser sempre positivo.
    """
```

## 🚀 **Exemplos Práticos do Nosso Projeto**

### **Configuração (config.py)**
```python
class Settings(BaseSettings):
    """
    Configurações do projeto com validação automática de tipos.
    
    Esta classe herda de BaseSettings do Pydantic, permitindo carregamento
    automático de variáveis de ambiente e validação de tipos.
    
    Attributes:
        openai_api_key (SecretStr): Chave da API OpenAI (obrigatória)
        model_name (str): Nome do modelo GPT (padrão: "gpt-4.1")
    
    Example:
        settings = Settings()
        api_key = settings.openai_api_key.get_secret_value()
    """
```

### **Função de Teste (test_config.py)**
```python
def test_config() -> bool:
    """
    Testa se a configuração pode ser importada sem erros.
    
    Esta função tenta importar o módulo de configuração e acessar
    suas propriedades básicas para verificar se está funcionando.
    
    Returns:
        bool: True se a configuração foi carregada com sucesso, False caso contrário.
    
    Example:
        success = test_config()
        if success:
            print("✅ Configuração funcionando!")
    """
```

## 🔧 **Ferramentas que Aproveitam a Documentação**

### **1. IDEs e Editores**
- **VS Code**: Mostra documentação ao passar o mouse
- **PyCharm**: Autocomplete com documentação
- **Vim/Emacs**: Plugins para exibir docstrings

### **2. Geração de Documentação**
```bash
# Gerar documentação HTML
pydoc -w config.py

# Usar Sphinx para documentação completa
sphinx-quickstart
make html
```

### **3. Verificação de Qualidade**
```bash
# Verificar se docstrings estão corretas
python -m pydocstyle config.py

# Verificar tipos e documentação
python -m mypy config.py
```

## 📋 **Checklist para Documentação**

- [ ] **Módulo**: Docstring explicando propósito e uso
- [ ] **Classes**: Descrição, atributos e exemplos
- [ ] **Funções**: Args, returns, raises e exemplos
- [ ] **Atributos**: Descrição clara do propósito
- [ ] **Exemplos**: Código que pode ser copiado e executado
- [ ] **Notas**: Informações importantes sobre uso

## 🎉 **Resultado Final**

Com documentação estilo Google, seu código se torna:

- 📖 **Auto-explicativo**
- 🔍 **Fácil de debugar**
- 👥 **Colaborativo**
- 🚀 **Profissional**
- 💡 **Inteligente para IDEs**

**Lembre-se**: Documentar bem hoje = Menos tempo debugando amanhã! 🎯
