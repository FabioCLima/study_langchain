# 🚀 LangChain Projects

This folder contains **complete, production-ready projects** that demonstrate real-world applications of LangChain concepts.

## 📁 **PROJECT OVERVIEW**

### 🤖 **chatbot/** - Conversational AI
**What it does:** Production-ready chatbot with memory and personality  
**Key Technologies:** LangChain Memory, Conversation Management, LCEL  
**Entry Point:** `src/simple_chatbot.py`  
**Difficulty:** ⭐⭐⭐

**Features:**
- Conversation memory management
- Personality customization
- Error handling and recovery
- Production-ready architecture

**Files:**
```
chatbot/
├── src/
│   └── simple_chatbot.py     # Main chatbot implementation
├── data/                     # Sample conversations
├── docs/                     # Documentation
└── tests/                    # Unit tests
```

### 🌍 **travel_agent/** - AI Travel Planner
**What it does:** Intelligent travel planning with recommendations  
**Key Technologies:** Chain Composition, Output Parsers, Multi-step Workflows  
**Entry Point:** `src/chain_destino.py`  
**Difficulty:** ⭐⭐⭐⭐

**Features:**
- Destination recommendations based on interests
- Restaurant suggestions with structured output
- Cultural activity planning
- Complex chain orchestration

**Files:**
```
travel_agent/
├── src/
│   └── chain_destino.py      # Main travel planning logic
├── data/                     # Travel data and samples
├── docs/                     # Project documentation
└── tests/                    # Integration tests
```

### 😊 **sentiment_analyzer/** - Text Sentiment Analysis
**What it does:** Advanced sentiment analysis with structured output  
**Key Technologies:** Pydantic Output Parsers, Text Processing  
**Entry Point:** `src/analisador_de_sentimento.py`  
**Difficulty:** ⭐⭐

**Features:**
- Multi-dimensional sentiment analysis
- Confidence scoring
- Structured JSON output
- Portuguese language support

**Files:**
```
sentiment_analyzer/
├── src/
│   └── analisador_de_sentimento.py  # Sentiment analysis engine
├── data/                            # Sample texts
├── docs/                            # Usage documentation
└── tests/                           # Test cases
```

### 📚 **rag_system/** - Document Q&A System
**What it does:** Question-answering system over documents  
**Key Technologies:** RAG, Vector Embeddings, Document Processing  
**Entry Point:** *Coming from learning/03_integration/files/*  
**Difficulty:** ⭐⭐⭐⭐⭐

**Features:**
- Document ingestion and processing
- Vector similarity search
- Context-aware question answering
- Multiple document format support

**Files:**
```
rag_system/
├── src/                     # RAG implementation
├── data/                    # Sample documents
├── docs/                    # System documentation
└── tests/                   # RAG tests
```

## 🎯 **HOW TO USE PROJECTS**

### 1. **Choose Based on Your Level**
- **Beginner**: Start with `sentiment_analyzer/`
- **Intermediate**: Try `chatbot/` 
- **Advanced**: Build `travel_agent/`
- **Expert**: Implement `rag_system/`

### 2. **Project Structure**
Each project follows the same structure:
```
project_name/
├── README.md            # Project-specific documentation
├── requirements.txt     # Additional dependencies
├── src/                 # Source code
├── data/               # Sample data and inputs
├── docs/               # Detailed documentation
└── tests/              # Test suite
```

### 3. **Running Projects**
```bash
# Navigate to project
cd projects/chatbot

# Check requirements
cat requirements.txt

# Run the main file
python src/simple_chatbot.py
```

## 🔗 **PROJECT RELATIONSHIPS**

### **Learning Path Integration:**
```
learning/01_fundamentals → projects/sentiment_analyzer
learning/02_advanced     → projects/chatbot  
learning/03_integration  → projects/rag_system
learning/04_patterns     → projects/travel_agent
```

### **Complexity Progression:**
```
sentiment_analyzer (⭐⭐) 
       ↓
   chatbot (⭐⭐⭐)
       ↓  
  travel_agent (⭐⭐⭐⭐)
       ↓
   rag_system (⭐⭐⭐⭐⭐)
```

## 📚 **PROJECT LEARNING OBJECTIVES**

### **chatbot/**
- Memory management patterns
- Conversation flow design
- Error handling strategies
- Production deployment considerations

### **travel_agent/**
- Multi-step workflow orchestration
- Complex chain composition
- Structured output management
- Real-world data processing

### **sentiment_analyzer/**
- Text processing fundamentals
- Output parser patterns
- Validation and error handling
- Structured data export

### **rag_system/**
- Vector database integration
- Document processing pipelines
- Retrieval-augmented generation
- Scalable architecture design

## 🚀 **QUICK START**

### **For Beginners:**
```bash
cd projects/sentiment_analyzer/src
python analisador_de_sentimento.py
```

### **For Intermediate:**
```bash
cd projects/chatbot/src  
python simple_chatbot.py
```

### **For Advanced:**
```bash
cd projects/travel_agent/src
python chain_destino.py
```

## 💡 **PROJECT EXTENSION IDEAS**

### **chatbot/**
- Add web interface
- Implement multiple personalities
- Add voice input/output
- Deploy to messaging platforms

### **travel_agent/**
- Add budget optimization
- Include weather data
- Build web dashboard
- Add booking integrations

### **sentiment_analyzer/**
- Add emotion detection
- Support multiple languages
- Build real-time API
- Add visualization dashboard

### **rag_system/**
- Add multi-modal support
- Implement semantic search
- Build web interface
- Add document versioning

---

**Ready to build?** Choose a project and dive in!
