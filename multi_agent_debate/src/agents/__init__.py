"""Agent implementations for the multi-agent debate system."""

from .base import BaseAgent
from .researcher import Researcher
from .critic import Critic
from .synthesizer import Synthesizer
from .judge import Judge
from .devils_advocate import DevilsAdvocate

__all__ = [
    "BaseAgent",
    "Researcher", 
    "Critic",
    "Synthesizer",
    "Judge",
    "DevilsAdvocate"
]
