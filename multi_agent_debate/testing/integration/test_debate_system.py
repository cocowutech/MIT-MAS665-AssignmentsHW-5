"""Integration tests for the debate system."""

import unittest
from unittest.mock import patch, Mock
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.debate_system import DebateSystem

class TestDebateSystemIntegration(unittest.TestCase):
    """Integration tests for the debate system."""
    
    @patch('src.agents.base.ChatOpenAI')
    def test_run_debate_2_agents(self, mock_llm):
        """Test running a debate with 2 agents."""
        # Mock the LLM responses
        mock_response = Mock()
        mock_response.content = "Mock response"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create debate system
        debate_system = DebateSystem()
        
        # Run debate with 2 agents
        result = debate_system.run_debate(
            topic="Test topic",
            rounds=1,
            agent_types=["researcher", "judge"],
            temperature=0.7
        )
        
        # Check result structure
        self.assertIn("experiment_id", result)
        self.assertIn("timestamp", result)
        self.assertEqual(result["topic"], "Test topic")
        self.assertEqual(result["configuration"]["rounds"], 1)
        self.assertEqual(result["configuration"]["agents"], ["researcher", "judge"])
        self.assertEqual(result["configuration"]["temperature"], 0.7)
        self.assertIn("messages", result)
        self.assertIn("verdict", result)
        self.assertIn("ratings", result)
        self.assertIn("convergence", result)
        self.assertIn("latency", result)
        self.assertIn("total_messages", result)
    
    @patch('src.agents.base.ChatOpenAI')
    def test_run_debate_4_agents(self, mock_llm):
        """Test running a debate with 4 agents."""
        # Mock the LLM responses
        mock_response = Mock()
        mock_response.content = "Mock response"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create debate system
        debate_system = DebateSystem()
        
        # Run debate with 4 agents
        result = debate_system.run_debate(
            topic="Test topic",
            rounds=1,
            agent_types=["researcher", "critic", "synthesizer", "judge"],
            temperature=0.7
        )
        
        # Check result structure
        self.assertEqual(result["configuration"]["agents"], ["researcher", "critic", "synthesizer", "judge"])
        self.assertGreaterEqual(len(result["messages"]), 4)  # At least one message per agent
    
    @patch('src.agents.base.ChatOpenAI')
    def test_run_experiment(self, mock_llm):
        """Test running multiple experiments."""
        # Mock the LLM responses
        mock_response = Mock()
        mock_response.content = "Mock response"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create debate system
        debate_system = DebateSystem()
        
        # Define experiment configurations
        experiment_configs = [
            {
                "rounds": 1,
                "agent_types": ["researcher", "judge"],
                "temperature": 0.7,
                "include_devils_advocate": False
            },
            {
                "rounds": 2,
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "temperature": 0.7,
                "include_devils_advocate": False
            }
        ]
        
        # Run experiments
        results = debate_system.run_experiment(
            topic="Test topic",
            experiment_configs=experiment_configs
        )
        
        # Check results
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn("experiment_id", result)
            self.assertIn("configuration", result)
            self.assertIn("debate_result", result)
    
    @patch('src.agents.base.ChatOpenAI')
    def test_compare_experiments(self, mock_llm):
        """Test comparing experiment results."""
        # Mock the LLM responses
        mock_response = Mock()
        mock_response.content = "Mock response"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # Create debate system
        debate_system = DebateSystem()
        
        # Define experiment configurations
        experiment_configs = [
            {
                "rounds": 1,
                "agent_types": ["researcher", "judge"],
                "temperature": 0.7,
                "include_devils_advocate": False
            },
            {
                "rounds": 2,
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "temperature": 0.7,
                "include_devils_advocate": False
            }
        ]
        
        # Run experiments
        results = debate_system.run_experiment(
            topic="Test topic",
            experiment_configs=experiment_configs
        )
        
        # Compare experiments
        comparison = debate_system.compare_experiments(results)
        
        # Check comparison
        self.assertIn("summary", comparison)
        self.assertIn("configurations", comparison)
        self.assertIn("ratings_comparison", comparison)
        self.assertIn("convergence_comparison", comparison)
        self.assertIn("latency_comparison", comparison)
        self.assertIn("message_count_comparison", comparison)
        
        # Check summary
        self.assertEqual(comparison["summary"]["total_experiments"], 2)
        self.assertEqual(len(comparison["configurations"]), 2)

if __name__ == "__main__":
    unittest.main()
