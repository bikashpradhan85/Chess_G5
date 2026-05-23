# ♟️ Simplified Chess Engine with AI

A complete chess engine built using Python and Pygame featuring:

- Full 8×8 chess board
- Legal move generation
- Check / Checkmate / Stalemate detection
- Castling
- En Passant
- Pawn Promotion Menu
- AI opponent using Minimax + Alpha-Beta Pruning
- Evaluation Bar
- 10-minute timer for each player
- Real chess piece graphics

---

# 📌 Features

## ✅ Core Features

- 8×8 board representation
- Human vs AI gameplay
- Legal chess move validation
- Piece capturing
- Check detection
- Checkmate detection
- Stalemate detection
- Castling support
- En passant support
- Pawn promotion selection
- Evaluation bar
- Timers for both players

---

# 🧠 AI Features

The AI opponent uses:

- Minimax Algorithm
- Alpha-Beta Pruning
- Move Ordering
- Position Evaluation
- Material Evaluation
- Positional Bonuses

---

# 🖼️ Chess Piece Graphics

This project uses PNG chess piece assets instead of Unicode icons for a professional appearance.

---

# 📂 Project Structure

```text
project_chess/
│
├── assets/
│   ├── wK.png
│   ├── wQ.png
│   ├── wR.png
│   ├── wB.png
│   ├── wN.png
│   ├── wP.png
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
└── README.md

Installation

Python Installation
🔹 Step 1: Download Python

Download Python from:

https://www.python.org/downloads/

🔹 Step 2: Install Python

While installing:

✅ Check the option:

Add Python to PATH

Then click:

Install Now
🔹 Step 3: Verify Installation

Open terminal / command prompt and run:

python --version

Example output:

Python 3.12.5
1️⃣ Clone the Repository
git clone <repository-url>

or download the ZIP file.

2️⃣ Open Project Folder
cd project_chess

Create Virtual Environment
Windows
python -m venv .venv
Linux / Mac
python3 -m venv .venv
Activate Virtual Environment
Windows (PowerShell)
.venv\Scripts\activate
Windows (CMD)
.venv\Scripts\activate.bat
Linux / Mac
source .venv/bin/activate

After activation you will see:

(.venv)
▶️ Running the Game

Run the following command:

python main.py

