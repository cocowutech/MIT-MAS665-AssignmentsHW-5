"""Script to create a comprehensive visualization of the complete debate flow."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def create_complete_flow_visualization():
    """Create a comprehensive visualization of the complete debate flow with all participants."""
    
    # Create figure with subplots for different configurations
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Multi-Agent Debate System: Complete Flow Visualization', fontsize=16, fontweight='bold')
    
    # Define colors for different agents
    agent_colors = {
        'researcher': '#3498db',      # Blue
        'critic': '#e74c3c',         # Red
        'devils_advocate': '#f39c12', # Orange
        'synthesizer': '#2ecc71',     # Green
        'judge': '#9b59b6'          # Purple
    }
    
    # 1. Standard 4-Agent Configuration
    ax1.set_title('Standard 4-Agent Configuration', fontweight='bold')
    agents_4 = ['researcher', 'critic', 'synthesizer', 'judge']
    positions_4 = [(1, 3), (3, 3), (5, 3), (7, 3)]
    
    # Draw agents
    for i, (agent, pos) in enumerate(zip(agents_4, positions_4)):
        ax1.add_patch(patches.Circle(pos, 0.5, color=agent_colors[agent], alpha=0.7))
        ax1.text(pos[0], pos[1], agent.title(), ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    
    # Draw message flow
    for i in range(len(positions_4) - 1):
        ax1.arrow(positions_4[i][0] + 0.5, positions_4[i][1], 
                positions_4[i+1][0] - positions_4[i][0] - 1, 0,
                head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    # Add start and end
    ax1.add_patch(patches.Circle((0, 3), 0.3, color='gray', alpha=0.7))
    ax1.text(0, 3, 'START', ha='center', va='center', fontsize=8, fontweight='bold')
    ax1.add_patch(patches.Circle((8.5, 3), 0.3, color='gray', alpha=0.7))
    ax1.text(8.5, 3, 'END', ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax1.arrow(0.3, 3, 0.4, 0, head_width=0.15, head_length=0.15, fc='black', ec='black')
    ax1.arrow(7.5, 3, 0.7, 0, head_width=0.15, head_length=0.15, fc='black', ec='black')
    
    ax1.set_xlim(-0.5, 9)
    ax1.set_ylim(1.5, 4.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # 2. With Devil's Advocate (5-Agent Configuration)
    ax2.set_title('With Devil\'s Advocate (5-Agent Configuration)', fontweight='bold')
    agents_5 = ['researcher', 'critic', 'devils_advocate', 'synthesizer', 'judge']
    positions_5 = [(1, 3), (2.5, 3), (4, 3), (5.5, 3), (7, 3)]
    
    # Draw agents
    for i, (agent, pos) in enumerate(zip(agents_5, positions_5)):
        ax2.add_patch(patches.Circle(pos, 0.4, color=agent_colors[agent], alpha=0.7))
        ax2.text(pos[0], pos[1], agent.replace('_', ' ').title(), ha='center', va='center', 
                fontsize=9, fontweight='bold', color='white')
    
    # Draw message flow
    for i in range(len(positions_5) - 1):
        ax2.arrow(positions_5[i][0] + 0.4, positions_5[i][1], 
                positions_5[i+1][0] - positions_5[i][0] - 0.8, 0,
                head_width=0.15, head_length=0.15, fc='black', ec='black')
    
    # Add start and end
    ax2.add_patch(patches.Circle((0, 3), 0.3, color='gray', alpha=0.7))
    ax2.text(0, 3, 'START', ha='center', va='center', fontsize=8, fontweight='bold')
    ax2.add_patch(patches.Circle((8, 3), 0.3, color='gray', alpha=0.7))
    ax2.text(8, 3, 'END', ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax2.arrow(0.3, 3, 0.4, 0, head_width=0.15, head_length=0.15, fc='black', ec='black')
    ax2.arrow(7.4, 3, 0.4, 0, head_width=0.15, head_length=0.15, fc='black', ec='black')
    
    ax2.set_xlim(-0.5, 8.5)
    ax2.set_ylim(1.5, 4.5)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # 3. Multi-Round Flow
    ax3.set_title('Multi-Round Flow', fontweight='bold')
    
    # Draw round structure
    round_y = 3
    for round_num in range(1, 4):  # Show 3 rounds as example
        round_x = round_num * 2.5
        
        # Draw round box
        rect = patches.Rectangle((round_x - 1, round_y - 1.5), 2, 3, 
                            linewidth=1, edgecolor='black', facecolor='none')
        ax3.add_patch(rect)
        ax3.text(round_x, round_y + 1.7, f'Round {round_num}', 
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw agents in round
        agent_positions = [(round_x - 0.7, round_y), (round_x, round_y), 
                        (round_x + 0.7, round_y)]
        agent_labels = ['R', 'C', 'S']  # Simplified labels
        
        for pos, label in zip(agent_positions, agent_labels):
            ax3.add_patch(patches.Circle(pos, 0.2, color='skyblue', alpha=0.7))
            ax3.text(pos[0], pos[1], label, ha='center', va='center', 
                    fontsize=8, fontweight='bold')
        
        # Draw flow within round
        ax3.arrow(round_x - 0.5, round_y, 0.4, 0, 
                head_width=0.1, head_length=0.1, fc='black', ec='black')
        ax3.arrow(round_x + 0.2, round_y, 0.4, 0, 
                head_width=0.1, head_length=0.1, fc='black', ec='black')
        
        # Draw flow to next round
        if round_num < 3:
            ax3.arrow(round_x + 0.9, round_y - 0.5, 0, -0.7, 
                    head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    # Add judge at the end
    ax3.add_patch(patches.Circle((8.5, round_y), 0.3, color='purple', alpha=0.7))
    ax3.text(8.5, round_y, 'J', ha='center', va='center', 
            fontsize=8, fontweight='bold', color='white')
    ax3.arrow(7.2, round_y, 0.9, 0, 
            head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    ax3.text(8.5, round_y - 0.7, 'Judge', ha='center', va='center', 
            fontsize=8, fontweight='bold')
    
    ax3.set_xlim(-0.5, 9.5)
    ax3.set_ylim(0.5, 4.5)
    ax3.axis('off')
    
    # 4. Feedback Mechanisms
    ax4.set_title('Feedback Mechanisms', fontweight='bold')
    
    # Draw feedback loop diagram
    center_x, center_y = 4, 3
    
    # Draw central message history
    ax4.add_patch(patches.Rectangle((center_x - 1.5, center_y - 1), 3, 2, 
                                linewidth=1, edgecolor='black', 
                                facecolor='lightgray', alpha=0.3))
    ax4.text(center_x, center_y + 0.5, 'Message\nHistory', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw agents around the history
    agent_positions = [
        (center_x - 2.5, center_y),      # Researcher
        (center_x - 2.5, center_y - 1.5),  # Critic
        (center_x + 2.5, center_y - 1.5),  # Devil's Advocate
        (center_x + 2.5, center_y),       # Synthesizer
        (center_x, center_y - 2.5)        # Judge
    ]
    
    agent_names = ['Researcher', 'Critic', "Devil's\nAdvocate", 'Synthesizer', 'Judge']
    agent_colors_list = ['blue', 'red', 'orange', 'green', 'purple']
    
    for pos, name, color in zip(agent_positions, agent_names, agent_colors_list):
        ax4.add_patch(patches.Circle(pos, 0.3, color=color, alpha=0.7))
        ax4.text(pos[0], pos[1], name, ha='center', va='center', 
                fontsize=8, fontweight='bold')
        
        # Draw arrows to/from message history
        if name != 'Judge':
            ax4.annotate('', xy=(center_x - 1.3, center_y - 0.3), xytext=pos,
                        arrowprops=dict(arrowstyle='->', lw=1, color='black'))
        else:
            ax4.annotate('', xy=pos, xytext=(center_x, center_y - 0.8),
                        arrowprops=dict(arrowstyle='->', lw=1, color='black'))
    
    # Add legend
    ax4.text(0.5, 0.5, 'Each agent accesses\ncomplete message\nhistory for context', 
            ha='center', va='center', fontsize=9, style='italic')
    
    ax4.set_xlim(-3.5, 6)
    ax4.set_ylim(-3.5, 4.5)
    ax4.axis('off')
    
    # Adjust layout and save
    plt.tight_layout()
    
    # Create output directory
    output_dir = Path("Deliverables/graphs")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Save visualization
    output_path = output_dir / "complete_flow_visualization.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return str(output_path)

if __name__ == "__main__":
    print("Creating complete flow visualization...")
    path = create_complete_flow_visualization()
    print(f"Visualization saved to: {path}")
