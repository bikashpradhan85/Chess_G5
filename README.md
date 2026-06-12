# ♟️ Chess_G5 - AI Chess Engine

## Overview

Chess_G5 is a complete AI-powered Chess Engine developed using Python and Pygame. The project implements all standard chess rules, graphical gameplay, intelligent AI opponent, chess timers, and board evaluation visualization.

The AI uses Minimax Search with Negamax implementation, Alpha-Beta Pruning, Move Ordering, and Evaluation Functions to select the strongest move.

This project demonstrates concepts from:

* Artificial Intelligence
* Game Theory
* Data Structures
* Search Algorithms
* Object-Oriented Programming
* Game Development

---

# Features

## Chess Features

* Complete 8×8 Chess Board
* Legal Move Generation
* Check Detection
* Checkmate Detection
* Stalemate Detection
* Turn Management

## Special Chess Rules

* Castling
* En Passant
* Pawn Promotion

  * Queen
  * Rook
  * Bishop
  * Knight

## AI Features

* Minimax Algorithm
* Negamax Search
* Alpha-Beta Pruning
* Move Ordering
* Transposition Table
* Position Evaluation Function

## User Interface Features

* Graphical Chess Board
* Piece Highlighting
* Legal Move Highlighting
* Evaluation Bar
* Chess Clock
* Game Over Screen

---

# Technologies Used

| Technology  | Purpose              |
| ----------- | -------------------- |
| Python      | Programming Language |
| Pygame      | GUI Framework        |
| Time Module | Chess Clock          |
| Copy Module | Board Simulation     |
| OOP         | Project Structure    |

---

# Prerequisites

Before running the project, Python must be installed on your system.

## Install Python

Download Python from:

https://www.python.org/downloads/

During installation enable:

```text
✓ Add Python to PATH
```

Verify installation:

```bash
python --version
```

Expected Output:

```bash
Python 3.x.x
```

# Clone Repository

```bash
git clone https://github.com/bikashpradhan85/Chess_G5.git
cd Chess_G5
```

---

# Create Virtual Environment

Creating a virtual environment keeps project dependencies isolated.

## Windows

```bash
python -m venv venv
```

## Linux / macOS

```bash
python3 -m venv venv
```

---

# Activate Virtual Environment

## Windows CMD

```bash
venv\Scripts\activate
```

## Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

## Linux / macOS

```bash
source venv/bin/activate
```

After activation:

```bash
(venv)
```

will appear at the beginning of the terminal.

---

Then
cd project_chess 
run above command to enter in project_chess folder.
it will show something like this : (venv) C:\Users\Administrator\Documents\GitHub\Chess_G5\project_chess>
Then continue following instructions below.

# Upgrade Pip

```bash
python -m pip install --upgrade pip
```

---

# Install Dependencies

## Using requirements.txt

```bash
pip install -r requirements.txt
```

## Manual Installation

```bash
pip install pygame
```

---


---

# Run Project

```bash
python main.py
```

The Chess application window will launch.

---

# Project Structure

```text
Chess_G5/

├── assets/
│
│   ├── wK.png
│   ├── wQ.png
│   ├── wR.png
│   ├── wB.png
│   ├── wN.png
│   ├── wP.png
│
│   ├── bK.png
│   ├── bQ.png
│   ├── bR.png
│   ├── bB.png
│   ├── bN.png
│   └── bP.png
│
├── main.py
├── board.py
├── pieces.py
├── ai.py
├── evaluation.py
├── timer.py
├── settings.py
├── requirements.txt
└── README.md
```

---

# Project Workflow

```text
Start Game
      ↓
Initialize Board
      ↓
Load Piece Images
      ↓
Create Chess Clock
      ↓
Display Chess Board
      ↓
Player Selects Piece
      ↓
Generate Legal Moves
      ↓
Validate Move
      ↓
Execute Move
      ↓
Check / Checkmate Detection
      ↓
AI Turn Starts
      ↓
Generate AI Legal Moves
      ↓
Move Ordering
      ↓
Negamax Search
      ↓
Alpha-Beta Pruning
      ↓
Evaluation Function
      ↓
Choose Best Move
      ↓
Execute AI Move
      ↓
Update Board
      ↓
Update Evaluation Bar
      ↓
Update Timers
      ↓
Repeat
      ↓
Game Over
```

---

# AI Algorithms Used

## 1. Minimax Algorithm

The Minimax algorithm is the core decision-making algorithm used by the AI.

Assumptions:

* AI always plays the best move.
* Opponent always plays the best move.

The algorithm explores future positions and selects the move with the highest guaranteed outcome.

---

## 2. Negamax Algorithm

Negamax is a simplified implementation of Minimax.

Formula:

```python
score = -negamax(child)
```

Benefits:

* Cleaner implementation
* Less code
* Same result as Minimax

---

## 3. Alpha-Beta Pruning

Alpha-Beta Pruning improves Minimax performance.

Branches that cannot affect the final decision are skipped.

Condition:

```text
alpha >= beta
```

Benefits:

* Faster search
* Reduced computation
* Same optimal result

---

## 4. Move Ordering

Moves are sorted before searching.

Priority:

```text
Checkmate
Captures
Promotions
Checks
Normal Moves
```

Benefits:

* Improves Alpha-Beta efficiency
* Reduces search time

---

## 5. Evaluation Function

The evaluation function estimates the strength of a board position.

### Piece Values

```text
Pawn   = 100
Knight = 320
Bishop = 330
Rook   = 500
Queen  = 900
King   = 20000
```

### Evaluation Formula

```text
Material Score
+
Positional Score
```

Factors:

* Material Advantage
* Center Control
* Piece Activity
* King Safety
* Pawn Structure

---

## 6. Transposition Table

Previously analyzed positions are stored.

Benefits:

* Faster search
* Avoids repeated calculations
* Improves AI efficiency

---

# Chess Rules Implemented

## Normal Movement

* Pawn
* Knight
* Bishop
* Rook
* Queen
* King

## Special Moves

### Castling

Both kingside and queenside castling are supported.

### En Passant

Special pawn capture rule implemented.

### Pawn Promotion

Promotion choices:

* Queen
* Rook
* Bishop
* Knight

---

# Evaluation Bar

The engine displays an evaluation bar showing the current position score.

Examples:

```text
+3.5
```

White advantage

```text
-2.0
```

Black advantage

---

# Timer System

The project includes a chess clock.

Features:

* White Timer
* Black Timer
* Automatic Turn Switching
* Timeout Detection

If a player's timer reaches zero:

```text
Time Out
```

Opponent wins.

---

# Learning Outcomes

This project demonstrates:

* Artificial Intelligence
* Minimax Search
* Alpha-Beta Pruning
* Heuristic Evaluation
* Data Structures
* Object-Oriented Programming
* Event-Driven Programming
* Game Development

---

# Future Improvements

* Difficulty Levels
* Online Multiplayer
* Move History Panel
* PGN Export
* Opening Book Database
* Stronger AI Search Depth
* Endgame Tablebases

---



# Authors

Chess_G5 Development Team(Team 5 TMSL)

---

# License

This project is developed for educational and academic purposes only.
