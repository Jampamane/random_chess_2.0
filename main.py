"""Main module that handles running the chess game."""
from chess_game import Game
from rich.layout import Layout
from rich.console import Console
from rich.table import Table
import time

def main() -> None:
    """
    Main function. Establishes a Chess Game object
    and then plays the chess game.
    """
    game = Game(headless=True)
    game.play_game(game_type="1 min")


if __name__ == "__main__":
    main()
