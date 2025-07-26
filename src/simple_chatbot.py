from typing import List

from langchain_core.messages import AIMessage, HumanMessage  # type: ignore
from langchain_core.prompts import ChatPromptTemplate  # type: ignore
from langchain_core.prompts import \
    FewShotChatMessagePromptTemplate  # type: ignore
from langchain_openai import ChatOpenAI  # type: ignore

from openai_client import ApiKeyLoader, ChatModelFactory


class ChatBot:
    def __init__(
        self,
        name: str,
        instructions: str,
        examples: List[dict[str, str]],  # type: ignore
        model: str = "gpt-4o-mini",
        temperature: float = 0.0
    ):
        self.name = name
        loader = ApiKeyLoader()  # type: ignore
        openai_api_key = loader.get_openai_key()  # type: ignore
        chat_factory = ChatModelFactory(openai_api_key)  # type: ignore
        self.llm = chat_factory.create_analytical_model(model_name=model, temperature=temperature)  # type: ignore
        
        example_prompt = ChatPromptTemplate.from_messages(  # type: ignore
            [
                ("system", instructions),
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )
        prompt_template = FewShotChatMessagePromptTemplate(  # type: ignore
            example_prompt=example_prompt,
            examples=examples,
        )
        self.messages = prompt_template.invoke({}).to_messages()  # type: ignore

    def invoke(self, user_message: str) -> AIMessage:  # type: ignore
        self.messages.append(HumanMessage(user_message))  # type: ignore
        ai_message = self.llm.invoke(self.messages)  # type: ignore
        self.messages.append(ai_message)  # type: ignore
        return ai_message  # type: ignore