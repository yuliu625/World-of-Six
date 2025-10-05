# World of Six: Exploring Machine Optimism in Multi-Agent Systems
This is the official code repository for the paper "Beyond Rationality: Network Effects, History, and Machine Optimism in Multi-Agents" (SWAIB 2025). This research delves into the behavior, strategies, and biases of large language model (LLM) based agents in complex multi-agent game environments with network effects.

## Abstract
This study aims to investigate the decision-making behavior of LLM-based agents in complex dynamic game environments. We constructed a simulation experiment, placing agents in a dynamic game scenario with network effects, and systematically analyzed their decision-making processes. Our core findings reveal that these agents are not entirely rational but exhibit observable systematic biases. Specifically, we observed the following four key behavioral patterns:

- **Irrational Expectations and Bias**: The decisions of LLM agents are not fully rational and show observable systematic biases.
- **Mean Reversion**: In the absence of historical information, agents tend to choose the average value, suggesting their decision-making process may be influenced by prior biases or default behaviors.
- **Historical Trends**: Agents are capable of effectively using historical information to dynamically adjust their decisions, demonstrating a degree of learning and adaptability.
- **Optimistic Tendency**: Agents tend to exhibit optimism, which may lead to a decrease in their utility in certain situations. We speculate that this bias may be related to the RLHF (Reinforcement Learning from Human Feedback) training process of LLMs.

By simulating a complex game, this study provides a new perspective for understanding and evaluating the behavior of LLM agents in quasi-real-world environments and lays the groundwork for building more reliable and predictable agents in more complex, non-zero-sum games in the future.


## Project Overview

### Research Motivation and Challenges
Existing game theory research, whether in economics or artificial intelligence, faces limitations. Economic research often relies on highly simplified theoretical models or costly human experiments, while the AI field often focuses on simple zero-sum games. Both methods fail to fully explore the complex, dynamic, recursive, and non-linear interactions of network effects.

A network effect is a typical real-world phenomenon where the value of a good or service depends on the size of its user base. This interdependence makes game strategies, pricing, and equilibrium analysis exceptionally complex. This research aims to fill this gap by building a simulation environment to analyze the decision-making behavior of LLM agents under network effects.

### Core Research Questions
We designed a simulation experiment that places LLM agents in a dynamic game scenario and analyzes their decision-making process. Our research aims to answer two core questions:

- Do LLM agents behave similarly to humans in complex, quasi-real-world dynamic games? Are their decisions better?
- How are the behavioral mechanisms and irrational biases of machines formed in multi-agent interactions?

### Experimental Design and Methodology
We assume a "World of Six," where each of the six agents must independently decide whether to attend a conference. The utility function for each agent $U_j(\theta_j)$ is defined as follows:

$$U_j(\theta_j) = \theta_j + \beta \times N - p_j$$

Where:
- $U_j$ is the utility of agent $j$.
- $\theta_j$ is the independent utility for each agent $j$.
- $\beta$ is the network utility strength.
- $N$ is the actual number of participants in the network.
- $p_j$ is the price of the network good.

By setting different network effect strengths ($\beta$), independent values ($\theta_j$), and price sequences ($p_j$), we can systematically analyze and record the decision-making behavior of each agent to reveal their underlying behavioral patterns.


## Project Structure and Technology Stack
```bash
.
├── game/                    # Core game logic, agents, and runtime environment
│   ├── agents/              # Agent definitions (participant, manager)
│   ├── configs/             # Agent attributes and price sequence configurations
│   ├── prompts/             # Agent prompt templates
│   ├── protocols/           # Inter-agent communication protocols (schema)
│   ├── runtime/             # Multi-agent system runtime logic
│   ├── tools/               # Tools defined for the Manager (e.g., utility_calculator)
│   └── utils/               # Helper utilities
├── experiments/             # Scripts and configurations for running the paper's experiments
├── visualization/           # Data visualization analysis scripts
└── README.md                # This file
```

### Key Module Descriptions
- `game/`: Contains all core code related to the game simulation. The `participant` agent in the `agents/` folder is designed as a general-purpose game agent, which is easy to port to other game scenarios. The `manager` is a programmatically controlled agent specifically designed for this experiment to manage the game flow and rules.
- `experiments/`: The scripts and configurations in this directory are used to run the specific experiments described in the paper. Each experiment script is carefully designed to ensure the reproducibility of the results.
- `visualization/`: Contains the code used to generate all the charts in the paper, including behavioral pattern analysis charts, utility curves, and more. This section of the code helps users understand the experimental results.


## Reproducing the Experiments
### 1. Model Configuration
Register your LLM model in `model_client.py`, such as OpenAI or other providers.

### 2. Parameter Settings
In `run_a_game.py` or `run_an_experiment.py`, adjust the parameters as needed. You can refer to the existing configurations in the `experiments` folder as examples.

### 3. Data Analysis and Visualization
After the experiments are completed, use the scripts in the `visualization/` directory to generate the charts from the paper.


## Maintenance Status and Related Work
This repository is an early research project and is shared solely to present the paper's findings. It will **not be maintained** further for the following reasons:
- **Programming Paradigm Evolution**: The project's design relies heavily on object-oriented programming, lacking more modern design patterns. Subsequent work has shifted toward more maintainable functional programming or better design patterns.
- **Technology Stack Iteration**: This was only a preliminary exploration of LLM agent research. I have since conducted more in-depth research and adopted more mature implementation methods based on this work.
- **Subsequent Work**: The research ideas from this paper have been further validated and expanded upon with more advanced methods. The related work is currently under submission, and its code repository will be made public once the paper is accepted.

### Related Research
- [Previous Work](https://github.com/yuliu625/Simulate-the-Prisoners-Dilemma-with-Agents): My earlier attempt using `autogen` to study the behavior of LLM agents in simple games like the Prisoner's Dilemma.
- [Subsequent Work](): The research ideas from this paper have been further validated and expanded upon with more advanced methods. The related work is currently under submission, and its code repository will be made public once the paper is accepted.

### My Other Repositories
- [Agent-Development-Toolkit](https://github.com/yuliu625/Yu-Agent-Development-Toolkit): An agent development toolkit based on `langchain` and `langgraph`, which includes my latest practices on agent architecture and design.
- [Prompt-Collection](https://github.com/yuliu625/Yu-Prompt-Collection): A library of prompts managed using `jinja2` template syntax for efficient management and reuse of various prompt templates.
- [Deep-Learning-Toolkit](https://github.com/yuliu625/Yu-Deep-Learning-Toolkit): A collection of deep learning tools that I have accumulated from my daily tasks.
- [Flash-Boilerplate](https://github.com/yuliu625/Yu-Flash-Boilerplate): A base template repository I built for my deep learning projects.

