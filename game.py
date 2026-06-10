"""
game.py - Core game logic: difficulty settings, round execution, score calculation.
"""

import random
from dataclasses import dataclass, field
from typing import Optional

from utils import (
    Color, print_divider, print_header, print_success, print_error,
    print_info, print_warning, get_integer_input, animate_dots,
)


# ── Difficulty configuration ──────────────────────────────────────────────────

@dataclass(frozen=True)
class Difficulty:
    """Immutable settings for a single difficulty level."""
    name: str
    min_number: int
    max_number: int
    max_attempts: int
    score_multiplier: float
    label_color: str


DIFFICULTIES: dict[str, Difficulty] = {
    "easy": Difficulty(
        name="Easy",
        min_number=1,
        max_number=50,
        max_attempts=10,
        score_multiplier=1.0,
        label_color=Color.GREEN,
    ),
    "medium": Difficulty(
        name="Medium",
        min_number=1,
        max_number=100,
        max_attempts=7,
        score_multiplier=1.5,
        label_color=Color.YELLOW,
    ),
    "hard": Difficulty(
        name="Hard",
        min_number=1,
        max_number=200,
        max_attempts=5,
        score_multiplier=2.5,
        label_color=Color.RED,
    ),
}


# ── Per-round result ──────────────────────────────────────────────────────────

@dataclass
class RoundResult:
    """Outcome data from a single round."""
    won: bool
    score: int
    attempts_used: int
    secret_number: int
    difficulty: Difficulty


# ── Session-level statistics ──────────────────────────────────────────────────

@dataclass
class SessionStats:
    """Accumulated statistics for the current session."""
    games_played: int = 0
    games_won: int = 0
    total_score: int = 0
    best_score: int = 0

    @property
    def win_percentage(self) -> float:
        """Return win rate as a percentage (0–100)."""
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100

    def update(self, result: RoundResult) -> None:
        """Update session stats after a round."""
        self.games_played += 1
        if result.won:
            self.games_won += 1
            self.total_score += result.score
            if result.score > self.best_score:
                self.best_score = result.score


# ── Game class ────────────────────────────────────────────────────────────────

class Game:
    """
    Manages a single round of the number-guessing game.

    Responsibilities
    ----------------
    - Generate the secret number for the chosen difficulty.
    - Run the interactive guessing loop.
    - Evaluate guesses and provide hints.
    - Calculate the final score.
    """

    BASE_SCORE = 1000

    def __init__(self, difficulty_key: str) -> None:
        """
        Initialise a round.

        Args:
            difficulty_key: One of 'easy', 'medium', or 'hard'.
        """
        if difficulty_key not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty_key!r}")
        self.difficulty: Difficulty = DIFFICULTIES[difficulty_key]
        self._secret: int = random.randint(
            self.difficulty.min_number, self.difficulty.max_number
        )
        self.attempts_used: int = 0
        self.won: bool = False

    # ── Private helpers ───────────────────────────────────────────────────────

    def _attempts_left(self) -> int:
        return self.difficulty.max_attempts - self.attempts_used

    def _calculate_score(self) -> int:
        """Score = base × multiplier × (remaining_attempts / max_attempts)."""
        if not self.won:
            return 0
        remaining_ratio = self._attempts_left() / self.difficulty.max_attempts
        raw = self.BASE_SCORE * self.difficulty.score_multiplier * remaining_ratio
        return max(1, round(raw))

    def _print_attempt_bar(self) -> None:
        """Render a visual attempt-usage bar."""
        total = self.difficulty.max_attempts
        used = self.attempts_used
        remaining = total - used

        filled = "█" * remaining
        empty  = "░" * used

        if remaining > total * 0.5:
            bar_color = Color.GREEN
        elif remaining > total * 0.25:
            bar_color = Color.YELLOW
        else:
            bar_color = Color.RED

        bar = f"{bar_color}{filled}{Color.GRAY}{empty}{Color.RESET}"
        label = (
            f"  Attempts left: {bar_color}{Color.BOLD}{remaining}{Color.RESET}"
            f"{Color.GRAY}/{total}{Color.RESET}"
        )
        print(f"  {bar}  {label}")

    def _print_hint(self, guess: int) -> None:
        """Print a directional hint after a wrong guess."""
        diff = abs(self._secret - guess)
        if guess < self._secret:
            direction = f"{Color.BLUE}▲  Too low!{Color.RESET}"
        else:
            direction = f"{Color.RED}▼  Too high!{Color.RESET}"

        if diff <= 5:
            proximity = f"{Color.YELLOW}  🔥 Very close!{Color.RESET}"
        elif diff <= 15:
            proximity = f"{Color.CYAN}  ~ Getting warmer…{Color.RESET}"
        else:
            proximity = f"{Color.GRAY}  ❄  Still far away.{Color.RESET}"

        print(f"\n  {direction}{proximity}\n")

    # ── Public interface ──────────────────────────────────────────────────────

    def play(self) -> RoundResult:
        """
        Run the interactive guessing loop for this round.

        Returns:
            A RoundResult with the outcome, score, and metadata.
        """
        d = self.difficulty
        print_header(f"  {d.label_color}{d.name}{Color.RESET}{Color.BOLD}{Color.CYAN}  Mode  ")

        print_info(
            f"Guess a number between "
            f"{Color.BOLD}{d.min_number}{Color.RESET}{Color.CYAN} and "
            f"{Color.BOLD}{d.max_number}{Color.RESET}{Color.CYAN}."
        )
        print_info(f"You have {Color.BOLD}{d.max_attempts}{Color.RESET}{Color.CYAN} attempts.\n")

        while self._attempts_left() > 0:
            print_divider()
            self._print_attempt_bar()
            print()

            guess = get_integer_input(
                f"  Enter your guess [{d.min_number}–{d.max_number}]: ",
                min_val=d.min_number,
                max_val=d.max_number,
            )
            self.attempts_used += 1

            if guess == self._secret:
                self.won = True
                break

            self._print_hint(guess)

            if self._attempts_left() == 0:
                break

        score = self._calculate_score()
        self._print_round_end(score)

        return RoundResult(
            won=self.won,
            score=score,
            attempts_used=self.attempts_used,
            secret_number=self._secret,
            difficulty=self.difficulty,
        )

    def _print_round_end(self, score: int) -> None:
        """Display the end-of-round summary."""
        print_divider("═", color=Color.CYAN)
        if self.won:
            print_success(
                f"Correct! The number was {Color.BOLD}{self._secret}{Color.RESET}"
                f"{Color.GREEN}  🎉"
            )
            print(
                f"  {Color.CYAN}Score earned:{Color.RESET}  "
                f"{Color.BOLD}{Color.YELLOW}{score:,}{Color.RESET} pts\n"
            )
        else:
            print_error(
                f"Out of attempts! The number was "
                f"{Color.BOLD}{self._secret}{Color.RESET}."
            )
            print(f"  {Color.GRAY}Better luck next time.\n{Color.RESET}")
        print_divider("═", color=Color.CYAN)
