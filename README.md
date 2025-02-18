# Overview

This project was developed as part of the Artificial Intelligence course. It is an AI-driven implementation of the classic Connect Four game. It includes various AI strategies for decision-making, including A* search and Monte Carlo Tree Search (MCTS). The objective is to develop an AI agent capable of making optimal moves while playing against a human or another AI opponent.

# Features

Basic Connect Four gameplay logic
AI integration using:
- A Search Algorithm* for heuristic-based decision-making
- Monte Carlo Tree Search (MCTS) for probabilistic decision-making
- Support for human vs. AI and AI vs. AI gameplay
- Performance analysis of AI agents based on statistical simulations

## Notebook

The ConnectFour.html notebook provides a complete description of the assignment's process, including code, results and analysis.

 
## Other files and folders

Furthermore, we've also included all python classes and files mentioned in the Notebook, as well as the folder Results (which contains csv files with the simulation results that we discussed in the Notebook).

If you would like to test our implementation locally:

- Run the main.py file;
- This initiates the game or simulation, allowing you to play against different AI agents or watch two agents play against each other.

You can also customize the MCTS Agent's behaviour:

Number of Iterations:
- Open the player.py file.
- Locate the MCTSAgent class and modify the iterations parameter to adjust how many times the MCTS algorithm will run.

Exploration Parameter:
- Open the mcts.py file.
- Find and adjust the exploration_constant to your preferred value.

**Statistical Analysis**

If you're interested in analyzing the outcomes of your experiments between different AI agents:
- Open the test.py file for modifications.
- Here, you can implement or modify code to save the results of your simulations to a csv file.

@ Flávio Dantas, Hugo Almeida, Vítor Ferreira | IA PL5 
