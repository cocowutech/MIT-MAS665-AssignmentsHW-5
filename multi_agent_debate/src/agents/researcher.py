"""Researcher agent for the multi-agent debate system."""

from typing import Dict, Any
from .base import BaseAgent

class Researcher(BaseAgent):
    """Researcher agent that gathers and presents information on a topic."""
    
    def __init__(self, temperature: float = None):
        super().__init__(
            name="Researcher",
            role_description="Gathers and presents factual information on the debate topic",
            temperature=temperature
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Researcher agent."""
        return """
You are a Researcher in a structured debate. Your role is to:
1. Gather and present factual information relevant to the debate topic
2. Provide evidence, data, and well-researched points
3. Focus on accuracy and verifiability of information
4. Present multiple perspectives when appropriate
5. Cite sources or indicate the basis of your claims

Your response should be well-structured, evidence-based, and focused on providing
substantive information that other agents can use for their analysis. Avoid making
unsubstantiated claims and clearly distinguish between facts and interpretations.
"""
    
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process the debate topic and provide researched information."""
        # Add the input to history
        self.add_to_history("user", input_text)
        
        # Create a specific prompt for the researcher
        research_prompt = f"""
Debate Topic: {input_text}

Please provide a well-researched analysis of this topic, including:
1. Key facts and background information
2. Relevant evidence and data
3. Different perspectives or viewpoints
4. Important considerations or implications

Focus on providing accurate, verifiable information that will help inform the debate.
"""
        
        # Generate response
        response = self.invoke_llm(research_prompt, context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
