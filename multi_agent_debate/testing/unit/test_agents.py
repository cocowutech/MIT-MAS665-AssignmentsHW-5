"""Unit tests for agent classes."""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.agents import Researcher, Critic, Synthesizer, Judge, DevilsAdvocate

class TestBaseAgent(unittest.TestCase):
    """Test the base agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = Researcher()
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.name, "Researcher")
        self.assertEqual(self.agent.role_description, "Gathers and presents factual information on the debate topic")
        self.assertEqual(len(self.agent.message_history), 0)
    
    def test_message_history(self):
        """Test message history functionality."""
        # Add messages to history
        self.agent.add_to_history("user", "Test message")
        self.agent.add_to_history("assistant", "Test response")
        
        # Check history
        history = self.agent.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Test message")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["content"], "Test response")
        
        # Clear history
        self.agent.clear_history()
        self.assertEqual(len(self.agent.get_history()), 0)

class TestResearcher(unittest.TestCase):
    """Test the Researcher agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = Researcher()
    
    def test_system_prompt(self):
        """Test the researcher's system prompt."""
        prompt = self.agent.get_system_prompt()
        self.assertIn("Researcher", prompt)
        self.assertIn("factual information", prompt)
        self.assertIn("evidence", prompt)
    
    @patch('src.agents.base.ChatOpenAI')
    def test_process_input(self, mock_llm):
        """Test processing input."""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.content = "Research findings on the topic"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create agent with mocked LLM
        agent = Researcher()
        
        # Process input
        response = agent.process_input("Test topic")
        
        # Check response
        self.assertEqual(response, "Research findings on the topic")
        
        # Check history
        history = agent.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Test topic")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["content"], "Research findings on the topic")

class TestCritic(unittest.TestCase):
    """Test the Critic agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = Critic()
    
    def test_system_prompt(self):
        """Test the critic's system prompt."""
        prompt = self.agent.get_system_prompt()
        self.assertIn("Critic", prompt)
        self.assertIn("evaluate", prompt.lower())
        self.assertIn("weaknesses", prompt)

class TestSynthesizer(unittest.TestCase):
    """Test the Synthesizer agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = Synthesizer()
    
    def test_system_prompt(self):
        """Test the synthesizer's system prompt."""
        prompt = self.agent.get_system_prompt()
        self.assertIn("Synthesizer", prompt)
        self.assertIn("integrate", prompt.lower())
        self.assertIn("common ground", prompt)

class TestJudge(unittest.TestCase):
    """Test the Judge agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = Judge()
    
    def test_system_prompt(self):
        """Test the judge's system prompt."""
        prompt = self.agent.get_system_prompt()
        self.assertIn("Judge", prompt)
        self.assertIn("verdict", prompt)
        self.assertIn("evaluation", prompt)
    
    def test_extract_ratings(self):
        """Test extracting ratings from verdict text."""
        verdict = """
        Overall assessment: The debate was well-structured.
        
        Evidence: 4/5 - Good evidence provided
        Feasibility: 3/5 - Moderately feasible
        Risks: 2/5 - Some risks not addressed
        Clarity: 4/5 - Arguments were clear
        """
        
        ratings = self.agent.extract_ratings(verdict)
        
        self.assertEqual(ratings["evidence"], 4)
        self.assertEqual(ratings["feasibility"], 3)
        self.assertEqual(ratings["risks"], 2)
        self.assertEqual(ratings["clarity"], 4)

class TestDevilsAdvocate(unittest.TestCase):
    """Test the Devil's Advocate agent."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.agents.base.ChatOpenAI'):
            self.agent = DevilsAdvocate()
    
    def test_system_prompt(self):
        """Test the devil's advocate's system prompt."""
        prompt = self.agent.get_system_prompt()
        self.assertIn("Devil's Advocate", prompt)
        self.assertIn("challenge", prompt.lower())
        self.assertIn("counterarguments", prompt)

if __name__ == "__main__":
    unittest.main()
