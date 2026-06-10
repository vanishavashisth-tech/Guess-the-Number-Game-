# 🎯 Guess the Number

A polished, console-based number-guessing game built with Python 3 and
object-oriented design. Features multiple difficulty levels, proximity
hints, score calculation, and a persistent JSON leaderboard.

---

## Features

| Feature | Details |
|---|---|
| Three difficulty levels | Easy (1–50, 10 attempts), Medium (1–100, 7), Hard (1–200, 5) |
| Proximity hints | "Too high / Too low" + warm/cold distance feedback |
| Visual attempt bar | Colour-coded block bar shows remaining guesses at a glance |
| Score system | Score = 1000 × difficulty multiplier × remaining-attempt ratio |
| Persistent leaderboard | Top 10 scores saved to `data/leaderboard.json` |
| Session statistics | Games played, won, win %, total and best score |
| Player name | Enter a name on start; change it at any time from the menu |
| Input validation | All user input is validated with helpful re-prompt messages |
| No dependencies | Standard library only — runs anywhere Python 3.9+ is installed |

---

## Installation

```bash
# 1. Clone or download this repository
git clone https://github.com/your-username/guess_the_number.git
cd guess_the_number

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. No packages to install — the requirements file is for reference only
```

---

## Usage

```bash
python main.py
```

The game walks you through:

1. **Name input** — enter your display name (max 20 characters).
2. **Main menu** — Play, Leaderboard, Stats, Instructions, Change name, Quit.
3. **Difficulty select** — pick Easy / Medium / Hard.
4. **Guessing loop** — type a number, read the hint, repeat until you win or run out of attempts.
5. **Score saved** — winning rounds are automatically added to the leaderboard.

---

## Scoring

```
score = floor( 1000 × multiplier × (attempts_remaining / max_attempts) )
```

| Difficulty | Multiplier | Perfect score |
|---|---|---|
| Easy | ×1.0 | 1 000 |
| Medium | ×1.5 | 1 500 |
| Hard | ×2.5 | 2 500 |

Guessing correctly on the **first attempt** always returns the maximum score
for that difficulty.

---

## Project Structure

```
guess_the_number/
│
├── main.py          # Entry point, main menu, navigation
├── game.py          # Game logic, difficulty settings, score calculation
├── leaderboard.py   # Persist and display top 10 scores (JSON)
├── utils.py         # Input validation, console colour helpers
│
├── data/
│   └── leaderboard.json   # Auto-created on first run; sample data included
│
├── README.md
└── requirements.txt
```

---

## File Responsibilities

### `main.py`
Entry point. Prints the welcome banner, collects the player name, then
drives the main menu loop — routing between Play, Leaderboard, Stats,
Instructions, and Quit.

### `game.py`
Contains three key constructs:

- `Difficulty` — frozen dataclass holding range, attempts, multiplier, and colour.
- `DIFFICULTIES` — dict mapping `"easy" | "medium" | "hard"` → `Difficulty`.
- `Game` — orchestrates a single round: generates the secret number, runs the
  guessing loop, renders hints and the attempt bar, calculates the final score,
  and returns a `RoundResult`.

### `leaderboard.py`
`Leaderboard` class that loads `data/leaderboard.json` on construction,
exposes `add_score()` and `top_scores()`, and renders a formatted table
(with medal emojis for top 3) via `display()`.

### `utils.py`
Stateless helpers:

- ANSI colour constants (`Color` class).
- `clear_screen()`, `print_header()`, `print_divider()`, `print_centered()`.
- Validated input functions: `get_integer_input()`, `get_string_input()`,
  `get_yes_no()`, `get_menu_choice()`.
- `animate_dots()` — a simple loading animation.

---

## Sample Leaderboard

`data/leaderboard.json` ships with 10 sample entries so the leaderboard
screen is populated on first launch. Real scores are appended automatically.

---

## Compatibility

- Python 3.9 or later
- Works on macOS, Linux, and Windows (PowerShell / Windows Terminal)
- ANSI colour codes require a terminal that supports them; on older Windows
  cmd.exe the output will still be readable but without colours
