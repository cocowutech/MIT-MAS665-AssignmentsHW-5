"""Judge agent for the multi-agent debate system."""

from typing import Dict, Any, List
from .base import BaseAgent

class Judge(BaseAgent):
    """Judge agent that evaluates the debate and provides a final verdict."""
    
    def __init__(self, temperature: float = None):
        super().__init__(
            name="Judge",
            role_description="Evaluates the debate and provides a final verdict",
            temperature=temperature
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Judge agent."""
        return """
You are a Judge in a structured debate. Your role is to:
1. Evaluate the overall quality and coherence of the debate
2. Assess the strength of arguments and evidence presented
3. Determine if consensus was reached or if issues remain unresolved
4. Provide a final verdict or assessment on the debate topic
5. Rate the debate on key dimensions (evidence, feasibility, risks, clarity)

Your evaluation should be impartial, thorough, and well-reasoned. Consider all
perspectives presented and provide a clear, justified conclusion. If consensus
was not reached, explain the key points of disagreement and what further
discussion might be needed.
"""
    
    def process_input(self, input_text: str, context: Dict[str, Any] = None) -> str:
        """Process the debate and provide a final verdict."""
        # Add the input to history
        self.add_to_history("user", input_text)
        
        # Get previous messages for context if available
        debate_history = ""
        if context and "previous_messages" in context:
            debate_history = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in context["previous_messages"]
            ])
        
        # Create a specific prompt for the judge
        judge_prompt = f"""
Final Debate Input:
{input_text}

Complete Debate History:
{debate_history}

Please provide a comprehensive evaluation of this debate, including:
1. Overall assessment of argument quality and evidence
2. Whether consensus was reached or key disagreements remain
3. Final verdict or position on the debate topic
4. Ratings on key dimensions (evidence, feasibility, risks, clarity) on a scale of 0-5
5. Key strengths and weaknesses of the debate process

Be thorough and provide clear justification for your evaluation.
"""
        
        # Generate response
        response = self.invoke_llm(judge_prompt, context)
        
        # Add response to history
        self.add_to_history("assistant", response)
        
        return response
    
    def extract_ratings(self, verdict: str) -> Dict[str, int]:
        """Extract numerical ratings from the verdict text."""
        ratings = {
            "evidence": 0,
            "feasibility": 0,
            "risks": 0,
            "clarity": 0
        }
        
        # Simple extraction logic - in a real implementation, this might be more sophisticated
        lines = verdict.split('\n')
        for line in lines:
            if "evidence" in line.lower():
                for i in range(6):  # 0-5
                    if f"{i}/5" in line or f"{i} out of 5" in line:
                        ratings["evidence"] = i
            elif "feasibility" in line.lower():
                for i in range(6):
                    if f"{i}/5" in line or f"{i} out of 5" in line:
                        ratings["feasibility"] = i
            elif "risks" in line.lower():
                for i in range(6):
                    if f"{i}/5" in line or f"{i} out of 5" in line:
                        ratings["risks"] = i
            elif "clarity" in line.lower():
                for i in range(6):
                    if f"{i}/5" in line or f"{i} out of 5" in line:
                        ratings["clarity"] = i
        
        return ratings
