"""Unit tests for evaluation components."""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from src.evaluation import DebateEvaluator, EvaluationCriteria, RatingScale

class TestDebateEvaluator(unittest.TestCase):
    """Test the debate evaluator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DebateEvaluator()
    
    def test_initialization(self):
        """Test evaluator initialization."""
        self.assertIn("evidence", self.evaluator.criteria)
        self.assertIn("feasibility", self.evaluator.criteria)
        self.assertIn("risks", self.evaluator.criteria)
        self.assertIn("clarity", self.evaluator.criteria)
    
    def test_evaluate_debate(self):
        """Test debate evaluation."""
        # Create a mock debate record
        debate_record = {
            "ratings": {
                "evidence": 4,
                "feasibility": 3,
                "risks": 2,
                "clarity": 4
            },
            "convergence": True,
            "latency": 45.5,
            "messages": [
                {"role": "researcher", "content": "Research findings" * 10},
                {"role": "critic", "content": "Critical analysis" * 10},
                {"role": "synthesizer", "content": "Synthesis of views" * 10},
                {"role": "judge", "content": "Final verdict" * 10}
            ],
            "verdict": {
                "content": "After careful consideration, there is strong consensus on this topic."
            }
        }
        
        # Evaluate the debate
        evaluation = self.evaluator.evaluate_debate(debate_record)
        
        # Check evaluation results
        self.assertEqual(evaluation["overall_score"], 3.25)  # (4+3+2+4)/4
        self.assertIn("detailed_scores", evaluation)
        self.assertIn("convergence", evaluation)
        self.assertIn("message_quality", evaluation)
        self.assertIn("latency", evaluation)
        self.assertIn("summary", evaluation)
        
        # Check detailed scores
        self.assertEqual(evaluation["detailed_scores"]["evidence"]["rating"], 4)
        self.assertEqual(evaluation["detailed_scores"]["feasibility"]["rating"], 3)
        self.assertEqual(evaluation["detailed_scores"]["risks"]["rating"], 2)
        self.assertEqual(evaluation["detailed_scores"]["clarity"]["rating"], 4)
        
        # Check convergence
        self.assertTrue(evaluation["convergence"]["achieved"])
        self.assertGreater(evaluation["convergence"]["score"], 3.0)
    
    def test_evaluate_debate_no_convergence(self):
        """Test debate evaluation with no convergence."""
        # Create a mock debate record with no convergence
        debate_record = {
            "ratings": {
                "evidence": 2,
                "feasibility": 2,
                "risks": 2,
                "clarity": 2
            },
            "convergence": False,
            "latency": 120.0,
            "messages": [
                {"role": "researcher", "content": "Short research"},
                {"role": "critic", "content": "Brief critique"}
            ],
            "verdict": {
                "content": "No agreement was reached on this topic."
            }
        }
        
        # Evaluate the debate
        evaluation = self.evaluator.evaluate_debate(debate_record)
        
        # Check evaluation results
        self.assertEqual(evaluation["overall_score"], 2.0)
        self.assertFalse(evaluation["convergence"]["achieved"])
        self.assertEqual(evaluation["convergence"]["score"], 1.0)
    
    def test_compare_evaluations(self):
        """Test comparing multiple evaluations."""
        # Create mock evaluations
        evaluations = [
            {
                "overall_score": 3.0,
                "convergence": {"achieved": True},
                "detailed_scores": {
                    "evidence": {"rating": 3},
                    "feasibility": {"rating": 3},
                    "risks": {"rating": 3},
                    "clarity": {"rating": 3}
                }
            },
            {
                "overall_score": 4.0,
                "convergence": {"achieved": False},
                "detailed_scores": {
                    "evidence": {"rating": 4},
                    "feasibility": {"rating": 4},
                    "risks": {"rating": 4},
                    "clarity": {"rating": 4}
                }
            }
        ]
        
        # Compare evaluations
        comparison = self.evaluator.compare_evaluations(evaluations)
        
        # Check comparison results
        self.assertEqual(comparison["overall_scores"], [3.0, 4.0])
        self.assertEqual(comparison["average_score"], 3.5)
        self.assertEqual(comparison["convergence_rate"], 0.5)
        
        # Check criteria comparison
        self.assertEqual(comparison["criteria_comparison"]["evidence"]["average"], 3.5)
        self.assertEqual(comparison["criteria_comparison"]["evidence"]["min"], 3)
        self.assertEqual(comparison["criteria_comparison"]["evidence"]["max"], 4)

class TestEvaluationCriteria(unittest.TestCase):
    """Test the evaluation criteria functionality."""
    
    def test_criteria_creation(self):
        """Test creating evaluation criteria."""
        criteria = EvaluationCriteria(
            name="Test Criteria",
            description="A test criteria for evaluation",
            weight=1.5
        )
        
        self.assertEqual(criteria.name, "Test Criteria")
        self.assertEqual(criteria.description, "A test criteria for evaluation")
        self.assertEqual(criteria.weight, 1.5)

class TestRatingScale(unittest.TestCase):
    """Test the rating scale enum."""
    
    def test_rating_values(self):
        """Test rating scale values."""
        self.assertEqual(RatingScale.POOR.value, 0)
        self.assertEqual(RatingScale.FAIR.value, 1)
        self.assertEqual(RatingScale.AVERAGE.value, 2)
        self.assertEqual(RatingScale.GOOD.value, 3)
        self.assertEqual(RatingScale.VERY_GOOD.value, 4)
        self.assertEqual(RatingScale.EXCELLENT.value, 5)

if __name__ == "__main__":
    unittest.main()
