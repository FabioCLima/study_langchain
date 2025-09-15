"""
Main Entry Point for the Assistant
==================================

Provides a polished CLI to interact with the compiled workflow,
showing real-time progress and a clean final answer.
"""
from .graph.workflow import app
from .core.state import AgentState

def main():
    print("🤖 Bem-vindo ao Assistente de Perguntas Inteligentes!")
    print("Para cada pergunta, forneça também o contexto/domínio.")
    print("Para sair, digite 'sair' na pergunta.")

    while True:
        original_question = input("\nSua pergunta: ")
        if original_question.lower() in ["sair", "exit"]:
            print("👋 Até logo!")
            break
        
        specialization = input(f"Contexto para '{original_question}': ")

        initial_state: AgentState = {
            "original_question": original_question,
            "specialization": specialization,
            "enhanced_question": "",
            "answer": ""
        }

        print("\n---  Procesando... ---")
        final_answer = "Ocorreu um erro ao processar sua pergunta." # Resposta padrão
        
        # Usamos o stream para dar feedback em tempo real
        for event in app.stream(initial_state):
            node_name = list(event.keys())[0]

            if node_name == "enhancer":
                print("🧠  Aprimorando sua pergunta...")
            
            if node_name == "specialist":
                print(f"🧑‍🏫  Consultando especialista em {specialization}...")
                final_answer = event[node_name]['answer']
            
            if node_name == "out_of_scope":
                print("🚫  A pergunta parece estar fora do escopo definido...")
                final_answer = event[node_name]['answer']

        print("\n--- Resposta Final ---")
        print(final_answer)

if __name__ == "__main__":
    main()