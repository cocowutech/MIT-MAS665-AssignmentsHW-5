"""Main entry point for the multi-agent debate system."""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.experiments import ExperimentRunner

def main():
    """Main function to run the debate system."""
    parser = argparse.ArgumentParser(description="Multi-Agent Debate System")
    parser.add_argument("--topic", type=str, required=True, help="Topic for the debate")
    parser.add_argument("--output", type=str, default="Deliverables", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Create experiment runner
    runner = ExperimentRunner()
    
    # Run experiments
    print(f"Running experiments on topic: {args.topic}")
    print("=" * 50)
    
    results = runner.run_standard_experiments(args.topic)
    
    # Generate excerpts
    excerpts = runner.generate_excerpts(results["experiments"])
    
    # Save excerpts
    import json
    from datetime import datetime
    
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    excerpts_file = output_dir / f"excerpts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(excerpts_file, 'w') as f:
        json.dump(excerpts, f, indent=2)
    
    print("=" * 50)
    print("Experiments completed successfully!")
    print(f"Results saved to: {runner.results_dir}")
    print(f"Excerpts saved to: {excerpts_file}")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
