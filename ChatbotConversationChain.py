"""
Este código define una clase llamada "ChatBotChain" que es una cadena 
que lleva a cabo una conversación y llama a un modelo de lenguaje (LLM). 
La clase extiende la clase "LLMChain" y tiene una memoria de almacenamiento
y una plantilla de conversación predeterminadas. La clase también tiene métodos 
para obtener el historial de conversación de la memoria.
"""
from typing import Dict, List

from pydantic import Extra, Field, root_validator

from langchain.prompts.prompt import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.memory.buffer import ConversationBufferMemory
from langchain.schema import BaseMemory, BasePromptTemplate
import config


class ChatBotChain(LLMChain):
    """Chain to have a conversation and load context from memory.

    Example:
        .. code-block:: python

            from langchain import ConversationChain, OpenAI

            conversation = ConversationChain(llm=OpenAI())
    """
    memory: BaseMemory = Field(default_factory=ConversationBufferMemory)
    #memory: BaseMemory = ConversationBufferMemory()
    """Default memory store."""
    prompt: BasePromptTemplate = PromptTemplate(input_variables=["history", "input"],
                                                template=config.SANDRA_TEMPLATE)
    """Default conversation prompt to use."""

    input_key: str = "input"  #: :meta private:
    output_key: str = "response"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Use this since so some prompt vars come from history."""
        return [self.input_key]

    @root_validator()
    def validate_prompt_input_variables(cls, values: Dict) -> Dict:
        """Validate that prompt input variables are consistent."""
        memory_keys = values["memory"].memory_variables
        input_key = values["input_key"]
        if input_key in memory_keys:
            raise ValueError(
                f"The input key {input_key} was also found in the memory keys "
                f"({memory_keys}) - please provide keys that don't overlap."
            )
        prompt_variables = values["prompt"].input_variables
        expected_keys = memory_keys + [input_key]
        if set(expected_keys) != set(prompt_variables):
            raise ValueError(
                "Got unexpected prompt input variables. The prompt expects "
                f"{prompt_variables}, but got {memory_keys} as inputs from "
                f"memory, and {input_key} as the normal input key."
            )
        return values

    def getHistory(self) -> BaseMemory:
        return self.memory