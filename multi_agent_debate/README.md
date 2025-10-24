# Multi-Agent Debate System

A system for running structured debates between AI agents using GLM-4.6 and LangGraph.

## Overview

This project implements a multi-agent debate system where AI agents with distinct roles engage in structured discussions on various topics. The system supports configurable debate parameters and provides comprehensive evaluation metrics.

## Features

- **Multiple Agent Types**: Researcher, Critic, Synthesizer, Judge, and Devil's Advocate
- **Configurable Debates**: Adjustable number of rounds, agents, and temperature settings
- **LangGraph Integration**: Uses LangGraph for workflow management
- **GLM-4.6 Support**: Compatible with GLM-4.6 model via Z.AI API
- **Evaluation Metrics**: Comprehensive rubric for assessing debate quality
- **Experiment Framework**: Built-in support for running comparative experiments

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd multi_agent_debate
```

2. Create and activate a virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies directly from requirements.txt:
```bash
uv pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env_example .env
# Edit .env with your Z.AI API key
```

5. If you encounter import errors with langchain, reinstall dependencies:
```bash
uv pip install -r requirements.txt --force-reinstall
```

Note: During execution, you may encounter content filter errors from the API (Error code: 400 - 'System detected potentially unsafe or sensitive content'). This is a safety feature of the GLM-4.6 model and may occur with certain debate topics. If this happens, try with a different topic or rephrase the current topic to be less sensitive.
## Usage

### Running a Debate

```bash
uv run main.py --topic "Should artificial intelligence be regulated?"
```

### Running Experiments

```bash
uv run -c "from src.experiments import ExperimentRunner; runner = ExperimentRunner(); results = runner.run_standard_experiments('Your debate topic here')"
```

### Running Tests

```bash
uv run run_tests.py
```

### Generating Deliverables

```bash
uv run generate_deliverables.py
```

## Project Structure

```
multi_agent_debate/
├── src/
│   ├── agents/          # Agent implementations
│   ├── evaluation/      # Evaluation metrics and rubrics
│   ├── experiments/     # Experiment management
│   ├── utils/           # Utility functions
│   └── workflow/        # LangGraph workflow definitions
├── testing/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── experiments/
│   ├── results/         # Experiment results
│   └── logs/            # Experiment logs
├── Deliverables/        # Generated deliverables
└── docs/               # Documentation
```

## Configuration

The system can be configured through environment variables in the `.env` file:

- `ZAI_API_KEY`: Your Z.AI API key (required)
- `GLM_MODEL`: Model name (default: glm-4.6)
- `GLM_BASE_URL`: API base URL (default: https://api.z.ai/api/coding/paas/v4/)
- `DEFAULT_TEMPERATURE`: Default temperature (default: 0.7)
- `LOW_TEMPERATURE`: Low temperature setting (default: 0.2)
- `HIGH_TEMPERATURE`: High temperature setting (default: 0.9)
- `DEFAULT_ROUNDS`: Default number of rounds (default: 2)
- `DEFAULT_AGENTS`: Default number of agents (default: 4)
- `MAX_TOKENS`: Maximum tokens per response (default: 1000)

## Agent Roles

### Researcher
Gathers and presents factual information relevant to the debate topic, providing evidence and data.

### Critic
Evaluates arguments, identifies logical fallacies, and points out weaknesses in reasoning.

### Synthesizer
Integrates different perspectives, finds common ground, and proposes balanced solutions.

### Judge
Evaluates the overall debate, provides a final verdict, and rates the debate on key dimensions.

### Devil's Advocate (Optional)
Challenges prevailing opinions and assumptions to ensure all perspectives are considered.

## Evaluation Metrics

The system evaluates debates based on four key dimensions:

1. **Evidence** (0-5): Quality and sufficiency of evidence provided
2. **Feasibility** (0-5): Practicality and implementability of proposals
3. **Risks** (0-5): Identification and assessment of potential risks
4. **Clarity** (0-5): Clarity and coherence of arguments

## Experiment Toggles

The system supports the following experiment toggles:

1. **Number of Agents**: 2 vs 4 agents
2. **Number of Rounds**: 1 vs 3 rounds
3. **Devil's Advocate**: With vs without Devil's Advocate
4. **Temperature**: Low vs high temperature settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.