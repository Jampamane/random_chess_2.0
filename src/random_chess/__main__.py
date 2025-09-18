"""Main module that handles running the chess game."""

from .chess_game import Game


def random_chess() -> None:
    """
    Main function. Establishes a Chess Game object
    and then plays the chess game.
    """
    game = Game(headless=True)
    while True:
        try:
            game.play_game(game_type="1 min")
        except KeyboardInterrupt:
            print("Stopping chess bot!")
            break


if __name__ == "__main__":
    random_chess()
