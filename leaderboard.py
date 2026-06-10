"""
leaderboard.py - Persistent leaderboard: save, load, and display top scores.
"""

import json
import os
from datetime import datetime
from typing import Optional

from utils import (
    Color, print_header, print_divider, print_centered,
    print_info, print_warning,
)


DATA_DIR  = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "leaderboard.json")
TOP_N     = 10

MEDAL = {1: "🥇", 2: "🥈", 3: "🥉"}

DIFFICULTY_COLORS = {
    "Easy":   Color.GREEN,
    "Medium": Color.YELLOW,
    "Hard":   Color.RED,
}


class Leaderboard:
    """
    Manages reading and writing scores to a JSON file.

    Each entry stored on disk:
    {
        "player": str,
        "score":  int,
        "difficulty": str,
        "attempts_used": int,
        "max_attempts":  int,
        "date": "YYYY-MM-DD HH:MM"
    }
    """

    def __init__(self) -> None:
        self._scores: list[dict] = []
        self._ensure_data_dir()
        self._load()

    # ── I/O ──────────────────────────────────────────────────────────────────

    def _ensure_data_dir(self) -> None:
        """Create the data directory if it does not exist."""
        os.makedirs(DATA_DIR, exist_ok=True)

    def _load(self) -> None:
        """Load scores from disk; initialise empty list on first run."""
        if not os.path.exists(DATA_FILE):
            self._scores = []
            self._write()
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                self._scores = data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            print_warning("Leaderboard file is corrupted – starting fresh.")
            self._scores = []
            self._write()

    def _write(self) -> None:
        """Persist the current scores list to disk."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as fh:
                json.dump(self._scores, fh, indent=2, ensure_ascii=False)
        except OSError as exc:
            print_warning(f"Could not save leaderboard: {exc}")

    # ── Public interface ──────────────────────────────────────────────────────

    def add_score(
        self,
        player: str,
        score: int,
        difficulty_name: str,
        attempts_used: int,
        max_attempts: int,
    ) -> None:
        """
        Append a new entry and persist to disk.

        Args:
            player:         Player's display name.
            score:          Points earned this round.
            difficulty_name: 'Easy', 'Medium', or 'Hard'.
            attempts_used:  How many guesses the player took.
            max_attempts:   Maximum guesses allowed for the difficulty.
        """
        entry = {
            "player":        player,
            "score":         score,
            "difficulty":    difficulty_name,
            "attempts_used": attempts_used,
            "max_attempts":  max_attempts,
            "date":          datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self._scores.append(entry)
        self._scores.sort(key=lambda e: e["score"], reverse=True)
        self._write()

    def top_scores(self, n: int = TOP_N) -> list[dict]:
        """Return the top-n entries sorted by score descending."""
        return self._scores[:n]

    def display(self) -> None:
        """Render the top-10 leaderboard table to the console."""
        print_header("🏆  Leaderboard — Top 10  🏆")

        entries = self.top_scores(TOP_N)
        if not entries:
            print_centered("No scores yet. Be the first to play!", color=Color.GRAY)
            print()
            return

        # Column widths
        rank_w   = 4
        name_w   = 16
        score_w  = 8
        diff_w   = 8
        tries_w  = 10
        date_w   = 16

        header = (
            f"  {'#':>{rank_w}}  "
            f"{'Player':<{name_w}}  "
            f"{'Score':>{score_w}}  "
            f"{'Level':<{diff_w}}  "
            f"{'Tries':>{tries_w}}  "
            f"{'Date':<{date_w}}"
        )
        print(f"{Color.BOLD}{Color.CYAN}{header}{Color.RESET}")
        print_divider()

        for i, entry in enumerate(entries, start=1):
            rank_display = MEDAL.get(i, f"{i:>{rank_w}}")

            diff_color = DIFFICULTY_COLORS.get(entry.get("difficulty", ""), Color.WHITE)
            diff_label = f"{diff_color}{entry.get('difficulty','?'):<{diff_w}}{Color.RESET}"

            # Highlight top 3 rows
            row_color = Color.BOLD + Color.WHITE if i <= 3 else ""
            reset     = Color.RESET if row_color else ""

            tries = f"{entry.get('attempts_used','?')}/{entry.get('max_attempts','?')}"

            print(
                f"{row_color}  {rank_display:<{rank_w+1}} "
                f"{entry.get('player','?'):<{name_w}}  "
                f"{Color.YELLOW}{entry.get('score',0):>{score_w},}{Color.RESET}  "
                f"{diff_label}  "
                f"{tries:>{tries_w}}  "
                f"{Color.GRAY}{entry.get('date',''):<{date_w}}{reset}{Color.RESET}"
            )

        print_divider()
        print()
