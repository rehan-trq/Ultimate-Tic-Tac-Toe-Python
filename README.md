
# Ultimate Tic-Tac-Toe 

A sophisticated implementation of Ultimate Tic-Tac-Toe featuring multiple AI difficulty levels powered by Constraint Satisfaction Problem (CSP) algorithms, Minimax with Alpha-Beta pruning, and advanced heuristics.

## Game Overview

Ultimate Tic-Tac-Toe is a strategic variant of the classic game played on a 3×3 grid of 3×3 boards. Your move determines which board your opponent must play in next, creating deep strategic gameplay that requires both tactical and strategic thinking.

### Key Features

- **Advanced AI System**: Three difficulty levels with different algorithms
  - **Easy**: Random move selection
  - **Medium**: Strategic play with win/block detection
  - **Hard**: CSP-based AI with Minimax, Alpha-Beta pruning, and constraint propagation
- **Multiple Game Modes**: Human vs Human, Human vs AI, AI vs AI
- **Modern UI**: Dark theme with visual feedback and board highlighting
- **Game Logging**: Comprehensive move tracking and game state logging
- **Real-time Gameplay**: Smooth animations and responsive controls

## AI Architecture

### CSP (Constraint Satisfaction Problem) Implementation

The advanced AI uses CSP techniques to make optimal moves:

- **Variables**: Empty cells in active small boards
- **Domains**: Valid player symbols ('X' or 'O')
- **Constraints**: Game rules (valid moves, board states, win conditions)

### Advanced Algorithms

1. **Minimax with Alpha-Beta Pruning**
   - Depth-limited search (3 levels for optimal performance)
   - Alpha-beta pruning for efficiency
   - Position evaluation heuristics

2. **Constraint Propagation**
   - **Forward Checking**: Eliminates inconsistent future moves
   - **Arc Consistency (AC-3)**: Maintains constraint consistency
   - **MRV Heuristic**: Minimum Remaining Values for variable ordering

3. **Strategic Heuristics**
   - Center position preference
   - Corner strategy implementation
   - Board constraint analysis
   - Win/block pattern recognition

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/rehan-trq/Ultimate-Tic-Tac-Toe-Pythoni.git
cd Ultimate-Tic-Tac-Toe-Python

# Run the game
python Code.py
```

### Alternative Installation

```bash
# If you prefer to download directly
wget https://raw.githubusercontent.com/rehan-trq/Ultimate-Tic-Tac-Toe-Python/main/Cide.py
python Code.py
```
