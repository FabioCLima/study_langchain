# 🤖 Assistant Questions Project

> An intelligent question-answering system that enhances user queries and provides context-aware responses using LangGraph, LangChain, and specialized AI agents.

## 📋 **Project Overview**

### **Purpose & Vision**
This project creates a flexible AI assistant that:
1. **Receives** a specialization from the user (e.g., "Python", "Data Science", "DevOps")
2. **Adopts** that specialized role for the conversation
3. **Enhances** user questions using LLM capabilities
4. **Provides** expert-level answers within that specialization
5. **Admits limitations** when questions are outside the specialist's knowledge

### **Evolution**
- **V1.0**: Fixed Python-specific assistant
- **V2.0**: User-defined specialist assistant ← *Current Goal*

### **Key Innovation**
Unlike generic chatbots, this system:
- 🎭 **Becomes any specialist** the user defines
- ✨ **Enhances questions** before processing (better understanding)
- 🧠 **Uses LangGraph** for intelligent workflow orchestration
- ❌ **Admits "I don't know"** when outside expertise area
- 🎯 **Provides expert-level responses** within chosen domain

---

## 🏗️ **Technical Architecture**

### **Core Technologies**
- **🕸️ LangGraph**: Workflow orchestration and agent coordination
- **🔗 LangChain**: LLM integration and chain management
- **🐍 Python**: Core implementation language
- **🤖 LLM**: Question enhancement and specialized responses

### **System Workflow**
```mermaid
flowchart TD
    A[User: "You are a {SPECIALIZATION} expert"] --> B[System: Set Specialist Role]
    B --> C[User: Asks Question]
    C --> D[Question Enhancement Agent]
    D --> E[Enhanced Question]
    E --> F[Specialist Agent Response]
    F --> G{Within Expertise?}
    G -->|Yes| H[Expert Answer]
    G -->|No| I["I don't know this question"]
    H --> J[Final Answer to User]
    I --> J
```

### **Specialist Types (User-Defined)**
- 🐍 **Python**: Programming, libraries, syntax, best practices
- 📊 **Data Science**: Analytics, ML, statistics, pandas, numpy
- 🏗️ **Software Architecture**: System design, patterns, scalability
- 💻 **DevOps**: Deployment, infrastructure, CI/CD, Docker, K8s
- 🔬 **AI/ML Engineering**: Models, frameworks, LangChain, LangGraph
- 📝 **Technical Writing**: Documentation, explanations, tutorials
- 🎓 **Education**: Teaching, learning paths, pedagogy
- 💰 **Finance**: Markets, analysis, accounting, economics
- ⚕️ **Healthcare**: Medical knowledge, procedures, research
- 🚗 **Automotive**: Vehicles, maintenance, engineering
- *[Any domain the user specifies]*

---

## ✨ **Features**

### **Current Implementation (V1.0)**
- ✅ Fixed Python-specific question answering
- ✅ Basic question enhancement pipeline
- ✅ Basic LangChain integration

### **Planned Features (V2.0)**
- 🎭 **User-Defined Specialization**: Any expert domain specified by user
- ✨ **Dynamic Role Adoption**: Assistant becomes the specified expert
- 🧠 **LangGraph Integration**: Workflow orchestration for enhancement
- 🔍 **Question Enhancement**: Improved question formulation
- ❌ **Knowledge Boundaries**: "I don't know" for out-of-scope questions
- 💬 **Session Memory**: Remember the chosen specialization
- 📈 **Response Quality**: Expert-level answers with examples

### **Future Enhancements (V3.0+)**
- 🌐 **Web Interface**: User-friendly GUI
- 🔌 **API Endpoints**: REST API for integration
- 📚 **Knowledge Base**: Domain-specific information storage
- 🔄 **Feedback Loop**: Learning from user satisfaction
- 🎨 **Custom Roles**: User-defined expert personas

---

## 🎯 **Usage Examples**

### **Example 1: Python Specialist**
```
User: "You are a Python expert"
System: "I'm now a Python specialist. How can I help you with Python programming?"

User: "Explain with examples what is a dictionary"
→ Enhanced Question: "Provide a comprehensive explanation of Python dictionaries with practical examples, including creation, access, modification, and common use cases"
→ Response: [Detailed Python dictionary explanation with code examples]

User: "How do I deploy a Django app?"
→ Response: "I don't know this question. While I'm a Python expert, Django deployment involves DevOps concepts that are outside my core Python programming expertise."
```

### **Example 2: Data Science Specialist**
```
User: "You are a Data Science expert"
System: "I'm now a Data Science specialist. How can I help you with data analysis and machine learning?"

User: "How do I handle missing data?"
→ Enhanced Question: "What are the best practices for handling missing data in datasets, including detection methods, imputation strategies, and their impact on model performance?"
→ Response: [Detailed data science answer with pandas/sklearn examples]

User: "What's the best Python IDE?"
→ Response: "I don't know this question. As a Data Science specialist, I focus on data analysis and ML techniques rather than general development tools."
```

