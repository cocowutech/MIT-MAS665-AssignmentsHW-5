"""Critic agent for the multi-agent debate system."""

from typing import Dict, Any
from .base import BaseAgent

class Critic(BaseAgent):
    """Critic agent that evaluates arguments and identifies weaknesses."""
    
    def __init__(self, temperature: float = None):
        super().__init__(
            name="Critic",
            role_description="Evaluates arguments and identifies logical fallacies or weaknesses",
            temperature=temperature
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Critic agent."""
        return """
You are a Critic in a structured debate. Your role is to:
1. Evaluate the strength and validity of arguments presented
2. Identify logical fallacies, unsupported claims, or weak evidence
3. Point out potential biases or assumptions in arguments
4. Highlight missing information or counterarguments
5. Assess the feasibility and practicality of proposals

Your critique should be constructive, specific, and evidence-based. Focus on the
quality of reasoning and evidence rather than personal opinions. Be thorough but
fair in your analysis, acknowledging strengths while identifying weaknesses.
"""
    
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process the arguments and provide critical evaluation."""
        # Add the input to history
        self.add_to_history("user", input_text)
        
        # Get previous messages for context if available
        previous_arguments = ""
        if context and "previous_messages" in context:
            previous_arguments = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in context["previous_messages"][-3:]  # Last 3 messages for context
            ])
        
        # Create a specific prompt for the critic
        critic_prompt = f"""
Arguments to Evaluate:
{input_text}

Previous Context:
{previous_arguments}

Please provide a critical evaluation of these arguments, focusing on:
1. Logical consistency and validity
2. Quality and sufficiency of evidence
3. Potential biases or unstated assumptions
4. Strengths and weaknesses of the reasoning
5. Missing counterarguments or considerations

Be specific in your critique and provide constructive feedback.
"""
        
        # Generate response
        response = self.invoke_llm(critic_prompt, context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
