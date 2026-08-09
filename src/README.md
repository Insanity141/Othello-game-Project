# Othello AI Game

An AI-based Othello game developed in Python using Pygame for the CSE366 Artificial Intelligence course.

The project demonstrates game-playing AI techniques through three difficulty levels:

- Easy: Random Move Selection
- Medium: Minimax
- Hard: Minimax with Alpha-Beta Pruning

The player first selects the AI difficulty, then chooses Heads or Tails for a coin toss. The toss winner receives the Black pieces and therefore makes the first move.

---

## Features

- Human vs AI Othello gameplay
- 6×6 Othello board
- Difficulty selection menu
- Coin toss system before each match
- Human can choose Heads or Tails
- Toss winner receives Black pieces
- Black always moves first
- Legal move highlighting
- Automatic piece flipping
- Automatic turn passing when no valid move exists
- AI statistics panel
- Final game result screen
- Final piece count
- Play Again option
- Exit option
- Small simulated delay before AI moves so the turn change is visible

---

## AI Difficulty Levels

### Easy

Easy mode uses random move selection.

The AI collects all valid moves and randomly chooses one of them.

**Algorithm:** Random Move Selection

---

### Medium

Medium mode uses the Minimax algorithm with a search depth of 2.

The AI explores possible future game states and selects the move with the best evaluation score.

**Algorithm:** Minimax  
**Search Depth:** 2

---

### Hard

Hard mode uses Minimax with Alpha-Beta Pruning.

Alpha-Beta Pruning avoids exploring branches that cannot affect the final decision, reducing unnecessary search.

**Algorithm:** Minimax + Alpha-Beta Pruning  
**Search Depth:** 4

---

## AI Comparison

| Difficulty | Algorithm             | Search Depth | Pruning |
| ---------- | --------------------- | -----------: | ------- |
| Easy       | Random Move Selection |          N/A | No      |
| Medium     | Minimax               |            2 | No      |
| Hard       | Minimax + Alpha-Beta  |            4 | Yes     |

---

## Board Evaluation

For Medium and Hard modes, the AI evaluates board states using a heuristic evaluation function.

The current evaluation considers:

- Piece difference
- Corner control
- Edge control
- Mobility

The overall evaluation is:

```text
Evaluation Score =
Piece Score
+ Corner Score
+ Edge Score
+ Mobility Score
```

### Piece Difference

The AI compares its number of pieces with the opponent's number of pieces.

A positive value means the board is better for the AI.

### Corner Control

Corners are highly valuable in Othello because a piece placed in a corner cannot be flipped.

Each controlled corner receives a high score.

### Edge Control

Edge pieces receive extra value because they are generally more stable than central pieces.

### Mobility

Mobility measures how many valid moves are available to the AI compared with the opponent.

More available moves generally provide more strategic options.

---

## Minimax

Minimax is an adversarial search algorithm used for two-player games.

The AI assumes that:

- The AI tries to maximize the evaluation score.
- The opponent tries to minimize the evaluation score.

The algorithm recursively explores possible future moves until the configured search depth is reached or the game ends.

---

## Alpha-Beta Pruning

Alpha-Beta Pruning is an optimization of Minimax.

It keeps track of two values:

```text
Alpha = Best score currently available to the maximizing player
Beta  = Best score currently available to the minimizing player
```

A branch can be stopped when:

```text
Beta <= Alpha
```

This means the branch cannot influence the final decision and does not need to be explored further.

---

## AI Statistics

The game displays statistics from the AI's most recent move.

These include:

- Algorithm name
- Nodes searched
- Number of pruning operations
- Evaluation score
- AI execution time in milliseconds

These statistics are useful for comparing Minimax and Alpha-Beta Pruning.

For example:

```text
Algorithm: Minimax + Alpha-Beta
Nodes: 1450
Pruned: 320
Score: +18
Time: 24.31 ms
```

In Medium mode, the pruning count should remain 0 because pure Minimax does not use Alpha-Beta Pruning.

---

## Coin Toss System

After selecting the difficulty, the player enters the coin toss screen.

The human player chooses:

- Heads
- Tails

The program randomly generates the toss result.

The toss winner receives the Black pieces.

Because Black always moves first in Othello, the toss winner also makes the first move.

If the human wins:

```text
Human = Black
AI    = White
```

If the AI wins:

```text
AI    = Black
Human = White
```

The AI system supports both Black and White correctly.

---

## Game Flow

```
Start
  |
  v
Difficulty Selection
  |
  v
Choose Heads or Tails
  |
  v
Coin Toss
  |
  v
Assign Black and White
  |
  v
Black Moves First
  |
  v
Human vs AI Match
  |
  v
Game Over
  |
  v
Final Score
  |
  v
Play Again or Exit
```

---

## Project Structure

```bash
Othello-game-Project
├── README.md
└── src
    ├── ai.py
    ├── ai_stats.py
    ├── board.py
    ├── constants.py
    ├── end_screen.py
    ├── evaluation.py
    ├── main.py
    ├── menu.py
    ├── toss.py
    ├── ui.py
    └── __init__.py
```

---

## File Descriptions

### `main.py`

Controls the overall application flow.

Responsibilities include:

