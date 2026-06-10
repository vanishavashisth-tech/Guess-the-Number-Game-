"""
main.py - Entry point: welcome screen, main menu, and navigation flow.
"""

import sys

from game import Game, DIFFICULTIES, SessionStats
from leaderboard import Leaderboard
from utils import (
    Color, clear_screen, print_header, print_divider, print_centered,
    print_success, print_info, print_warning, get_string_input,
    get_menu_choice, get_yes_no, animate_dots,
)


# ── ASCII banner ──────────────────────────────────────────────────────────────

BANNER = r"""
   ___                       _   _
  / __|_  _ ___ ___  ___ _  | |_| |_  ___
 | (_ | || / -_|_-< (_-<_   |  _| ' \/ -_)
  \___|\_,_\___/__/ /__(_)   \__|_||_\___|
  _  _           _
 | \| |_  _ _ __| |__  ___ _ _
 | .` | || | '  \ '_ \/ -_) '_|
 |_|\_|\_,_|_|_|_|_.__/\___|_|
"""

TAGLINE = "How many guesses will it take you?"


def print_welcome() -> None:
    """Render the splash screen."""
    clear_screen()
    print(f"{Color.BOLD}{Color.MAGENTA}{BANNER}{Color.RESET}")
    print_centered(TAGLINE, color=Color.GRAY)
    print()
    print_divider("─", color=Color.GRAY)
    print()


def print_instructions() -> None:
    """Display game rules and scoring explanation."""
    print_header("📖  How to Play")

    lines = [
        ("Pick a difficulty", "Easy · Medium · Hard"),
        ("Guess the number", "Enter your guess each round"),
        ("Read the hints",    "Too high / Too low / proximity hint"),
        ("Score points",      "Fewer attempts = higher score"),
        ("Beat the board",    "Top 10 scores saved permanently"),
    ]

    for step, (title, desc) in enumerate(lines, start=1):
        print(
            f"  {Color.CYAN}{step}.{Color.RESET}  "
            f"{Color.BOLD}{title:<20}{Color.RESET}  "
            f"{Color.GRAY}{desc}{Color.RESET}"
        )

    print()
    print_divider()
    print(f"\n  {Color.YELLOW}Score formula:{Color.RESET}")
    print(f"  {Color.GRAY}score = 1000 × difficulty_multiplier × (remaining / max) attempts{Color.RESET}")
    print()

    multipliers = [
        ("Easy",   "×1.0", Color.GREEN),
        ("Medium", "×1.5", Color.YELLOW),
        ("Hard",   "×2.5", Color.RED),
    ]
    for name, mult, color in multipliers:
        print(f"    {color}{name:<8}{Color.RESET}  {Color.BOLD}{mult}{Color.RESET}")
    print()


def choose_difficulty() -> str:
    """Prompt the user to select a difficulty and return its key."""
    print_header("⚙  Choose Difficulty")

    options = []
    for key, d in DIFFICULTIES.items():
        rng     = f"{d.min_number}–{d.max_number}"
        label   = (
            f"{d.label_color}{Color.BOLD}{d.name:<8}{Color.RESET}  "
            f"{Color.GRAY}Range: {rng:<8}  Attempts: {d.max_attempts}{Color.RESET}"
        )
        options.append(label)

    choice = get_menu_choice(options, prompt="Select difficulty")
    return list(DIFFICULTIES.keys())[choice - 1]


def play_round(player: str, leaderboard: Leaderboard, stats: SessionStats) -> None:
    """Run a single round and handle post-round leaderboard update."""
    difficulty_key = choose_difficulty()
    game = Game(difficulty_key)
    result = game.play()

    stats.update(result)

    if result.won:
        leaderboard.add_score(
            player=player,
            score=result.score,
            difficulty_name=result.difficulty.name,
            attempts_used=result.attempts_used,
            max_attempts=result.difficulty.max_attempts,
        )
        print_info("Score saved to the leaderboard.")


def show_stats(stats: SessionStats) -> None:
    """Display session statistics."""
    print_header("📊  Your Session Stats")

    rows = [
        ("Games played",   str(stats.games_played)),
        ("Games won",      str(stats.games_won)),
        ("Win rate",       f"{stats.win_percentage:.1f}%"),
        ("Total score",    f"{stats.total_score:,}"),
        ("Best score",     f"{stats.best_score:,}"),
    ]

    for label, value in rows:
        print(
            f"  {Color.GRAY}{label:<16}{Color.RESET}  "
            f"{Color.BOLD}{Color.WHITE}{value}{Color.RESET}"
        )
    print()


def main_menu(player: str, leaderboard: Leaderboard, stats: SessionStats) -> None:
    """
    Main navigation loop.

    Args:
        player:      Validated player name.
        leaderboard: Shared Leaderboard instance.
        stats:       Shared SessionStats instance.
    """
    options = [
        "Play a round",
        "View leaderboard",
        "Your stats",
        "Instructions",
        "Change name",
        "Quit",
    ]

    while True:
        clear_screen()
        print_welcome()
        print(
            f"  {Color.GRAY}Logged in as:{Color.RESET}  "
            f"{Color.BOLD}{Color.MAGENTA}{player}{Color.RESET}\n"
        )

        choice = get_menu_choice(options, prompt="Main menu")

        if choice == 1:
            play_round(player, leaderboard, stats)
            if not get_yes_no("\n  Play another round?"):
                continue

        elif choice == 2:
            clear_screen()
            leaderboard.display()
            input(f"  {Color.GRAY}Press Enter to go back…{Color.RESET}")

        elif choice == 3:
            clear_screen()
            show_stats(stats)
            input(f"  {Color.GRAY}Press Enter to go back…{Color.RESET}")

        elif choice == 4:
            clear_screen()
            print_instructions()
            input(f"  {Color.GRAY}Press Enter to go back…{Color.RESET}")

        elif choice == 5:
            clear_screen()
            player = get_string_input("  Enter new name: ", max_length=20)

        elif choice == 6:
            clear_screen()
            print_welcome()
            print_centered(
                f"Thanks for playing, {player}!  Final score: {stats.total_score:,} pts",
                color=Color.CYAN,
            )
            print()
            sys.exit(0)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """Initialise game components and launch the main menu."""
    print_welcome()
    print_info("Loading leaderboard…")
    leaderboard = Leaderboard()

    print()
    player = get_string_input("  Enter your name: ", max_length=20)
    animate_dots("Starting game", duration=0.9)

    stats = SessionStats()
    main_menu(player, leaderboard, stats)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.GRAY}  Game interrupted. Goodbye!{Color.RESET}\n")
        sys.exit(0)
