# OutputParsers - Exemplos Práticos com Datetime e Boolean

Este diretório contém exemplos práticos de OutputParsers no LangChain, focando em trabalhar com **datetime** e **boolean**.

## 📁 Arquivos

- `output_parsers_datetime_boolean.py` - Exemplos completos de OutputParsers
- `README.md` - Este arquivo explicativo

## 🎯 Conceitos Demonstrados

### 1. **OutputParser com Datetime**

**Problema**: Extrair informações de data e hora de textos naturais.

**Solução**: Usar Pydantic com campos `datetime` para estruturar a saída.

```python
class EventInfo(BaseModel):
    event_name: str
    event_date: datetime  # ← Campo datetime
    duration_hours: Optional[float]
    is_recurring: bool
```

**Exemplo de uso**:
```python
text = "Reunião de equipe amanhã às 14:30 por 2 horas"
# Resultado: EventInfo com event_date = datetime(2024, 12, 16, 14, 30)
```

### 2. **OutputParser com Boolean**

**Problema**: Analisar sentimento e flags de status em textos.

**Solução**: Usar campos `bool` para classificação binária.

```python
class SentimentAnalysis(BaseModel):
    text: str
    is_positive: bool      # ← Campo boolean
    is_negative: bool      # ← Campo boolean
    is_neutral: bool       # ← Campo boolean
    contains_urgency: bool # ← Campo boolean
    confidence_score: float
```

**Exemplo de uso**:
```python
text = "Adorei o produto! Funciona perfeitamente."
# Resultado: is_positive=True, is_negative=False, is_neutral=False
```

### 3. **OutputParser Combinado (Datetime + Boolean)**

**Problema**: Analisar compromissos com data/hora e flags de prioridade.

**Solução**: Combinar campos `datetime` e `bool` no mesmo modelo.

```python
class AppointmentAnalysis(BaseModel):
    appointment_date: datetime  # ← Datetime
    is_urgent: bool           # ← Boolean
    is_important: bool        # ← Boolean
    requires_preparation: bool # ← Boolean
    is_online: bool          # ← Boolean
```

### 4. **OutputParser com Validação Customizada**

**Problema**: Validar datas futuras e lógica de conclusão de tarefas.

**Solução**: Usar validators do Pydantic.

```python
class ValidatedTask(BaseModel):
    task_name: str
    due_date: datetime
    is_completed: bool
    is_high_priority: bool
    
    @validator('due_date')
    def validate_future_date(cls, v):
        if v < datetime.now():
            raise ValueError('Data deve estar no futuro')
        return v
```

## 🚀 Como Executar

1. **Configure o ambiente**:
```bash
pip install langchain-openai pydantic python-dotenv
```

2. **Configure a API Key**:
```bash
# Crie um arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

3. **Execute o exemplo**:
```bash
python output_parsers_datetime_boolean.py
```

## 📊 Saída Esperada

```
🚀 OUTPUTPARSERS - EXEMPLOS PRÁTICOS
============================================================

🎯 EXEMPLO 1: OutputParser com Datetime
============================================================

📋 Exemplo 1:
Texto: Reunião de equipe amanhã às 14:30 por 2 horas
📅 Reunião de equipe (Único)
   📆 16/12/2024 às 14:30 - Duração: 2.0h
----------------------------------------

🎯 EXEMPLO 2: OutputParser com Boolean
============================================================

📋 Exemplo 1:
📝 TEXTO: Adorei o produto! Funciona perfeitamente e superou minhas expectativas.
😊 POSITIVO
⏰ Urgência: Não
📊 Confiança: ██████████ 100.0%
----------------------------------------
```

## 🎯 Casos de Uso Práticos

### **Datetime Parsers**
- **Agendamento**: Extrair compromissos de emails/textos
- **Logs**: Analisar timestamps em logs de sistema
- **Relatórios**: Processar datas em relatórios

### **Boolean Parsers**
- **Análise de Sentimento**: Classificar feedback de clientes
- **Filtros**: Marcar conteúdo como urgente/importante
- **Validação**: Verificar se dados estão completos

### **Parsers Combinados**
- **Gerenciamento de Tarefas**: Data + prioridade + status
- **CRM**: Contatos + urgência + importância
- **Sistema de Tickets**: Data + urgência + categoria

## 🔧 Benefícios dos OutputParsers

1. **Type Safety**: Validação automática de tipos
2. **Estruturação**: Respostas sempre no formato esperado
3. **Integração**: Fácil uso com APIs e bancos de dados
4. **Manutenibilidade**: Código mais limpo e organizado
5. **Documentação**: Auto-documentação com Pydantic

## 📚 Conceitos Importantes

### **Pydantic + LangChain**
- Pydantic fornece validação e serialização
- LangChain integra com LLMs para parsing estruturado
- Combinação garante dados consistentes

### **Validação Customizada**
- Use `@validator` para regras específicas
- Valide relacionamentos entre campos
- Capture erros de validação graciosamente

### **Formatação de Saída**
- Crie métodos `display_*()` para saída legível
- Use emojis e formatação para melhor UX
- Mantenha consistência visual

## 🎓 Próximos Passos

1. **Explore outros tipos**: List, Dict, Enum
2. **Crie validadores complexos**: Regras de negócio específicas
3. **Integre com APIs**: Use parsers para estruturar respostas de APIs
4. **Teste com diferentes LLMs**: Compare resultados entre modelos

---

**Autor**: Tutor LangChain  
**Data**: 2024  
**Versão**: 1.0 