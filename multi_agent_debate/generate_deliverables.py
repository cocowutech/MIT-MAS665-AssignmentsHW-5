"""Script to generate deliverables for the multi-agent debate system."""

import json
import sys
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from datetime import datetime
import os

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.experiments import ExperimentRunner
from src.evaluation import DebateEvaluator
from src.debate_system import DebateSystem

def create_diagram():
    """Create a diagram of agent roles and message flow."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define agent positions
    agents = ["Researcher", "Critic", "Synthesizer", "Judge"]
    positions = [(1, 3), (3, 3), (5, 3), (7, 3)]
    
    # Draw agents
    for i, (agent, pos) in enumerate(zip(agents, positions)):
        ax.add_patch(plt.Circle(pos, 0.5, color='skyblue', alpha=0.7))
        ax.text(pos[0], pos[1], agent, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw message flow
    for i in range(len(positions) - 1):
        ax.arrow(positions[i][0] + 0.5, positions[i][1], 
                positions[i+1][0] - positions[i][0] - 1, 0,
                head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # Add round indicators
    ax.text(4, 1.5, "Round 1 → Round 2 → ...", ha='center', va='center', fontsize=12)
    
    # Set plot properties
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Multi-Agent Debate System: Roles & Message Flow", fontsize=14, fontweight='bold')
    
    # Save diagram
    diagram_path = Path("Deliverables/diagram.png")
    diagram_path.parent.mkdir(exist_ok=True)
    plt.savefig(diagram_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return diagram_path

def create_proof_of_execution(results):
    """Create proof of execution document."""
    proof_path = Path("Deliverables/proof_of_execution.md")
    proof_path.parent.mkdir(exist_ok=True)
    
    with open(proof_path, 'w') as f:
        f.write("# Multi-Agent Debate System: Proof of Execution\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Add diagram
        f.write("## System Architecture\n\n")
        f.write("![Agent Roles & Message Flow](diagram.png)\n\n")
        
        # Add configuration summary
        f.write("## Configuration Summary\n\n")
        f.write("| Parameter | Value |\n")
        f.write("|-----------|-------|\n")
        f.write(f"| Model | GLM-4.6 |\n")
        f.write(f"| Base URL | https://api.z.ai/api/coding/paas/v4/ |\n")
        f.write(f"| Default Temperature | 0.7 |\n")
        f.write(f"| Low Temperature | 0.2 |\n")
        f.write(f"| High Temperature | 0.9 |\n")
        f.write(f"| Default Rounds | 2 |\n")
        f.write(f"| Default Agents | 4 |\n")
        f.write(f"| Max Tokens | 1000 |\n\n")
        
        # Add experiment results
        f.write("## Experiment Results\n\n")
        f.write(f"Topic: {results['topic']}\n\n")
        
        for exp in results['experiments']:
            f.write(f"### {exp['experiment_name']}\n\n")
            f.write(f"Description: {exp['description']}\n\n")
            f.write(f"Configuration: {exp['configuration']}\n\n")
            f.write(f"Overall Score: {exp['evaluation']['overall_score']:.1f}/5.0\n\n")
            f.write(f"Convergence: {'Yes' if exp['evaluation']['convergence']['achieved'] else 'No'}\n\n")
            f.write(f"Latency: {exp['evaluation']['latency']['seconds']:.1f} seconds\n\n")
            
            # Add sample messages
            f.write("#### Sample Messages:\n\n")
            for i, msg in enumerate(exp['debate_result']['messages'][:2]):  # First 2 messages
                f.write(f"**{msg['role'].title()} (Round {msg['round']}):**\n")
                f.write(f"{msg['content'][:200]}...\n\n")
            
            # Add verdict
            if exp['debate_result']['verdict']:
                f.write("#### Final Verdict:\n\n")
                verdict = exp['debate_result']['verdict']['content']
                f.write(f"{verdict[:300]}...\n\n")
            
            f.write("---\n\n")
        
        # Add comparison
        f.write("## Comparison Results\n\n")
        comparison = results['comparison']
        
        f.write("### Experiment Comparisons:\n\n")
        for exp_name, exp_comp in comparison.get('experiment_comparisons', {}).items():
            f.write(f"#### {exp_name.replace('_', ' ').title()}\n\n")
            for key, value in exp_comp.items():
                f.write(f"- {key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
    
    return proof_path

def create_mini_report(results):
    """Create a mini-report with experiment results."""
    report_path = Path("Deliverables/mini_report.md")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# Multi-Agent Debate System: Mini-Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Scenario and acceptance criteria
        f.write("## Scenario Tested\n\n")
        f.write(f"**Topic:** {results['topic']}\n\n")
        f.write("**Acceptance Criteria:**\n")
        f.write("1. System supports 2-4 agents with distinct roles\n")
        f.write("2. Protocol supports at least 2 rounds of debate\n")
        f.write("3. Judge provides final verdict or indicates non-consensus\n")
        f.write("4. System runs locally on a single machine\n")
        f.write("5. System supports experiment toggles (agents, rounds, temperature)\n\n")
        
        # Results table
        f.write("## Results Table\n\n")
        f.write("| Experiment | Agents | Rounds | Temperature | Score | Convergence | Latency (s) |\n")
        f.write("|------------|--------|--------|-------------|-------|-------------|-------------|\n")
        
        for exp in results['experiments']:
            config = exp['configuration']
            agents_count = len(config['agents'])
            rounds = config['rounds']
            temp = config['temperature']
            score = exp['evaluation']['overall_score']
            conv = 'Yes' if exp['evaluation']['convergence']['achieved'] else 'No'
            latency = exp['evaluation']['latency']['seconds']
            
            f.write(f"| {exp['experiment_name']} | {agents_count} | {rounds} | {temp} | {score:.1f} | {conv} | {latency:.1f} |\n")
        
        f.write("\n")
        
        # Detailed rubric scores
        f.write("### Detailed Rubric Scores\n\n")
        f.write("| Experiment | Evidence | Feasibility | Risks | Clarity |\n")
        f.write("|------------|----------|-------------|-------|---------|\n")
        
        for exp in results['experiments']:
            scores = exp['evaluation']['detailed_scores']
            evidence = scores['evidence']['rating']
            feasibility = scores['feasibility']['rating']
            risks = scores['risks']['rating']
            clarity = scores['clarity']['rating']
            
            f.write(f"| {exp['experiment_name']} | {evidence} | {feasibility} | {risks} | {clarity} |\n")
        
        f.write("\n")
        
        # What changed with toggles
        f.write("## What Changed with Toggles\n\n")
        comparison = results['comparison']
        
        for exp_name, exp_comp in comparison.get('experiment_comparisons', {}).items():
            f.write(f"### {exp_name.replace('_', ' ').title()}\n\n")
            
            if 'difference' in exp_comp:
                diff = exp_comp['difference']
                if diff > 0:
                    f.write(f"- **Score Improvement:** +{diff:.1f} points\n")
                elif diff < 0:
                    f.write(f"- **Score Decrease:** {diff:.1f} points\n")
                else:
                    f.write("- **No Change in Score**\n")
            
            if 'convergence' in exp_name.lower():
                f.write(f"- **Convergence Change:** ")
                if exp_comp.get(f"{exp_name.split('_')[0]}_convergence") != exp_comp.get(f"{exp_name.split('_')[-1]}_convergence"):
                    f.write("Convergence status changed between configurations\n")
                else:
                    f.write("No change in convergence status\n")
            
            if 'latency' in exp_comp:
                latency_diff = exp_comp.get(f"{exp_name.split('_')[-1]}_latency", 0) - exp_comp.get(f"{exp_name.split('_')[0]}_latency", 0)
                if latency_diff > 0:
                    f.write(f"- **Latency Increase:** +{latency_diff:.1f} seconds\n")
                elif latency_diff < 0:
                    f.write(f"- **Latency Decrease:** {latency_diff:.1f} seconds\n")
                else:
                    f.write("- **No Change in Latency**\n")
            
            f.write("\n")
        
        # Limits and next steps
        f.write("## Limits and Next Steps\n\n")
        f.write("### Current Limitations\n\n")
        f.write("1. **Simplified Rating Extraction:** The system uses basic text parsing to extract numerical ratings from the judge's verdict, which may not always be accurate.\n")
        f.write("2. **Limited Context Window:** The system has a fixed maximum token limit, which may constrain very long debates.\n")
        f.write("3. **Deterministic Workflow:** The current implementation follows a fixed agent sequence, which doesn't allow for dynamic agent selection based on debate content.\n")
        f.write("4. **Basic Convergence Detection:** Convergence is determined through simple keyword matching rather than semantic analysis.\n\n")
        
        f.write("### Next Steps\n\n")
        f.write("1. **Enhanced Rating Extraction:** Implement more sophisticated NLP techniques to accurately extract and interpret ratings from judge's verdicts.\n")
        f.write("2. **Dynamic Agent Selection:** Develop a mechanism to dynamically select which agent should respond next based on the current state of the debate.\n")
        f.write("3. **Semantic Convergence Analysis:** Use semantic similarity measures to more accurately determine when agents have reached consensus.\n")
        f.write("4. **Expanded Agent Roles:** Introduce additional specialized agents (e.g., Ethicist, Economist, Technical Expert) for more domain-specific debates.\n")
        f.write("5. **Longer Context Support:** Implement strategies to handle longer debates, such as summarization or hierarchical memory.\n\n")
    
    return report_path

def create_results_visualization(results):
    """Create visualizations of the experiment results."""
    viz_path = Path("Deliverables/results_visualization.png")
    viz_path.parent.mkdir(exist_ok=True)
    
    # Extract data for visualization
    experiments = [exp['experiment_name'] for exp in results['experiments']]
    scores = [exp['evaluation']['overall_score'] for exp in results['experiments']]
    latencies = [exp['evaluation']['latency']['seconds'] for exp in results['experiments']]
    convergence = [1 if exp['evaluation']['convergence']['achieved'] else 0 for exp in results['experiments']]
    
    # Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    # Plot scores
    bars1 = ax1.bar(experiments, scores, color='skyblue')
    ax1.set_ylabel('Score (0-5)')
    ax1.set_title('Overall Debate Quality Scores')
    ax1.set_ylim(0, 5)
    
    # Add value labels on bars
    for bar, score in zip(bars1, scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{score:.1f}', ha='center', va='bottom')
    
    # Plot latencies
    bars2 = ax2.bar(experiments, latencies, color='lightgreen')
    ax2.set_ylabel('Latency (seconds)')
    ax2.set_title('Debate Latency')
    
    # Add value labels on bars
    for bar, latency in zip(bars2, latencies):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(latencies)*0.01,
                f'{latency:.1f}s', ha='center', va='bottom')
    
    # Plot convergence
    bars3 = ax3.bar(experiments, convergence, color='salmon')
    ax3.set_ylabel('Convergence (0=No, 1=Yes)')
    ax3.set_title('Debate Convergence')
    ax3.set_ylim(0, 1.2)
    
    # Add value labels on bars
    for bar, conv in zip(bars3, convergence):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                'Yes' if conv else 'No', ha='center', va='bottom')
    
    # Rotate x-axis labels for better readability
    for ax in [ax1, ax2, ax3]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(viz_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return viz_path

def create_experiment_graphs(results):
    """Create graph visualizations for each experiment."""
    debate_system = DebateSystem()
    graph_paths = []
    
    # Create graphs directory
    graphs_dir = Path("Deliverables/graphs")
    graphs_dir.mkdir(exist_ok=True, parents=True)
    
    for exp in results['experiments']:
        config = exp['configuration']
        experiment_id = exp['experiment_id']
        
        # Create graph visualization
        graph_path = debate_system.visualize_debate_graph(
            agent_types=config['agents'],
            rounds=config['rounds'],
            temperature=config['temperature'],
            include_devils_advocate=config.get('include_devils_advocate', False),
            experiment_id=experiment_id,
            output_dir="Deliverables/graphs"
        )
        
        graph_paths.append({
            "experiment_id": experiment_id,
            "experiment_name": exp['experiment_name'],
            "graph_path": graph_path
        })
    
    return graph_paths

def main():
    """Main function to generate all deliverables."""
    print("Generating deliverables for the multi-agent debate system...")
    
    # Check if results exist
    results_dir = Path("experiments/results")
    if not results_dir.exists():
        print("No experiment results found. Running experiments first...")
        
        # Create experiment runner
        runner = ExperimentRunner()
        
        # Run experiments with a sample topic
        topic = "Should artificial intelligence be regulated to ensure ethical development?"
        results = runner.run_standard_experiments(topic)
    else:
        # Load the most recent results
        result_files = list(results_dir.glob("complete_results_*.json"))
        if not result_files:
            print("No complete results found. Running experiments first...")
            runner = ExperimentRunner()
            topic = "Should artificial intelligence be regulated to ensure ethical development?"
            results = runner.run_standard_experiments(topic)
        else:
            # Load the most recent results
            latest_file = max(result_files, key=lambda f: f.stat().st_mtime)
            with open(latest_file, 'r') as f:
                results = json.load(f)
    
    # Create diagram
    print("Creating system diagram...")
    diagram_path = create_diagram()
    
    # Create proof of execution
    print("Creating proof of execution...")
    proof_path = create_proof_of_execution(results)
    
    # Create mini-report
    print("Creating mini-report...")
    report_path = create_mini_report(results)
    
    # Create results visualization
    print("Creating results visualization...")
    viz_path = create_results_visualization(results)

    # Create experiment graphs
    print("Creating experiment graphs...")
    graph_paths = create_experiment_graphs(results)
    
    # Create complete flow visualization
    print("Creating complete flow visualization...")
    import sys
    sys.path.append(str(Path(__file__).parent / "Deliverables" / "graphs"))
    from complete_flow_visualization import create_complete_flow_visualization
    flow_viz_path = create_complete_flow_visualization()
    
    print("\nDeliverables generated successfully!")
    print(f"Diagram: {diagram_path}")
    print(f"Proof of Execution: {proof_path}")
    print(f"Mini-Report: {report_path}")
    print(f"Results Visualization: {viz_path}")
    print(f"Experiment Graphs: {graph_paths}")
    print(f"Complete Flow Visualization: {flow_viz_path}")
    
    # Create a summary file with all deliverable paths
    summary_path = Path("Deliverables/README.md")
    with open(summary_path, 'w') as f:
        f.write("# Multi-Agent Debate System: Deliverables\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Deliverable Files\n\n")
        f.write(f"- [System Diagram](diagram.png)\n")
        f.write(f"- [Proof of Execution](proof_of_execution.md)\n")
        f.write(f"- [Mini-Report](mini_report.md)\n")
        f.write(f"- [Results Visualization](results_visualization.png)\n")
        f.write(f"- [Experiment Graphs](graphs/)\n")
        f.write(f"- [Complete Flow Visualization](complete_flow_visualization.png)\n\n")
        f.write("## Experiment Results\n\n")
        f.write(f"Topic: {results['topic']}\n\n")
        f.write("For detailed experiment results, see the files in the `experiments/results/` directory.\n\n")
        
        # Add experiment graph information
        f.write("## Experiment Graphs\n\n")
        f.write("Each experiment has a corresponding graph visualization showing the agent flow:\n\n")
        
        for graph_info in graph_paths:
            exp_name = graph_info['experiment_name']
            exp_id = graph_info['experiment_id']
            graph_file = Path(graph_info['graph_path']).name
            
            f.write(f"### {exp_name}\n\n")
            f.write(f"- [Graph Visualization](graphs/{graph_file})\n")
            f.write(f"- Experiment ID: {exp_id}\n\n")
    
    print(f"Summary file created: {summary_path}")

if __name__ == "__main__":
    main()
