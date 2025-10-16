"""Base agent class for the multi-agent debate system."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from src.utils.config import config

class BaseAgent(ABC):
    """Abstract base class for all debate agents."""
    
    def __init__(self, name: str, role_description: str, temperature: float = None):
        self.name = name
        self.role_description = role_description
        self.llm = ChatOpenAI(**config.get_llm_config(temperature))
        self.message_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    @abstractmethod
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process input and generate response."""
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add a message to the agent's history."""
        self.message_history.append({"role": role, "content": content})
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the agent's message history."""
        return self.message_history.copy()
    
    def clear_history(self):
        """Clear the agent's message history."""
        self.message_history = []
    
    def _create_messages(self, input_text: str, context: Dict[str, Any] = None) -> List:
        """Create messages for the LLM."""
        messages = [HumanMessage(content=self.get_system_prompt())]
        
        # Add context if provided
        if context and "previous_messages" in context:
            for msg in context["previous_messages"]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current input
        messages.append(HumanMessage(content=input_text))
        
        return messages
    
    def invoke_llm(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Invoke the LLM with the given input."""
        messages = self._create_messages(input_text, context)
        response = self.llm.invoke(messages)
        return response.content
