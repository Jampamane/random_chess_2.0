"""Main module that handles running the chess game."""
from chess_game import Game
import time

def main() -> None:
    """
    Main function. Establishes a Chess Game object
    and then plays the chess game.
    """
    game = Game()
    game.play_game(game_type="10 min")

if __name__ == "__main__":
    main()
