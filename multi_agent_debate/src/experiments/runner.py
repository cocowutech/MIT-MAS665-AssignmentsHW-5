"""Experiment runner for the multi-agent debate system."""

import json
import time
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from src.debate_system import DebateSystem
from src.evaluation import DebateEvaluator
from src.utils.config import config

class ExperimentRunner:
    """Runner for conducting experiments with different configurations."""
    
    def __init__(self):
        self.debate_system = DebateSystem()
        self.evaluator = DebateEvaluator()
        self.results_dir = Path("experiments/results")
        self.results_dir.mkdir(exist_ok=True)
    
    def run_standard_experiments(self, topic: str) -> Dict[str, Any]:
        """Run the standard set of experiments as specified in the requirements."""
        
        # Define experiment configurations
        experiment_configs = [
            # Experiment 1: 2 agents vs 4 agents
            {
                "name": "2_agents",
                "description": "Debate with 2 agents (Researcher, Judge)",
                "agent_types": ["researcher", "judge"],
                "rounds": 2,
                "temperature": config.default_temperature,
                "include_devils_advocate": False
            },
            {
                "name": "4_agents",
                "description": "Debate with 4 agents (Researcher, Critic, Synthesizer, Judge)",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 2,
                "temperature": config.default_temperature,
                "include_devils_advocate": False
            },
            
            # Experiment 2: 1 round vs 3 rounds
            {
                "name": "1_round",
                "description": "Debate with 1 round",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 1,
                "temperature": config.default_temperature,
                "include_devils_advocate": False
            },
            {
                "name": "3_rounds",
                "description": "Debate with 3 rounds",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 3,
                "temperature": config.default_temperature,
                "include_devils_advocate": False
            },
            
            # Experiment 3: With and without Devil's Advocate
            {
                "name": "without_devils_advocate",
                "description": "Debate without Devil's Advocate",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 2,
                "temperature": config.default_temperature,
                "include_devils_advocate": False
            },
            {
                "name": "with_devils_advocate",
                "description": "Debate with Devil's Advocate",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 2,
                "temperature": config.default_temperature,
                "include_devils_advocate": True
            },
            
            # Experiment 4: Low vs High temperature
            {
                "name": "low_temperature",
                "description": "Debate with low temperature (0.2)",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 2,
                "temperature": config.low_temperature,
                "include_devils_advocate": False
            },
            {
                "name": "high_temperature",
                "description": "Debate with high temperature (0.9)",
                "agent_types": ["researcher", "critic", "synthesizer", "judge"],
                "rounds": 2,
                "temperature": config.high_temperature,
                "include_devils_advocate": False
            }
        ]
        
        # Run experiments
        results = []
        for exp_config in experiment_configs:
            print(f"Running experiment: {exp_config['name']}")
            print(f"Description: {exp_config['description']}")
            
            # Run the debate
            debate_result = self.debate_system.run_debate(
                topic=topic,
                rounds=exp_config["rounds"],
                agent_types=exp_config["agent_types"],
                temperature=exp_config["temperature"],
                include_devils_advocate=exp_config["include_devils_advocate"],
                experiment_id=exp_config["name"]
            )
            
            # Evaluate the debate
            evaluation = self.evaluator.evaluate_debate(debate_result)
            
            # Combine results
            experiment_result = {
                "experiment_name": exp_config["name"],
                "description": exp_config["description"],
                "configuration": {
                    "rounds": exp_config["rounds"],
                    "agents": exp_config["agent_types"],
                    "temperature": exp_config["temperature"],
                    "include_devils_advocate": exp_config["include_devils_advocate"]
                },
                "debate_result": debate_result,
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(experiment_result)
            
            # Save individual result
            self.save_experiment_result(experiment_result)
            
            print(f"Completed experiment: {exp_config['name']}")
            print(f"Overall score: {evaluation['overall_score']:.1f}/5.0")
            print(f"Convergence: {'Yes' if evaluation['convergence']['achieved'] else 'No'}")
            print(f"Latency: {evaluation['latency']['seconds']:.1f} seconds")
            print("-" * 50)
        
        # Create comparison report
        comparison = self.create_comparison_report(results)
        
        # Save complete experiment set
        complete_results = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "experiments": results,
            "comparison": comparison
        }
        
        self.save_complete_results(complete_results)
        
        return complete_results
    
    def save_experiment_result(self, result: Dict[str, Any]):
        """Save an individual experiment result."""
        filename = f"{result['experiment_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
    
    def save_complete_results(self, results: Dict[str, Any]):
        """Save the complete set of experiment results."""
        filename = f"complete_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
    
    def create_comparison_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a comparison report from experiment results."""
        
        # Extract evaluations for comparison
        evaluations = [r["evaluation"] for r in results]
        
        # Use the evaluator to compare
        comparison = self.evaluator.compare_evaluations(evaluations)
        
        # Add experiment-specific comparisons
        comparison["experiment_comparisons"] = {}
        
        # Compare 2 vs 4 agents
        agents_2 = next((r for r in results if r["experiment_name"] == "2_agents"), None)
        agents_4 = next((r for r in results if r["experiment_name"] == "4_agents"), None)
        
        if agents_2 and agents_4:
            comparison["experiment_comparisons"]["agents_2_vs_4"] = {
                "2_agents_score": agents_2["evaluation"]["overall_score"],
                "4_agents_score": agents_4["evaluation"]["overall_score"],
                "difference": agents_4["evaluation"]["overall_score"] - agents_2["evaluation"]["overall_score"],
                "2_agents_convergence": agents_2["evaluation"]["convergence"]["achieved"],
                "4_agents_convergence": agents_4["evaluation"]["convergence"]["achieved"],
                "2_agents_latency": agents_2["evaluation"]["latency"]["seconds"],
                "4_agents_latency": agents_4["evaluation"]["latency"]["seconds"]
            }
        
        # Compare 1 vs 3 rounds
        rounds_1 = next((r for r in results if r["experiment_name"] == "1_round"), None)
        rounds_3 = next((r for r in results if r["experiment_name"] == "3_rounds"), None)
        
        if rounds_1 and rounds_3:
            comparison["experiment_comparisons"]["rounds_1_vs_3"] = {
                "1_round_score": rounds_1["evaluation"]["overall_score"],
                "3_rounds_score": rounds_3["evaluation"]["overall_score"],
                "difference": rounds_3["evaluation"]["overall_score"] - rounds_1["evaluation"]["overall_score"],
                "1_round_convergence": rounds_1["evaluation"]["convergence"]["achieved"],
                "3_rounds_convergence": rounds_3["evaluation"]["convergence"]["achieved"],
                "1_round_latency": rounds_1["evaluation"]["latency"]["seconds"],
                "3_round_latency": rounds_3["evaluation"]["latency"]["seconds"]
            }
        
        # Compare with vs without Devil's Advocate
        without_da = next((r for r in results if r["experiment_name"] == "without_devils_advocate"), None)
        with_da = next((r for r in results if r["experiment_name"] == "with_devils_advocate"), None)
        
        if without_da and with_da:
            comparison["experiment_comparisons"]["devils_advocate"] = {
                "without_da_score": without_da["evaluation"]["overall_score"],
                "with_da_score": with_da["evaluation"]["overall_score"],
                "difference": with_da["evaluation"]["overall_score"] - without_da["evaluation"]["overall_score"],
                "without_da_convergence": without_da["evaluation"]["convergence"]["achieved"],
                "with_da_convergence": with_da["evaluation"]["convergence"]["achieved"],
                "without_da_latency": without_da["evaluation"]["latency"]["seconds"],
                "with_da_latency": with_da["evaluation"]["latency"]["seconds"]
            }
        
        # Compare low vs high temperature
        low_temp = next((r for r in results if r["experiment_name"] == "low_temperature"), None)
        high_temp = next((r for r in results if r["experiment_name"] == "high_temperature"), None)
        
        if low_temp and high_temp:
            comparison["experiment_comparisons"]["temperature"] = {
                "low_temp_score": low_temp["evaluation"]["overall_score"],
                "high_temp_score": high_temp["evaluation"]["overall_score"],
                "difference": high_temp["evaluation"]["overall_score"] - low_temp["evaluation"]["overall_score"],
                "low_temp_convergence": low_temp["evaluation"]["convergence"]["achieved"],
                "high_temp_convergence": high_temp["evaluation"]["convergence"]["achieved"],
                "low_temp_latency": low_temp["evaluation"]["latency"]["seconds"],
                "high_temp_latency": high_temp["evaluation"]["latency"]["seconds"]
            }
        
        return comparison
    
    def generate_excerpts(self, results: List[Dict[str, Any]], num_excerpts: int = 3) -> List[Dict[str, Any]]:
        """Generate interesting excerpts from the debate results."""
        excerpts = []
        
        for result in results:
            messages = result["debate_result"]["messages"]
            
            # Find interesting exchanges
            for i, message in enumerate(messages):
                # Look for critic catching an error
                if message.get("role") == "critic" and i > 0:
                    prev_message = messages[i-1]
                    if any(keyword in message.get("content", "").lower() 
                          for keyword in ["error", "flaw", "incorrect", "mistake", "weakness"]):
                        excerpts.append({
                            "experiment": result["experiment_name"],
                            "type": "critic_catching_error",
                            "context": prev_message.get("content", "")[:200] + "...",
                            "critic_response": message.get("content", "")[:300] + "...",
                            "round": message.get("round", 0)
                        })
                
                # Look for synthesis of different views
                if message.get("role") == "synthesizer" and i > 1:
                    excerpts.append({
                        "experiment": result["experiment_name"],
                        "type": "synthesis",
                        "synthesis": message.get("content", "")[:300] + "...",
                        "round": message.get("round", 0)
                    })
                
                # Look for judge's verdict
                if message.get("role") == "judge":
                    excerpts.append({
                        "experiment": result["experiment_name"],
                        "type": "verdict",
                        "verdict": message.get("content", "")[:300] + "...",
                        "round": message.get("round", 0)
                    })
        
        # Return a selection of excerpts
        return excerpts[:num_excerpts]
