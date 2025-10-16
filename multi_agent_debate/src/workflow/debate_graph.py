"""LangGraph workflow for the multi-agent debate system."""

from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agents import Researcher, Critic, Synthesizer, Judge, DevilsAdvocate
from src.utils.config import config

class DebateState(TypedDict):
    """State for the debate workflow."""
    topic: str
    messages: Annotated[List[Dict[str, Any]], lambda x, y: x + y]
    current_round: int
    total_rounds: int
    current_agent: str
    agent_sequence: List[str]
    verdict: Dict[str, Any]
    ratings: Dict[str, int]
    convergence: bool
    experiment_config: Dict[str, Any]

def create_debate_graph(
    agent_types: List[str] = None,
    rounds: int = 2,
    temperature: float = None,
    include_devils_advocate: bool = False
) -> StateGraph:
    """Create a debate graph with specified agents and configuration."""
    
    # Default agent sequence
    if agent_types is None:
        agent_types = ["researcher", "critic", "synthesizer", "judge"]
    
    # Add devil's advocate if requested
    if include_devils_advocate and "devils_advocate" not in agent_types:
        # Insert before synthesizer
        if "synthesizer" in agent_types:
            idx = agent_types.index("synthesizer")
            agent_types.insert(idx, "devils_advocate")
        else:
            agent_types.append("devils_advocate")
    
    # Initialize agents
    agents = {}
    if "researcher" in agent_types:
        agents["researcher"] = Researcher(temperature)
    if "critic" in agent_types:
        agents["critic"] = Critic(temperature)
    if "synthesizer" in agent_types:
        agents["synthesizer"] = Synthesizer(temperature)
    if "judge" in agent_types:
        agents["judge"] = Judge(temperature)
    if "devils_advocate" in agent_types:
        agents["devils_advocate"] = DevilsAdvocate(temperature)
    
    # Create the graph
    workflow = StateGraph(DebateState)
    
    # Define the nodes
    def researcher_node(state: DebateState) -> DebateState:
        """Process the researcher's turn."""
        agent = agents["researcher"]
        context = {"previous_messages": state["messages"]}
        response = agent.process_input(state["topic"], context)
        
        new_message = {
            "role": "researcher",
            "content": response,
            "round": state["current_round"]
        }
        
        return {
            **state,
            "messages": state["messages"] + [new_message],
            "current_agent": "critic" if "critic" in agent_types else next_agent(agent_types, "researcher")
        }
    
    def critic_node(state: DebateState) -> DebateState:
        """Process the critic's turn."""
        agent = agents["critic"]
        last_message = state["messages"][-1]["content"] if state["messages"] else ""
        context = {"previous_messages": state["messages"]}
        response = agent.process_input(last_message, context)
        
        new_message = {
            "role": "critic",
            "content": response,
            "round": state["current_round"]
        }
        
        return {
            **state,
            "messages": state["messages"] + [new_message],
            "current_agent": next_agent(agent_types, "critic")
        }
    
    def synthesizer_node(state: DebateState) -> DebateState:
        """Process the synthesizer's turn."""
        agent = agents["synthesizer"]
        last_message = state["messages"][-1]["content"] if state["messages"] else ""
        context = {"previous_messages": state["messages"]}
        response = agent.process_input(last_message, context)
        
        new_message = {
            "role": "synthesizer",
            "content": response,
            "round": state["current_round"]
        }
        
        return {
            **state,
            "messages": state["messages"] + [new_message],
            "current_agent": next_agent(agent_types, "synthesizer")
        }
    
    def devils_advocate_node(state: DebateState) -> DebateState:
        """Process the devil's advocate's turn."""
        agent = agents["devils_advocate"]
        last_message = state["messages"][-1]["content"] if state["messages"] else ""
        context = {"previous_messages": state["messages"]}
        response = agent.process_input(last_message, context)
        
        new_message = {
            "role": "devils_advocate",
            "content": response,
            "round": state["current_round"]
        }
        
        return {
            **state,
            "messages": state["messages"] + [new_message],
            "current_agent": next_agent(agent_types, "devils_advocate")
        }
    
    def judge_node(state: DebateState) -> DebateState:
        """Process the judge's final evaluation."""
        agent = agents["judge"]
        last_message = state["messages"][-1]["content"] if state["messages"] else ""
        context = {"previous_messages": state["messages"]}
        response = agent.process_input(last_message, context)
        
        new_message = {
            "role": "judge",
            "content": response,
            "round": state["current_round"]
        }
        
        # Extract ratings from the verdict
        ratings = agent.extract_ratings(response)
        
        # Determine convergence (simple heuristic)
        convergence = "consensus" in response.lower() or "agreement" in response.lower()
        
        return {
            **state,
            "messages": state["messages"] + [new_message],
            "verdict": {"content": response, "final": True},
            "ratings": ratings,
            "convergence": convergence,
            "current_agent": END
        }
    
    def check_round_completion(state: DebateState) -> str:
        """Check if the current round is complete and determine next action."""
        current = state["current_agent"]
        
        # If we've reached the judge, end the debate
        if current == "judge" or current == END:
            return "judge"
        
        # If we've completed all agents in this round, move to next round or end
        if state["current_round"] >= state["total_rounds"]:
            # Check if judge is in the sequence
            if "judge" in agent_types:
                return "judge"
            else:
                return END
        
        # Continue with the current agent
        return current
    
    def next_agent(agent_sequence: List[str], current: str) -> str:
        """Get the next agent in the sequence."""
        try:
            idx = agent_sequence.index(current)
            if idx + 1 < len(agent_sequence):
                return agent_sequence[idx + 1]
            else:
                # End of sequence, move to next round or judge
                if "judge" in agent_sequence:
                    return "judge"
                else:
                    return END
        except ValueError:
            return END
    
    # Add nodes to the graph
    if "researcher" in agent_types:
        workflow.add_node("researcher", researcher_node)
    if "critic" in agent_types:
        workflow.add_node("critic", critic_node)
    if "synthesizer" in agent_types:
        workflow.add_node("synthesizer", synthesizer_node)
    if "devils_advocate" in agent_types:
        workflow.add_node("devils_advocate", devils_advocate_node)
    if "judge" in agent_types:
        workflow.add_node("judge", judge_node)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "researcher",
        check_round_completion,
        {
            "critic": "critic",
            "synthesizer": "synthesizer",
            "devils_advocate": "devils_advocate",
            "judge": "judge",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "critic",
        check_round_completion,
        {
            "synthesizer": "synthesizer",
            "devils_advocate": "devils_advocate",
            "judge": "judge",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "synthesizer",
        check_round_completion,
        {
            "devils_advocate": "devils_advocate",
            "judge": "judge",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "devils_advocate",
        check_round_completion,
        {
            "judge": "judge",
            END: END
        }
    )
    
    workflow.add_edge("judge", END)
    
    # Set entry point
    workflow.set_entry_point(agent_types[0] if agent_types else "researcher")
    
    # Add memory for conversation history
    memory = MemorySaver()
    
    # Compile the graph
    app = workflow.compile(checkpointer=memory)
    
    return app

def initialize_debate_state(
    topic: str,
    rounds: int = 2,
    agent_types: List[str] = None,
    temperature: float = None,
    include_devils_advocate: bool = False
) -> DebateState:
    """Initialize the debate state with configuration."""
    if agent_types is None:
        agent_types = ["researcher", "critic", "synthesizer", "judge"]
    
    # Add devil's advocate if requested
    if include_devils_advocate and "devils_advocate" not in agent_types:
        if "synthesizer" in agent_types:
            idx = agent_types.index("synthesizer")
            agent_types.insert(idx, "devils_advocate")
        else:
            agent_types.append("devils_advocate")
    
    return {
        "topic": topic,
        "messages": [],
        "current_round": 1,
        "total_rounds": rounds,
        "current_agent": agent_types[0] if agent_types else "researcher",
        "agent_sequence": agent_types,
        "verdict": {},
        "ratings": {"evidence": 0, "feasibility": 0, "risks": 0, "clarity": 0},
        "convergence": False,
        "experiment_config": {
            "rounds": rounds,
            "agents": len(agent_types),
            "temperature": temperature or config.default_temperature,
            "include_devils_advocate": include_devils_advocate
        }
    }
