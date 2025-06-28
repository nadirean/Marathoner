"""
A module to run the Marathoner game.
"""

import sys

from modules.Game import Game


def main() -> None:
    """
    Main entry point for the Marathoner game.

    Initializes and runs the game loop. Handles any top-level exceptions
    that might occur during game initialization or execution.
    """
    try:
        marathoner = Game()
        marathoner.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
