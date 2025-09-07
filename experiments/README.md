# 🧪 LangChain Experiments

This folder contains **dated experiments and proof-of-concepts** that document your learning journey. Each experiment represents a specific exploration or comparison.

## 📅 **EXPERIMENT STRUCTURE**

### **Naming Convention:**
```
YYYY-MM-DD_experiment_name/
├── experiment_file.py
├── results.md            # (optional)
└── notes.md             # (optional)
```

### **Current Experiments:**

#### **🔗 2025-09-07_chain_pais_capital_curiosidade/**
**What it explores:** Evolution of a country-capital chain through multiple iterations  
**Files:** 4 versions showing progressive improvements  
**Key Learning:** Chain refinement and debugging process

```
├── chain_pais_capital_curiosidade_v3.py      # Version 3
├── chain_pais_capital_curiosidade_v5.py      # Version 5  
├── chain_pais_capital_curiosidade_corrigido.py  # Bug fixes
└── chain_pais_capital_curiosidade_final.py      # Final version
```

#### **⚡ 2025-09-07_comparacao_paralelo_vs_encadeado/**
**What it explores:** Performance comparison between parallel and sequential chain execution  
**Files:** 1 comparison script  
**Key Learning:** When to use RunnableParallel vs sequential chains

#### **🔧 2025-09-07_runnable_passthrough_assign_demo/**
**What it explores:** Advanced usage patterns for RunnablePassthrough.assign  
**Files:** 1 demonstration script  
**Key Learning:** Data flow control in LCEL chains

#### **🏗️ 2025-09-07_exemplo_runnable_parallel/**
**What it explores:** RunnableParallel implementation patterns  
**Files:** 1 example implementation  
**Key Learning:** Parallel execution strategies

#### **📝 2025-09-07_projetinho_alura_chains/**
**What it explores:** Small project iterations from Alura course  
**Files:** 2 versions (v2, v3)  
**Key Learning:** Project evolution and best practices

#### **🎯 2025-09-07_exemplo_simples_paralelo/**
**What it explores:** Simple parallel execution examples  
**Files:** 1 basic example  
**Key Learning:** Fundamentals of parallel processing

## 🎯 **HOW TO USE EXPERIMENTS**

### **1. Learning from Failures**
```bash
cd experiments/2025-09-07_chain_pais_capital_curiosidade
# Compare different versions to see what was fixed
diff chain_pais_capital_curiosidade_v3.py chain_pais_capital_curiosidade_final.py
```

### **2. Understanding Evolution**
Each experiment shows:
- ✅ **What worked** - Successful patterns
- ❌ **What failed** - Common mistakes  
- 🔄 **What changed** - Iterative improvements
- 💡 **What learned** - Key insights

### **3. Pattern Recognition**
Look for recurring themes:
- **Output parsing evolution** - Multiple attempts at structured output
- **Chain composition patterns** - Different approaches to combining chains
- **Error handling strategies** - How bugs were identified and fixed

## 📚 **EXPERIMENT CATEGORIES**

### **🔗 Chain Evolution**
- `chain_pais_capital_curiosidade/` - Multi-version chain development
- Shows iterative improvement process

### **⚡ Performance Comparisons**
- `comparacao_paralelo_vs_encadeado/` - Parallel vs sequential execution
- `exemplo_runnable_parallel/` - Parallel execution patterns
- `exemplo_simples_paralelo/` - Basic parallel concepts

### **🎯 Feature Exploration**
- `runnable_passthrough_assign_demo/` - Advanced LCEL patterns
- Shows specific feature deep-dives

### **📝 Project Iterations**
- `projetinho_alura_chains/` - Course project evolution
- Shows real learning progression

## 💡 **EXPERIMENT INSIGHTS**

### **Key Learning Patterns:**

#### **1. Chain Debugging Process**
```
v1 → Basic implementation
v2 → Fix syntax errors  
v3 → Improve structure
v4 → Add error handling
v5 → Optimize performance
final → Production ready
```

#### **2. Common Evolution Path**
```
Simple string output
       ↓
Structured output attempt
       ↓
Pydantic model implementation
       ↓
Error handling added
       ↓
Production optimization
```

#### **3. Parallel vs Sequential Decision Tree**
```
Independent operations? → RunnableParallel
Sequential dependencies? → Chain composition  
Mixed requirements? → Hybrid approach
```

## 🔍 **EXPERIMENT ANALYSIS**

### **Most Valuable Experiments:**
1. **`chain_pais_capital_curiosidade/`** - Shows complete debugging cycle
2. **`comparacao_paralelo_vs_encadeado/`** - Performance insights
3. **`projetinho_alura_chains/`** - Real project evolution

### **Quick Wins:**
- **`exemplo_simples_paralelo/`** - Easy parallel concepts
- **`runnable_passthrough_assign_demo/`** - Useful LCEL patterns

## 📈 **CREATING NEW EXPERIMENTS**

### **Template for New Experiment:**
```bash
# Create new experiment
mkdir experiments/$(date +%Y-%m-%d)_your_experiment_name

# Add your experimental code
cp your_prototype.py experiments/$(date +%Y-%m-%d)_your_experiment_name/

# Document results (optional)
echo "# Experiment Results" > experiments/$(date +%Y-%m-%d)_your_experiment_name/results.md
echo "# Learning Notes" > experiments/$(date +%Y-%m-%d)_your_experiment_name/notes.md
```

### **Best Practices:**
1. **Date your experiments** - Track chronological learning
2. **Keep original failures** - Learn from mistakes
3. **Document insights** - Add README or notes
4. **Compare versions** - Show evolution clearly

---

**💡 Remember:** Experiments are meant to fail! They show your learning journey and help others avoid the same mistakes.
