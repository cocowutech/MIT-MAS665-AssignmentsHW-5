"""Evaluation rubric for the multi-agent debate system."""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class RatingScale(Enum):
    """Rating scale for evaluation metrics."""
    POOR = 0
    FAIR = 1
    AVERAGE = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5

@dataclass
class EvaluationCriteria:
    """Criteria for evaluating debate quality."""
    name: str
    description: str
    weight: float = 1.0
    
class DebateEvaluator:
    """Evaluator for debate quality and outcomes."""
    
    def __init__(self):
        self.criteria = {
            "evidence": EvaluationCriteria(
                "Evidence",
                "Quality and sufficiency of evidence provided",
                weight=1.0
            ),
            "feasibility": EvaluationCriteria(
                "Feasibility",
                "Practicality and implementability of proposals",
                weight=1.0
            ),
            "risks": EvaluationCriteria(
                "Risks",
                "Identification and assessment of potential risks",
                weight=1.0
            ),
            "clarity": EvaluationCriteria(
                "Clarity",
                "Clarity and coherence of arguments",
                weight=1.0
            )
        }
    
    def evaluate_debate(self, debate_record: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a debate record using the rubric."""
        
        # Get the ratings from the judge
        judge_ratings = debate_record.get("ratings", {})
        
        # Calculate weighted scores
        total_score = 0
        total_weight = 0
        detailed_scores = {}
        
        for criterion_name, criterion in self.criteria.items():
            rating = judge_ratings.get(criterion_name, 0)
            weighted_score = rating * criterion.weight
            detailed_scores[criterion_name] = {
                "rating": rating,
                "weight": criterion.weight,
                "weighted_score": weighted_score,
                "description": self._get_rating_description(rating)
            }
            total_score += weighted_score
            total_weight += criterion.weight
        
        # Calculate overall score
        overall_score = total_score / total_weight if total_weight > 0 else 0
        
        # Evaluate convergence
        convergence_score = self._evaluate_convergence(debate_record)
        
        # Evaluate message quality
        message_quality = self._evaluate_message_quality(debate_record)
        
        # Create evaluation report
        evaluation = {
            "overall_score": overall_score,
            "overall_rating": self._get_rating_description(overall_score),
            "detailed_scores": detailed_scores,
            "convergence": {
                "achieved": debate_record.get("convergence", False),
                "score": convergence_score,
                "description": self._get_convergence_description(convergence_score)
            },
            "message_quality": message_quality,
            "latency": {
                "seconds": debate_record.get("latency", 0),
                "rating": self._get_latency_rating(debate_record.get("latency", 0))
            },
            "summary": self._generate_summary(evaluation, debate_record)
        }
        
        return evaluation
    
    def _get_rating_description(self, rating: float) -> str:
        """Get a description for a numeric rating."""
        if rating <= 0.5:
            return "Poor - Significant weaknesses"
        elif rating <= 1.5:
            return "Fair - Some strengths but notable weaknesses"
        elif rating <= 2.5:
            return "Average - Balanced strengths and weaknesses"
        elif rating <= 3.5:
            return "Good - Clear strengths with minor weaknesses"
        elif rating <= 4.5:
            return "Very Good - Strong performance with minimal weaknesses"
        else:
            return "Excellent - Outstanding performance"
    
    def _evaluate_convergence(self, debate_record: Dict[str, Any]) -> float:
        """Evaluate the quality of convergence in the debate."""
        if not debate_record.get("convergence", False):
            return 1.0  # Low score for non-convergence
        
        # Check for consensus indicators in the verdict
        verdict = debate_record.get("verdict", {}).get("content", "").lower()
        
        # Strong consensus indicators
        strong_indicators = ["strong consensus", "unanimous", "complete agreement"]
        for indicator in strong_indicators:
            if indicator in verdict:
                return 5.0
        
        # Moderate consensus indicators
        moderate_indicators = ["consensus", "agreement", "converged"]
        for indicator in moderate_indicators:
            if indicator in verdict:
                return 4.0
        
        # Weak consensus indicators
        weak_indicators = ["partial agreement", "some consensus", "mostly agreed"]
        for indicator in weak_indicators:
            if indicator in verdict:
                return 3.0
        
        # Default convergence score
        return 3.5
    
    def _get_convergence_description(self, score: float) -> str:
        """Get a description for the convergence score."""
        if score <= 2.0:
            return "No convergence - Agents remained in disagreement"
        elif score <= 3.0:
            return "Limited convergence - Some progress but significant disagreements remain"
        elif score <= 4.0:
            return "Moderate convergence - General agreement with some reservations"
        else:
            return "Strong convergence - Clear consensus or agreement reached"
    
    def _evaluate_message_quality(self, debate_record: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of messages in the debate."""
        messages = debate_record.get("messages", [])
        
        if not messages:
            return {"average_length": 0, "rating": 0, "description": "No messages to evaluate"}
        
        # Calculate average message length
        total_length = sum(len(msg.get("content", "")) for msg in messages)
        average_length = total_length / len(messages)
        
        # Rate based on average length (simple heuristic)
        if average_length < 100:
            length_rating = 1  # Too short
        elif average_length < 300:
            length_rating = 3  # Good length
        elif average_length < 800:
            length_rating = 5  # Good detailed length
        else:
            length_rating = 4  # Might be too verbose
        
        # Check for role diversity
        roles = set(msg.get("role", "") for msg in messages)
        diversity_score = min(len(roles) / 4, 1.0) * 5  # Normalize to 0-5
        
        # Overall message quality
        overall_quality = (length_rating + diversity_score) / 2
        
        return {
            "average_length": average_length,
            "length_rating": length_rating,
            "role_diversity": {
                "unique_roles": len(roles),
                "roles": list(roles),
                "score": diversity_score
            },
            "overall_quality": overall_quality,
            "description": self._get_message_quality_description(overall_quality)
        }
    
    def _get_message_quality_description(self, score: float) -> str:
        """Get a description for the message quality score."""
        if score <= 2.0:
            return "Poor quality - Messages are too brief or lack diversity"
        elif score <= 3.0:
            return "Fair quality - Messages have some substance but could be improved"
        elif score <= 4.0:
            return "Good quality - Messages are detailed and diverse"
        else:
            return "Excellent quality - Messages are comprehensive and well-balanced"
    
    def _get_latency_rating(self, latency: float) -> str:
        """Get a rating for the debate latency."""
        if latency < 30:
            return "Excellent - Very fast response"
        elif latency < 60:
            return "Good - Reasonable response time"
        elif latency < 120:
            return "Fair - Somewhat slow but acceptable"
        else:
            return "Poor - Slow response time"
    
    def _generate_summary(self, evaluation: Dict[str, Any], debate_record: Dict[str, Any]) -> str:
        """Generate a summary of the evaluation."""
        overall_score = evaluation["overall_score"]
        convergence = evaluation["convergence"]["achieved"]
        
        summary = f"Debate Quality Assessment: {evaluation['overall_rating']} ({overall_score:.1f}/5.0)\n"
        summary += f"Convergence: {'Achieved' if convergence else 'Not Achieved'}\n"
        
        # Highlight strongest and weakest areas
        scores = evaluation["detailed_scores"]
        if scores:
            strongest = max(scores.items(), key=lambda x: x[1]["rating"])
            weakest = min(scores.items(), key=lambda x: x[1]["rating"])
            
            summary += f"Strongest Area: {strongest[0]} ({strongest[1]['rating']}/5)\n"
            summary += f"Weakest Area: {weakest[0]} ({weakest[1]['rating']}/5)\n"
        
        # Add latency information
        latency = evaluation["latency"]["seconds"]
        summary += f"Response Time: {latency:.1f} seconds ({evaluation['latency']['rating']})\n"
        
        return summary
    
    def compare_evaluations(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple debate evaluations."""
        if not evaluations:
            return {"error": "No evaluations to compare"}
        
        comparison = {
            "overall_scores": [e["overall_score"] for e in evaluations],
            "average_score": sum(e["overall_score"] for e in evaluations) / len(evaluations),
            "convergence_rate": sum(1 for e in evaluations if e["convergence"]["achieved"]) / len(evaluations),
            "criteria_comparison": {}
        }
        
        # Compare each criterion
        for criterion in self.criteria.keys():
            scores = [e["detailed_scores"].get(criterion, {}).get("rating", 0) for e in evaluations]
            comparison["criteria_comparison"][criterion] = {
                "scores": scores,
                "average": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores)
            }
        
        return comparison
