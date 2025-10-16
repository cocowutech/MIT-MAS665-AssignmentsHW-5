"""Synthesizer agent for the multi-agent debate system."""

from typing import Dict, Any
from .base import BaseAgent

class Synthesizer(BaseAgent):
    """Synthesizer agent that integrates different perspectives and finds common ground."""
    
    def __init__(self, temperature: float = None):
        super().__init__(
            name="Synthesizer",
            role_description="Integrates different perspectives and finds common ground",
            temperature=temperature
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Synthesizer agent."""
        return """
You are a Synthesizer in a structured debate. Your role is to:
1. Integrate different perspectives and arguments presented
2. Identify areas of agreement and common ground
3. Reconcile conflicting viewpoints when possible
4. Highlight key insights from different positions
5. Propose balanced solutions or compromises

Your synthesis should be comprehensive, balanced, and forward-looking. Focus on
finding the most valuable insights from each perspective and creating a coherent
understanding that incorporates the strongest elements of all arguments.
"""
    
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process the different arguments and provide a synthesis."""
        # Add the input to history
        self.add_to_history("user", input_text)
        
        # Get previous messages for context if available
        previous_arguments = ""
        if context and "previous_messages" in context:
            previous_arguments = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in context["previous_messages"]
            ])
        
        # Create a specific prompt for the synthesizer
        synthesis_prompt = f"""
Arguments to Synthesize:
{input_text}

Previous Debate Context:
{previous_arguments}

Please provide a synthesis of these arguments, focusing on:
1. Key points of agreement and disagreement
2. Common ground that can be identified
3. How different perspectives complement each other
4. Balanced insights that incorporate multiple viewpoints
5. Potential compromises or integrated solutions

Create a coherent understanding that respects the valuable elements of each position.
"""
        
        # Generate response
        response = self.invoke_llm(synthesis_prompt, context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
