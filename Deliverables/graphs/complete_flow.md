# Multi-Agent Debate System: Complete Flow

## Overview
The multi-agent debate system uses LangGraph to orchestrate conversations between different AI agents with specialized roles. The system supports multiple configurations with different agent combinations and debate rounds.

## Agent Roles

### 1. Researcher
- **Purpose**: Gathers and presents factual information relevant to the debate topic
- **Input**: Debate topic
- **Output**: Evidence-based information and data
- **Position in Flow**: Always starts the debate

### 2. Critic
- **Purpose**: Evaluates arguments, identifies logical fallacies, and points out weaknesses
- **Input**: Previous agent's message
- **Output**: Critical evaluation of arguments
- **Position in Flow**: Second in sequence (if included)

### 3. Devil's Advocate (Optional)
- **Purpose**: Challenges prevailing opinions and assumptions
- **Input**: Previous agent's message
- **Output**: Counterarguments and challenges
- **Position in Flow**: Inserted before Synthesizer (if included)

### 4. Synthesizer
- **Purpose**: Integrates different perspectives and finds common ground
- **Input**: Previous agent's message
- **Output**: Balanced synthesis of arguments
- **Position in Flow**: Before Judge (if included)

### 5. Judge
- **Purpose**: Evaluates the overall debate and provides final verdict
- **Input**: Previous agent's message
- **Output**: Final verdict with ratings
- **Position in Flow**: Always ends the debate

## Debate Flow

### Standard 4-Agent Configuration
```
START → Researcher → Critic → Synthesizer → Judge → END
```

### With Devil's Advocate (5-Agent Configuration)
```
START → Researcher → Critic → Devil's Advocate → Synthesizer → Judge → END
```

### Minimal 2-Agent Configuration
```
START → Researcher → Judge → END
```

## Multi-Round Flow

For debates with multiple rounds, the flow continues in cycles:

1. **Round 1**: Researcher → Critic → [Devil's Advocate] → Synthesizer
2. **Round 2**: Researcher → Critic → [Devil's Advocate] → Synthesizer
3. **Final Round**: Judge provides verdict

After each complete cycle through all agents (except Judge), the system checks if the maximum number of rounds has been reached:
- If more rounds are needed: Continue to next round with Researcher
- If max rounds reached: Move to Judge for final verdict

## Feedback Mechanisms

### Message History
Each agent has access to the complete message history from previous rounds, allowing them to:
- Reference earlier arguments
- Build upon previous points
- Identify contradictions or evolution in arguments

### Context Passing
When an agent processes input, they receive:
- The immediate previous message
- Full message history from all previous rounds
- Current round number
- Total number of rounds

### Conditional Routing
The system uses conditional routing to determine the next agent based on:
- Current agent in the sequence
- Number of rounds completed
- Whether the judge has been reached

## State Management

The debate system maintains state throughout the conversation:
- **Topic**: The debate topic
- **Messages**: Complete history of all agent messages
- **Current Round**: Tracks which round is active
- **Current Agent**: Tracks which agent is currently speaking
- **Agent Sequence**: The ordered list of agents in the debate
- **Verdict**: The judge's final evaluation
- **Ratings**: Numerical scores for different aspects
- **Convergence**: Whether consensus was reached

## Example Flow with Feedback

Consider a debate on "Should artificial intelligence be regulated?":

1. **Researcher (Round 1)**: Presents factual information about AI regulation, existing laws, and potential impacts
2. **Critic (Round 1)**: Evaluates the researcher's evidence, points out potential biases or gaps
3. **Devil's Advocate (Round 1)**: Challenges the premise that regulation is necessary, highlights potential negative consequences
4. **Synthesizer (Round 1)**: Integrates the different perspectives, identifies areas of agreement and disagreement
5. **Researcher (Round 2)**: Responds to criticisms, provides additional evidence, addresses challenges
6. **Critic (Round 2)**: Evaluates the new evidence and responses
7. **Devil's Advocate (Round 2)**: Continues to challenge assumptions and highlight risks
8. **Synthesizer (Round 2)**: Attempts to find common ground and balanced solutions
9. **Judge**: Provides final verdict with ratings on evidence, feasibility, risks, and clarity

This structured flow ensures comprehensive exploration of the topic from multiple perspectives, with each agent building upon or responding to previous contributions.
