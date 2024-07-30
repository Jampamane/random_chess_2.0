"""Defines the player and all of it's characteristics."""

from __future__ import annotations

from pieces import Piece
from pieces import Pawn
from pieces import Knight
from pieces import Rook
from pieces import Bishop
from pieces import King
from pieces import Queen
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Player:
    """Player object that handles all the logic for the player."""

    def __init__(self, color: str) -> None:
        self.color = color
        self.pawn1 = Pawn(color)
        self.pawn2 = Pawn(color)
        self.pawn3 = Pawn(color)
        self.pawn4 = Pawn(color)
        self.pawn5 = Pawn(color)
        self.pawn6 = Pawn(color)
        self.pawn7 = Pawn(color)
        self.pawn8 = Pawn(color)
        self.rook1 = Rook(color)
        self.rook2 = Rook(color)
        self.kight1 = Knight(color)
        self.kight2 = Knight(color)
        self.bishop1 = Bishop(color)
        self.bishop2 = Bishop(color)
        self.king = King(color)
        self.queen = Queen(color)
        self.potential_moves = ""

    @property
    def pieces(self) -> list[Piece]:
        """List of player pieces.

        Returns:
            list[Piece]: A list of all of the player objects. 16 pieces in total.
        """
        return [
            self.pawn1,
            self.pawn2,
            self.pawn3,
            self.pawn4,
            self.pawn5,
            self.pawn6,
            self.pawn7,
            self.pawn8,
            self.rook1,
            self.rook2,
            self.kight1,
            self.kight2,
            self.bishop1,
            self.bishop2,
            self.king,
            self.queen,
        ]

    @property
    def alive_pieces(self) -> list[Piece]:
        """
        List of player pieces that are alive.
        Does a simple check to make sure the piece position doesn't equal "00".

        Returns:
            list[Piece]: A list of all the player objects that are alive.
        """
        return [piece for piece in self.pieces if piece.board_position != "00"]

    @property
    def piece_positions(self) -> dict[str, str]:
        """Fetch all of the positions of each piece that is alive.

        Returns:
            dict[str, str]:
                Dictionary of all the pieces that are alive.
                Keys are positions and values are piece identities.
                Example: {"45": "bk"} is Black King in position 45.
        """
        piece_dict = {}
        for piece in self.alive_pieces:
            piece_dict[piece.board_position] = piece.identity
        return piece_dict

    def _create_dict(self, pieces: list[str], sort_type: str = "all") -> dict[str, str]:
        """
        Reads the browser's HTML and creates a
        dictionary with piece and location information.

        Args:
            page_source (Chrome.page_source):
                Current page source from the selenium browser.
            sort_color (bool, optional):
                Defaults to True. If set to false, will only return
                white pieces or black pieces depending on the player color.

        Returns:
            dict: Dictionary with information on each piece.
            Format is: {board_position: piece}.
            Example: A white pawn in position a1 would be {'11': 'wp'}
        """
        piece_dict = {}

        for piece in pieces:  # Selects each div compenent that was turned into text
            current_piece = None
            current_position = None
            piece = piece.replace('"', "").split()

            for text in piece:  # Iterates over each individual value
                if (
                    len(text) != 2
                ):  # Test to see if the value is a 2 character piece identifier
                    try:
                        int(
                            text[-2:]
                        )  # Test to see if the last 2 characters can be cast to an int
                    except ValueError:
                        pass
                    else:
                        current_position = text[-2:]
                elif len(text) == 2:
                    if sort_type == "all":
                        current_piece = text
                    elif sort_type == "player":
                        if self.color[0] == text[0]:
                            current_piece = text
                    elif sort_type == "opponent":
                        if self.color[0] != text[0]:
                            current_piece = text

            if (
                current_position and current_piece
            ):  # Update dictionary only if correct color
                piece_dict[current_position] = current_piece

        return piece_dict

    def set_positions(self, pieces: list[str]) -> None:
        """
        Calls the create_dict function to create a dictionary with piece and location information.
        Uses that information to set the positions of each piece that is currently alive.

        Args:
            page_source (Chrome.page_source):
                Current page source from the selenium browser.
        """
        piece_dict = self._create_dict(pieces=pieces, sort_type="player")
        piece_list = self.alive_pieces
        for position, piece in piece_dict.items():
            for player_piece in piece_list:
                if piece == player_piece.identity:
                    player_piece.set_position(position)
                    piece_list.remove(player_piece)
                    break
        if len(piece_list) != 0:  # If there is still a piece left in piece_list,
            for piece in piece_list:  # it wasn't found in the HTML and it must be dead
                piece.board_position = "00"

    def is_turn(self, browser: Chrome) -> bool:
        """Checks to see if it's the your turn.

        Args:
            browser (Chrome): Selenium Chrome browser.

        Returns:
            bool: True if turn, False if not.
        """
        try:
            browser.find_element(
                By.CLASS_NAME,
                f"clock-component.clock-bottom.clock-{self.color}.clock-player-turn",
            )
        except NoSuchElementException:
            return False
        return True

    def human_readable_format(self, move_list: list[tuple[Piece, str]]) -> list:
        """Turns the move_list into a readable format to be displayed in the terminal.

        Args:
            move_list (list[tuple[Piece, str]]): Move list to be converted.

        Returns:
            list: Human readable format list.
        """
        readable_list = []
        decode = {
            "piece": {
                "p": "Pawn",
                "n": "Knight",
                "b": "Bishop",
                "r": "Rook",
                "k": "King",
                "q": "Queen",
            },
            "position": {
                "1": "A",
                "2": "B",
                "3": "C",
                "4": "D",
                "5": "E",
                "6": "F",
                "7": "G",
                "8": "H",
            },
        }
        for move in move_list:
            piece = decode["piece"][move[0].identity[1]]
            position = decode["position"][move[1][0]] + move[1][1]
            message = f"{piece}: {position}"
            readable_list.append(message)

        return readable_list

    def retrieve_final_moves(
        self,
        pieces: list[str],
        all_pieces: dict[str, str] = None,
        piece_list: list[Piece] = None,
    ) -> list[tuple[Piece, str]]:
        """
        Retrieves all of the moves that all the pieces can do,
        regardless if doing that move will put you in check.

        Args:
            pieces (list[str]): List of all player pieces.
            all_pieces (dict, optional):
                Dictionary list of all the pieces, player and opponent.
                Defaults to None, for retrieve_non_check_moves().
            piece_list (dict, optional):
                List of all the alive pieces.
                Defaults to None, for retrieve_non_check_moves().

        Returns:
            list[tuple[Piece, str]]: List of all the final moves.
        """
        final_moves = []
        if piece_list is None:
            piece_list = self.alive_pieces
        if all_pieces is None:
            all_pieces = self._create_dict(pieces=pieces, sort_type="all")
        for piece in piece_list:
            moves = piece.return_final_moves(all_pieces)
            if len(moves) > 0:
                for move in moves.values():
                    final_moves.append((piece, move))
        return final_moves

    def retrieve_non_check_moves(
        self, pieces: list[str], opponent: Player
    ) -> list[tuple[Piece, str]]:
        """
        Retrieves all of the moves that all the pieces can do,
        specifically taking into account if doing that move will put the player in check.

        Args:
            pieces (list[str]): List of all the player pieces.
            opponent (Player): The opponent object.

        Returns:
            list[tuple[Piece, str]]: List of the FINAL, final moves.
        """
        player_potential_moves = self.retrieve_final_moves(pieces=pieces)
        all_the_pieces = self._create_dict(pieces=pieces, sort_type="all")
        opponent_alive_pieces_copy = opponent.alive_pieces
        opponent_current_positions = {
            piece.board_position: piece for piece in opponent.alive_pieces
        }
        non_check_moves = []
        for piece, move in player_potential_moves:
            capture_piece = None
            try:
                capture_piece = opponent_current_positions[move]
            except KeyError:
                pass
            else:
                opponent_alive_pieces_copy.remove(capture_piece)
            all_the_pieces.pop(piece.board_position)
            all_the_pieces[move] = f"{self.color[0]}{piece.char_identifier}"
            opponent_moves = {
                move: "Value don't matter"
                for piece, move in opponent.retrieve_final_moves(
                    pieces=pieces,
                    all_pieces=all_the_pieces,
                    piece_list=opponent_alive_pieces_copy,
                )
            }
            try:
                if str(piece) == "King":
                    if move not in opponent_moves.values():
                        raise KeyError
                elif str(piece) != "King":
                    if self.king.board_position not in opponent_moves.values():
                        raise KeyError
            except KeyError:
                non_check_moves.append((piece, move))
            finally:
                all_the_pieces.pop(move)
                all_the_pieces[piece.board_position] = (
                    f"{self.color[0]}{piece.char_identifier}"
                )
            if capture_piece is not None:
                opponent_alive_pieces_copy.append(capture_piece)

        self.potential_moves = self.human_readable_format(move_list=non_check_moves)
        return non_check_moves
