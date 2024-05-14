"""Main module that handles running the chess game."""

from chess_game import Game

def main() -> None:
    """
    Main function. Establishes a Chess Game object
    and then plays the chess game.

    Args:
        game_url (str): URL for the chess game.
    """
    game = Game()

if __name__ == "__main__":
    main()