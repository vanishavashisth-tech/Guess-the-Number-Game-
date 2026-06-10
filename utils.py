"""
utils.py - Utility functions for input validation and console formatting.
"""

import os
import time


# ── Console colour codes ──────────────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foreground
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    # Background
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")


def print_divider(char: str = "─", width: int = 56, color: str = Color.GRAY) -> None:
    """Print a horizontal divider line."""
    print(f"{color}{char * width}{Color.RESET}")


def print_centered(text: str, width: int = 56, color: str = "") -> None:
    """Print text centred within a given width."""
    print(f"{color}{text.center(width)}{Color.RESET}")


def print_header(title: str) -> None:
    """Print a styled section header."""
    print()
    print_divider("═", color=Color.CYAN)
    print_centered(title, color=Color.BOLD + Color.CYAN)
    print_divider("═", color=Color.CYAN)
    print()


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"\n{Color.GREEN}{Color.BOLD}  ✔  {message}{Color.RESET}\n")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"\n{Color.RED}  ✖  {message}{Color.RESET}\n")


def print_info(message: str) -> None:
    """Print an informational message in cyan."""
    print(f"{Color.CYAN}  ℹ  {message}{Color.RESET}")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    print(f"{Color.YELLOW}  ⚠  {message}{Color.RESET}")


def animate_dots(message: str, duration: float = 1.2) -> None:
    """Show an animated dots effect for brief loading feedback."""
    import sys
    steps = int(duration / 0.3)
    for i in range(steps):
        dots = "." * ((i % 3) + 1)
        sys.stdout.write(f"\r{Color.CYAN}  {message}{dots}   {Color.RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
    print()


# ── Input helpers ─────────────────────────────────────────────────────────────

def get_integer_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """
    Prompt the user for an integer, re-prompting on invalid input.

    Args:
        prompt:  Text shown to the user.
        min_val: Inclusive lower bound (optional).
        max_val: Inclusive upper bound (optional).

    Returns:
        A validated integer within the requested range.
    """
    while True:
        raw = input(f"{Color.WHITE}{prompt}{Color.RESET}").strip()
        if not raw:
            print_error("Input cannot be empty. Please enter a number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print_error(f"'{raw}' is not a valid integer. Try again.")
            continue
        if min_val is not None and value < min_val:
            print_error(f"Please enter a number ≥ {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print_error(f"Please enter a number ≤ {max_val}.")
            continue
        return value


def get_string_input(prompt: str, max_length: int = 20, allow_empty: bool = False) -> str:
    """
    Prompt the user for a non-empty string.

    Args:
        prompt:      Text shown to the user.
        max_length:  Maximum allowed character count.
        allow_empty: If True, an empty string is accepted.

    Returns:
        A validated string.
    """
    while True:
        raw = input(f"{Color.WHITE}{prompt}{Color.RESET}").strip()
        if not raw and not allow_empty:
            print_error("Input cannot be empty.")
            continue
        if len(raw) > max_length:
            print_error(f"Name too long (max {max_length} characters).")
            continue
        return raw


def get_yes_no(prompt: str) -> bool:
    """
    Prompt the user for a yes/no answer.

    Returns:
        True for 'y', False for 'n'.
    """
    while True:
        raw = input(f"{Color.WHITE}{prompt} (y/n): {Color.RESET}").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print_error("Please enter 'y' or 'n'.")


def get_menu_choice(options: list[str], prompt: str = "Your choice") -> int:
    """
    Display a numbered menu and return the 1-based selection index.

    Args:
        options: List of menu item labels.
        prompt:  Prompt text shown after the menu.

    Returns:
        1-based integer corresponding to the chosen option.
    """
    for i, option in enumerate(options, start=1):
        print(f"  {Color.CYAN}{i}.{Color.RESET}  {option}")
    print()
    return get_integer_input(f"{prompt}: ", min_val=1, max_val=len(options))
