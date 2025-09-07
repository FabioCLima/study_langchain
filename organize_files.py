#!/usr/bin/env python3
"""
Smart File Organizer for LangChain Study Project
Automatically categorizes and moves files based on content analysis
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Define categorization rules based on file names and patterns
CATEGORIZATION_RULES = {
    # Learning - Fundamentals
    'learning/01_fundamentals/chains': [
        r'chain_template',
        r'simple_chain',
        r'chain_.*study',
        r'chain_2_steps',
        r'langchain_ex[1-3]',  # Basic examples
        r'exercise_chain[0-2]',  # Basic exercises
    ],
    
    'learning/01_fundamentals/prompts': [
        r'few_shot',
        r'prompt',
        r'template',
    ],
    
    'learning/01_fundamentals/models': [
        r'openai_client',
        r'test_setup',
    ],
    
    # Learning - Advanced
    'learning/02_advanced/output_parsers': [
        r'output_parser',
        r'pydantic',
        r'parser',
        r'advanced_output_parsers',
        r'improved_pydantic_example',
    ],
    
    'learning/02_advanced/memory': [
        r'memory',
        r'chatbot_core',
        r'chatbot_class',
    ],
    
    'learning/02_advanced/agents': [
        r'ai_agent',
        r'agent',
    ],
    
    # Learning - Integration  
    'learning/03_integration/files': [
        r'rag_',
        r'document',
    ],
    
    # Learning - Patterns
    'learning/04_patterns/factories': [
        r'factory',
        r'client',
    ],
    
    'learning/04_patterns/builders': [
        r'multi_step_workflow',
        r'chains_composition',
    ],
    
    # Projects
    'projects/chatbot/src': [
        r'chatbot',
        r'simple_chatbot',
    ],
    
    'projects/travel_agent/src': [
        r'roteiro',
        r'viagem',
        r'destino',
        r'chain_destino',
    ],
    
    'projects/sentiment_analyzer/src': [
        r'sentiment',
        r'analisador_de_sentimento',
    ],
    
    # Experiments (anything with versions or comparisons)
    'experiments': [
        r'.*_v[2-9]',  # versioned files
        r'.*_final',
        r'.*_corrigido',
        r'.*_melhorado',
        r'comparacao_',
        r'exemplo_',
        r'runnable_',
    ],
    
    # Tools
    'tools': [
        r'main\.py$',
        r'setup',
        r'test_',
    ]
}

def analyze_file_content(file_path: Path) -> List[str]:
    """Analyze file content to determine its category"""
    keywords = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for key patterns in content
            if 'PydanticOutputParser' in content or 'BaseModel' in content:
                keywords.append('output_parser')
            if 'ChatOpenAI' in content and 'memory' in content.lower():
                keywords.append('chatbot')
            if 'RunnableParallel' in content:
                keywords.append('advanced_chains')
            if 'agent' in content.lower():
                keywords.append('agent')
            if 'rag' in content.lower() or 'retrieval' in content.lower():
                keywords.append('rag')
            if 'sentiment' in content.lower():
                keywords.append('sentiment')
            if 'travel' in content.lower() or 'viagem' in content.lower():
                keywords.append('travel')
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return keywords

def categorize_file(file_path: Path) -> str:
    """Categorize a file based on name and content"""
    filename = file_path.name.lower()
    
    # First try name-based categorization
    for category, patterns in CATEGORIZATION_RULES.items():
        for pattern in patterns:
            if re.search(pattern, filename):
                return category
    
    # Then try content-based categorization
    content_keywords = analyze_file_content(file_path)
    
    if 'output_parser' in content_keywords:
        return 'learning/02_advanced/output_parsers'
    elif 'chatbot' in content_keywords:
        return 'projects/chatbot/src'
    elif 'travel' in content_keywords:
        return 'projects/travel_agent/src'
    elif 'sentiment' in content_keywords:
        return 'projects/sentiment_analyzer/src'
    elif 'rag' in content_keywords:
        return 'projects/rag_system/src'
    
    # Default fallback
    if filename.endswith('.py'):
        return 'learning/01_fundamentals/exercises'
    
    return 'archive'

def get_files_to_organize() -> List[Path]:
    """Get list of Python files to organize"""
    base_path = Path('/home/fabiolima/Workdir/langchain/study_langchain')
    
    files_to_organize = []
    
    # Get files from src/script_4_studies (the messy folder)
    script_studies = base_path / 'src' / 'script_4_studies'
    if script_studies.exists():
        files_to_organize.extend(list(script_studies.glob('*.py')))
    
    # Get files from src/examples
    examples_dir = base_path / 'src' / 'examples'
    if examples_dir.exists():
        files_to_organize.extend(list(examples_dir.glob('*.py')))
    
    # Get files from src/chain_roteiro_viagem  
    roteiro_dir = base_path / 'src' / 'chain_roteiro_viagem'
    if roteiro_dir.exists():
        files_to_organize.extend(list(roteiro_dir.glob('*.py')))
    
    return files_to_organize

def create_experiment_folder(file_path: Path, base_path: Path) -> str:
    """Create dated experiment folder for versioned files"""
    from datetime import datetime
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = file_path.stem
    
    # Clean filename for folder name
    clean_name = re.sub(r'_v\d+|_final|_corrigido|_melhorado', '', filename)
    
    experiment_name = f"{today}_{clean_name}"
    experiment_path = base_path / 'experiments' / experiment_name
    
    return str(experiment_path.relative_to(base_path))

def organize_files():
    """Main organization function"""
    base_path = Path('/home/fabiolima/Workdir/langchain/study_langchain')
    
    files_to_organize = get_files_to_organize()
    
    print(f"Found {len(files_to_organize)} files to organize...")
    
    organization_plan = {}
    
    for file_path in files_to_organize:
        category = categorize_file(file_path)
        
        # Special handling for experiments
        if category == 'experiments':
            category = create_experiment_folder(file_path, base_path)
        
        if category not in organization_plan:
            organization_plan[category] = []
            
        organization_plan[category].append(file_path)
    
    print("\n📋 ORGANIZATION PLAN:")
    print("=" * 50)
    
    for category, files in organization_plan.items():
        print(f"\n📁 {category}:")
        for file_path in files:
            print(f"  - {file_path.name}")
    
    return organization_plan

def execute_organization(organization_plan: Dict[str, List[Path]], dry_run: bool = True):
    """Execute the file organization"""
    base_path = Path('/home/fabiolima/Workdir/langchain/study_langchain')
    
    for category, files in organization_plan.items():
        target_dir = base_path / category
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for file_path in files:
            target_file = target_dir / file_path.name
            
            if dry_run:
                print(f"WOULD MOVE: {file_path} -> {target_file}")
            else:
                print(f"MOVING: {file_path} -> {target_file}")
                shutil.move(str(file_path), str(target_file))

if __name__ == "__main__":
    print("🎯 LangChain Project Organizer")
    print("=" * 40)
    
    plan = organize_files()
    
    print(f"\n❓ Execute organization? (y/n): ", end="")
    response = input()
    
    if response.lower() == 'y':
        execute_organization(plan, dry_run=False)
        print("\n✅ Organization complete!")
    else:
        print("ℹ️  Organization cancelled. Run with dry_run=False to execute.")
