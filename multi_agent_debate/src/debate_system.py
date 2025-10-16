"""Main debate system implementation."""

import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from src.workflow import create_debate_graph, initialize_debate_state
from src.utils.config import config

class DebateSystem:
    """Main system for running multi-agent debates."""
    
    def __init__(self):
        self.config = config
        self.debate_history: List[Dict[str, Any]] = []
    
    def run_debate(
        self,
        topic: str,
        rounds: int = 2,
        agent_types: List[str] = None,
        temperature: float = None,
        include_devils_advocate: bool = False,
        experiment_id: str = None
    ) -> Dict[str, Any]:
        """Run a debate with the specified configuration."""
        
        # Generate experiment ID if not provided
        if experiment_id is None:
            experiment_id = str(uuid.uuid4())
        
        # Validate configuration
        self.config.validate()
        
        # Set defaults
        if agent_types is None:
            agent_types = ["researcher", "critic", "synthesizer", "judge"]
        
        if temperature is None:
            temperature = self.config.default_temperature
        
        # Initialize the debate graph
        graph = create_debate_graph(
            agent_types=agent_types,
            rounds=rounds,
            temperature=temperature,
            include_devils_advocate=include_devils_advocate
        )
        
        # Initialize the debate state
        initial_state = initialize_debate_state(
            topic=topic,
            rounds=rounds,
            agent_types=agent_types,
            temperature=temperature,
            include_devils_advocate=include_devils_advocate
        )
        
        # Run the debate
        start_time = time.time()
        
        # Configure the graph with thread ID for memory
        thread_config = {"configurable": {"thread_id": experiment_id}}
        
        # Run the debate
        result = graph.invoke(initial_state, thread_config)
        
        end_time = time.time()
        latency = end_time - start_time
        
        # Create debate record
        debate_record = {
            "experiment_id": experiment_id,
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "configuration": {
                "rounds": rounds,
                "agents": agent_types,
                "temperature": temperature,
                "include_devils_advocate": include_devils_advocate
            },
            "messages": result["messages"],
            "verdict": result["verdict"],
            "ratings": result["ratings"],
            "convergence": result["convergence"],
            "latency": latency,
            "total_messages": len(result["messages"])
        }
        
        # Add to history
        self.debate_history.append(debate_record)
        
        return debate_record
    
    def run_experiment(
        self,
        topic: str,
        experiment_configs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Run multiple experiments with different configurations."""
        
        results = []
        
        for i, exp_config in enumerate(experiment_configs):
            print(f"Running experiment {i+1}/{len(experiment_configs)}...")
            
            # Extract configuration
            rounds = exp_config.get("rounds", 2)
            agent_types = exp_config.get("agent_types", ["researcher", "critic", "synthesizer", "judge"])
            temperature = exp_config.get("temperature", self.config.default_temperature)
            include_devils_advocate = exp_config.get("include_devils_advocate", False)
            
            # Run the debate
            result = self.run_debate(
                topic=topic,
                rounds=rounds,
                agent_types=agent_types,
                temperature=temperature,
                include_devils_advocate=include_devils_advocate,
                experiment_id=f"exp_{i+1}"
            )
            
            results.append(result)
        
        return results
    
    def compare_experiments(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare results from multiple experiments."""
        
        if not results:
            return {"error": "No results to compare"}
        
        comparison = {
            "summary": {
                "total_experiments": len(results),
                "topics": list(set(r["topic"] for r in results)),
                "date_range": {
                    "start": min(r["timestamp"] for r in results),
                    "end": max(r["timestamp"] for r in results)
                }
            },
            "configurations": [],
            "ratings_comparison": {},
            "convergence_comparison": {},
            "latency_comparison": {},
            "message_count_comparison": {}
        }
        
        # Extract configurations
        for result in results:
            comparison["configurations"].append(result["configuration"])
        
        # Compare ratings
        for metric in ["evidence", "feasibility", "risks", "clarity"]:
            values = [r["ratings"].get(metric, 0) for r in results]
            comparison["ratings_comparison"][metric] = {
                "values": values,
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        
        # Compare convergence
        convergence_count = sum(1 for r in results if r["convergence"])
        comparison["convergence_comparison"] = {
            "converged": convergence_count,
            "diverged": len(results) - convergence_count,
            "convergence_rate": convergence_count / len(results)
        }
        
        # Compare latency
        latencies = [r["latency"] for r in results]
        comparison["latency_comparison"] = {
            "values": latencies,
            "average": sum(latencies) / len(latencies),
            "min": min(latencies),
            "max": max(latencies)
        }
        
        # Compare message counts
        message_counts = [r["total_messages"] for r in results]
        comparison["message_count_comparison"] = {
            "values": message_counts,
            "average": sum(message_counts) / len(message_counts),
            "min": min(message_counts),
            "max": max(message_counts)
        }
        
        return comparison
    
    def get_debate_by_id(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific debate by its experiment ID."""
        for debate in self.debate_history:
            if debate["experiment_id"] == experiment_id:
                return debate
        return None
    
    def get_all_debates(self) -> List[Dict[str, Any]]:
        """Get all debate records."""
        return self.debate_history.copy()
    
    def save_debate_to_file(self, experiment_id: str, filepath: str) -> bool:
        """Save a debate record to a file."""
        debate = self.get_debate_by_id(experiment_id)
        if debate is None:
            return False
        
        try:
            import json
            with open(filepath, 'w') as f:
                json.dump(debate, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_debate_from_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load a debate record from a file."""
        try:
            import json
            with open(filepath, 'r') as f:
                debate = json.load(f)
            
            # Add to history if not already present
            if not any(d["experiment_id"] == debate["experiment_id"] for d in self.debate_history):
                self.debate_history.append(debate)
            
            return debate
        except Exception:
            return None
