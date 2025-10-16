"""Devil's Advocate agent for the multi-agent debate system."""

from typing import Dict, Any
from .base import BaseAgent

class DevilsAdvocate(BaseAgent):
    """Devil's Advocate agent that challenges prevailing opinions and assumptions."""
    
    def __init__(self, temperature: float = None):
        super().__init__(
            name="Devil's Advocate",
            role_description="Challenges prevailing opinions and assumptions",
            temperature=temperature
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Devil's Advocate agent."""
        return """
You are a Devil's Advocate in a structured debate. Your role is to:
1. Challenge prevailing opinions and assumptions
2. Present counterarguments to popular positions
3. Highlight potential negative consequences or risks
4. Question the feasibility or desirability of proposals
5. Ensure all perspectives receive thorough consideration

Your arguments should be thoughtful and well-reasoned, not merely contrarian.
Focus on identifying legitimate concerns, alternative viewpoints, and potential
problems that might otherwise be overlooked. Your goal is to strengthen the
debate by ensuring all positions are thoroughly tested.
"""
    
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process the arguments and provide counterarguments."""
        # Add the input to history
        self.add_to_history("user", input_text)
        
        # Get previous messages for context if available
        previous_arguments = ""
        if context and "previous_messages" in context:
            previous_arguments = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in context["previous_messages"][-3:]  # Last 3 messages for context
            ])
        
        # Create a specific prompt for the devil's advocate
        advocate_prompt = f"""
Arguments to Challenge:
{input_text}

Previous Context:
{previous_arguments}

Please provide counterarguments and challenges to these positions, focusing on:
1. Potential flaws or weaknesses in the reasoning
2. Alternative perspectives that might be overlooked
3. Possible negative consequences or risks
4. Questioning of underlying assumptions
5. Feasibility concerns or practical limitations

Be thoughtful in your challenges and provide reasoned arguments for your positions.
"""
        
        # Generate response
        response = self.invoke_llm(advocate_prompt, context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
