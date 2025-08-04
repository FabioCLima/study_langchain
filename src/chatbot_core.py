"""
This script is an example of how to use OpenAI's LLM model to create a chatbot.
"""

from collections.abc import Sequence

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,  # type: ignore
)
from langchain_openai import ChatOpenAI  # type: ignore

from openai_client import ApiKeyLoader, ChatModelFactory


def create_analytical_model() -> ChatOpenAI | None:
    """
    Creates and returns an instance of OpenAI's analytical chat model.

    This method loads the API key from the .env file, instantiates the chat model factory,
    and returns the LLM model configured for analysis.

    Returns:
        ChatOpenAI | None: Instance of the OpenAI chat model if loaded successfully,
        or None if there was an error loading the API key.

    Raises:
        ValueError: If the API key cannot be found or loaded.
    """
    try:
        loader = ApiKeyLoader()
        openai_api_key = loader.get_openai_key()
        print(f"OpenAI API key loaded successfully: {openai_api_key[-4:]}")
        chat_factory = ChatModelFactory(openai_api_key)
        analytical_llm = chat_factory.create_analytical_model()
        print("OpenAI chat model created successfully!")
        return analytical_llm
    except ValueError as e:
        print(f"Error loading API key: {e}")
        return None


analytical_llm = create_analytical_model()
if not analytical_llm:
    print("Error: model was not loaded.")


class MemoryManager:
    """Abstracts the chatbot's memory management."""

    def __init__(self) -> None:
        self._memory: list[BaseMessage] = []

    def add_message(self, message: BaseMessage) -> None:
        """Adds a user or AI message to the conversation history."""
        self._memory.append(message)

    def get_history(self, limit: int = 20) -> list[BaseMessage]:
        """Returns the last `limit` messages from the conversation history."""
        return self._memory[-limit:]


class PromptFactory:
    """Creates and formats prompts with personality and examples."""

    def __init__(
        self,
        system_prompt: str,
        few_shot_examples: Sequence[BaseMessage],
    ):
        self.system_prompt = SystemMessage(content=system_prompt)
        self.few_shot_examples = list(few_shot_examples)

    def build_full_prompt(
        self, current_memory: list[BaseMessage], user_message: str
    ) -> list[BaseMessage]:
        """Builds the list of messages to send to the LLM."""
        return [
            self.system_prompt,
            *self.few_shot_examples,
            *current_memory,
            HumanMessage(content=user_message),
        ]


class Chatbot:
    """Orchestrates the interaction between the user, memory, prompt factory, and LLM."""

    def __init__(
        self,
        llm: ChatOpenAI,
        memory: MemoryManager,
        prompt_factory: PromptFactory,
    ):
        self.llm = llm
        self.memory = memory
        self.prompt_factory = prompt_factory

    def chat(self, user_message: str) -> str:
        """Processes the user's message and returns the AI's response."""
        current_history = self.memory.get_history()
        full_prompt = self.prompt_factory.build_full_prompt(
            current_history, user_message
        )

        ai_response = self.llm.invoke(full_prompt)

        self.memory.add_message(HumanMessage(content=user_message))
        self.memory.add_message(ai_response)

        # Garantir que sempre retorna str
        return str(getattr(ai_response, "content", ai_response))


def main():
    """
    Main entry point: configures and runs the chatbot.
    """
    print("Starting ChatBot setup...")

    # 1. Load the LLM model
    llm = create_analytical_model()
    if not llm:
        print("Shutting down application due to model loading failure.")
        return

    # 2. Configure other ChatBot components
    pirate_personality = (
        "You are a robotic pirate named 'Captain Byte'. "
        "You are sarcastic but always helpful. "
        "Respond in Brazilian Portuguese and use pirate slang."
    )
    pirate_examples = [
        HumanMessage(content="Qual o seu nome?"),
        AIMessage(
            content="Arr! Meu nome é Capitão Byte, o terror dos sete mares digitais! O que você deseja, marujo?"
        ),
    ]

    memory = MemoryManager()
    prompt_factory = PromptFactory(
        system_prompt=pirate_personality, few_shot_examples=pirate_examples
    )

    # 3. Assemble the ChatBot by injecting dependencies
    chatbot = Chatbot(llm=llm, memory=memory, prompt_factory=prompt_factory)

    print("\n--- Chat with Captain Byte started! Type 'sair' to end. ---")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print(
                "Capitão Byte: Adeus, marujo! Que seus ventos sejam sempre favoráveis!"
            )
            break
        try:
            response = chatbot.chat(user_input)
            print(f"Capitão Byte: {response}")
        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")


if __name__ == "__main__":
    main()
