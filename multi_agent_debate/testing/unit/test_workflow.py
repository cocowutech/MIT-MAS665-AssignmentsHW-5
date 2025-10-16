"""Unit tests for workflow components."""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.workflow import create_debate_graph, initialize_debate_state, DebateState

class TestDebateWorkflow(unittest.TestCase):
    """Test the debate workflow functionality."""
    
    def test_initialize_debate_state(self):
        """Test debate state initialization."""
        state = initialize_debate_state(
            topic="Test topic",
            rounds=2,
            agent_types=["researcher", "critic", "judge"]
        )
        
        self.assertEqual(state["topic"], "Test topic")
        self.assertEqual(state["current_round"], 1)
        self.assertEqual(state["total_rounds"], 2)
        self.assertEqual(state["current_agent"], "researcher")
        self.assertEqual(state["agent_sequence"], ["researcher", "critic", "judge"])
        self.assertEqual(len(state["messages"]), 0)
        self.assertFalse(state["convergence"])
    
    def test_initialize_debate_state_with_devils_advocate(self):
        """Test debate state initialization with devil's advocate."""
        state = initialize_debate_state(
            topic="Test topic",
            rounds=2,
            agent_types=["researcher", "critic", "synthesizer", "judge"],
            include_devils_advocate=True
        )
        
        # Devil's advocate should be inserted before synthesizer
        expected_sequence = ["researcher", "critic", "devils_advocate", "synthesizer", "judge"]
        self.assertEqual(state["agent_sequence"], expected_sequence)
    
    @patch('src.agents.base.ChatOpenAI')
    def test_create_debate_graph(self, mock_llm):
        """Test debate graph creation."""
        graph = create_debate_graph(
            agent_types=["researcher", "critic", "judge"],
            rounds=2,
            temperature=0.7
        )
        
        # Check that graph was created
        self.assertIsNotNone(graph)
    
    @patch('src.agents.base.ChatOpenAI')
    def test_create_debate_graph_with_devils_advocate(self, mock_llm):
        """Test debate graph creation with devil's advocate."""
        graph = create_debate_graph(
            agent_types=["researcher", "critic", "synthesizer", "judge"],
            rounds=2,
            include_devils_advocate=True
        )
        
        # Check that graph was created
        self.assertIsNotNone(graph)

if __name__ == "__main__":
    unittest.main()