### **Example 3: Finance Specialist**
```
User: "You are a Finance expert"
System: "I'm now a Finance specialist. How can I help you with financial analysis and markets?"

User: "Explain compound interest"
→ Enhanced Question: "Provide a comprehensive explanation of compound interest, including the formula, practical examples, and its importance in investments and loans"
→ Response: [Detailed finance explanation with calculations and real-world examples]

User: "How do I code in Python?"
→ Response: "I don't know this question. As a Finance specialist, I focus on financial concepts rather than programming languages."
```

---

## 📁 **Project Structure**

```
assistent_questions_project/
├── README.md              # This file
├── .env                   # Environment variables
├── __init__.py           # Package initialization
├── requirements.txt       # Dependencies (to be created)
├── pyproject.toml        # Project configuration (to be created)
│
├── src/                  # Source code
│   ├── __init__.py
│   ├── agents/           # LangGraph agents
│   │   ├── __init__.py
│   │   ├── question_enhancer.py     # Enhances user questions
│   │   ├── specialist_agent.py      # Single flexible specialist
│   │   └── knowledge_boundary.py    # "I don't know" logic
│   │
│   ├── graph/           # LangGraph workflows
│   │   ├── __init__.py
│   │   ├── main_workflow.py         # Question → Enhancement → Response
│   │   └── graph_config.py          # LangGraph configuration
│   │
│   ├── core/           # Core utilities
│   │   ├── __init__.py
│   │   ├── llm_config.py            # LLM setup and configuration
│   │   ├── prompts.py               # Specialist role prompts
│   │   ├── session_manager.py       # Remember chosen specialization
│   │   └── validators.py            # Input validation
│   │
│   └── main.py         # Entry point
│
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_workflow.py
│   └── test_integration.py
│
├── data/              # Sample data and examples
│   ├── sample_questions.json
│   └── test_contexts.json
│
├── docs/              # Documentation
│   ├── architecture.md
│   ├── agent_roles.md
│   └── examples.md
│
└── v1_legacy/         # Previous Python-only version
    └── python_assistant.py
```

---

## 🚀 **Installation & Setup**

### **Prerequisites**
- Python 3.10+
- OpenAI API key (or other LLM provider)
- Git

### **Installation Steps**
```bash
# 1. Clone/Navigate to project
cd assistent_questions_project

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# 3. Install dependencies (when requirements.txt is created)
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env  # Copy environment template
# Edit .env with your API keys

# 5. Run the assistant
python src/main.py
```

---

## 🛣️ **Development Roadmap**

### **Phase 1: Foundation** (Weeks 1-2)
- [ ] Set up project structure
- [ ] Configure LangGraph and LangChain
- [ ] Create basic question enhancement agent
- [ ] Implement simple context analyzer
- [ ] Build role selection logic

### **Phase 2: Core Agents** (Weeks 3-4)
- [ ] Develop 3-5 specialist agents
- [ ] Create LangGraph workflow
- [ ] Implement agent coordination
- [ ] Add response quality validation

### **Phase 3: Enhancement** (Weeks 5-6)
- [ ] Add conversational memory
- [ ] Improve context understanding
- [ ] Create comprehensive test suite
- [ ] Add logging and monitoring

### **Phase 4: Polish** (Weeks 7-8)
- [ ] User interface improvements
- [ ] Performance optimization
- [ ] Documentation completion
- [ ] Deployment preparation

---

## 🧪 **Testing Strategy**

### **Test Categories**
- **Unit Tests**: Individual agent functionality
- **Integration Tests**: LangGraph workflow end-to-end
- **Performance Tests**: Response time and quality
- **Context Tests**: Role selection accuracy

### **Test Examples**
```python
def test_question_enhancement():
    """Test that questions are properly enhanced"""
    input_q = "What is a dictionary?"
    enhanced = enhance_question(input_q, "Python")
    assert "Python dictionaries" in enhanced
    assert "examples" in enhanced
    
def test_specialist_assignment():
    """Test that specialist role is properly set"""
    specialist = create_specialist("Python")
    assert specialist.domain == "Python"
    assert "Python expert" in specialist.system_prompt
    
def test_knowledge_boundary():
    """Test 'I don't know' responses for out-of-scope questions"""
    python_specialist = create_specialist("Python")
    response = python_specialist.answer("How to invest in stocks?")
    assert "I don't know" in response
    
def test_workflow_integration():
    """Test complete question-to-answer flow"""
    # Test: User sets specialization → asks question → gets expert answer
```

---

## 🤝 **Contributing**

This is a learning project! Contributions and suggestions are welcome:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **LangChain**: For the foundational LLM framework
- **LangGraph**: For workflow orchestration capabilities
- **OpenAI**: For powerful language models
- **Community**: For inspiration and best practices

---

**🚀 Ready to build an intelligent question-answering assistant? Let's get started!**