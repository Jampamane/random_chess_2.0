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
    
    game = Game()
    game.play_game(game_type="10 min")
    """

    console = Console()
    table = Table()
    table.add_column()
    table.add_column()
    table.add_column()
    table.add_row("1", "0", "3")
    table.add_row("1", "0", "3")
    table.add_row("1", "0", "3")
    layout = Layout()
    layout.split_row(
        Layout(table, name="wow"),
        Layout(table, name="cancel")
    )
    console.print(layout)
    time.sleep(3)
    layout["wow"].update("hello")
    layout["cancel"].update("never")
    console.print(layout)
if __name__ == "__main__":
    main()