- Starting Pygame
- Running the difficulty menu
- Running the coin toss
- Starting the match
- Managing player turns
- Calling the AI
- Detecting game over
- Opening the end screen
- Restarting or closing the game

### `board.py`

Contains the Othello game rules.

Responsibilities include:

- Creating the board
- Checking board boundaries
- Validating moves
- Finding valid moves
- Finding flippable pieces
- Flipping pieces
- Making moves
- Counting pieces
- Detecting game over
- Determining the winner

### `ai.py`

Contains the AI algorithms.

Implemented algorithms:

- Random Move Selection
- Minimax
- Minimax with Alpha-Beta Pruning

It also selects the correct algorithm based on the chosen difficulty.

### `evaluation.py`

Contains the heuristic board evaluation functions used by Minimax and Alpha-Beta Pruning.

The evaluation considers:

- Piece difference
- Corners
- Edges
- Mobility

### `ai_stats.py`

Stores AI search statistics such as:

- Nodes searched
- Pruning count
- Thinking time
- Evaluation score
- Algorithm name

### `menu.py`

Displays the difficulty selection screen.

Available options:

- Easy
- Medium
- Hard

### `toss.py`

Handles the Heads/Tails selection and coin toss.

The toss determines whether the human or AI receives the Black pieces.

### `ui.py`

Handles the main gameplay interface.

It draws:

- Othello board
- Grid
- Pieces
- Valid move indicators
- Current turn
- Difficulty
- Algorithm
- Piece counts
- AI statistics

### `end_screen.py`

Displays the final game result.

It shows:

- Game Over
- Human win, AI win, or draw
- Winning color
- Final Black piece count
- Final White piece count
- Play Again button
- Exit button

### `constants.py`

Stores shared configuration values such as:

- Board size
- Cell size
- Search depth
- Difficulty constants
- Window size
- Colors
- Piece values
- FPS
- Direction vectors

---

## Technologies Used

- Python
- Pygame

---

## Requirements

- Python 3
- Pygame

Install Pygame using:

```bash
pip install pygame
```

---

## How to Run

Clone the repository:

```bash
git clone <your-repository-url>
```

Open the project folder:

```bash
cd Othello-game-Project
```

Enter the `src` directory:

```bash
cd src
```

Run the game:

```bash
python main.py
```

Depending on the system, this may also work:

```bash
python3 main.py
```

---

## How to Play

1. Start the program.
2. Select Easy, Medium, or Hard difficulty.
3. Click **Start Game**.
4. Choose **Heads** or **Tails**.
5. Click **Toss Coin**.
6. The toss winner receives Black.
7. Black makes the first move.
8. Click one of the highlighted valid positions on the board.
9. The AI automatically makes its move when it is the AI's turn.
10. If a player has no valid move, the turn passes automatically.
11. The game ends when neither player has a valid move.
12. The player with the most pieces wins.
13. Choose **Play Again** or **Exit** from the final screen.

---

## Othello Rules

Othello is played by two players using Black and White pieces.

A move is valid when the newly placed piece surrounds one or more opponent pieces in a straight line.

Valid directions include:

- Up
- Down
- Left
- Right
- Upper-left diagonal
- Upper-right diagonal
- Lower-left diagonal
- Lower-right diagonal

All surrounded opponent pieces are flipped to the current player's color.

If a player has no valid move, that player's turn is skipped.

The game ends when neither player can make a valid move.

The player with the highest number of pieces wins.

---

## Project Objective

The main objective of this project is to demonstrate the application of adversarial search algorithms in a game-playing environment.

The project compares three levels of AI behavior:

```text
Random Move Selection
        |
        v
      Minimax
        |
        v
Minimax + Alpha-Beta Pruning
```

The project also records computational statistics such as nodes searched, pruning count, evaluation score, and execution time.

This makes it possible to analyze both the quality and efficiency of different AI approaches.

---

## Possible Experimental Analysis

The project can be evaluated using metrics such as:

- AI win rate
- Number of nodes searched
- Number of branches pruned
- Execution time
- Final piece difference
- Search depth

Example comparison table:

| Difficulty | Algorithm            | Average Nodes | Average Time | Win Rate |
| ---------- | -------------------- | ------------: | -----------: | -------: |
| Easy       | Random               |             - |            - |        - |
| Medium     | Minimax              |             - |            - |        - |
| Hard       | Minimax + Alpha-Beta |             - |            - |        - |

The actual values can be collected by running multiple games.

---

## Limitations

The current project has several limitations:

- The board is 6×6 instead of the standard 8×8 Othello board.
- Minimax search depth is limited to keep execution time manageable.
- The evaluation function uses a limited number of heuristics.
- Easy difficulty uses random move selection rather than strategic search.
- The game currently supports Human vs AI only.
- There is no online multiplayer.
- There is no persistent game history.

---

## Future Improvements

Possible future improvements include:

- Standard 8×8 board
- Adjustable search depth
- More advanced evaluation heuristics
- Stable-piece evaluation
- Frontier-piece evaluation
- Dynamic evaluation weights
- Iterative deepening
- Transposition tables
- AI vs AI mode
- Move history
- Individual player timers
- Sound effects
- Piece-flipping animation
- Save and load game
- Online multiplayer

---

## Course Information

**Course:** CSE366 - Artificial Intelligence

**Project:** Othello AI Game
