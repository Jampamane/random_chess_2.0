"""Defines the player and all of it's characteristics."""

from bs4 import BeautifulSoup
from pieces import Pawn
from pieces import Knight
from pieces import Rook
from pieces import Bishop
from pieces import King
from pieces import Queen
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Player():
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

    @property
    def pieces(self) -> list:
        return [self.pawn1, self.pawn2, self.pawn3, self.pawn4,
                self.pawn5, self.pawn6, self.pawn7, self.pawn8,
                self.rook1, self.rook2, self.kight1, self.kight2,
                self.bishop1, self.bishop2, self.king, self.queen]

    def get_piece_positions(self) -> dict:
        piece_dict = {}
        for piece in self.pieces:
            piece_dict[piece.board_position] = self.color[0] + piece.char_identifier
        return piece_dict
    
    def check_for_move(self, page_source):
        piece_positions = self.get_piece_positions()
        page_html_positions = page_source#self._create_dict(page_source)
        for position, piece in piece_positions.items():
            try:
                html_piece = page_html_positions[position]
                if html_piece == piece:
                    piece_positions.pop(position)
            except KeyError:
                pass
        
    def has_moved(self, page_source):
        page = BeautifulSoup(page_source, "html.parser")
        moves = page.find_all(class_ = f"{self.color} node")
        selected_move = page.find(class_ = f"{self.color} node selected")
        if selected_move:
            moves.append(selected_move)
        if len(moves) == 0:
            return False
        return True

    def _create_dict(self, browser: Chrome, sort_color: bool = True) -> dict:
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
            Example: A white pawn in position a1 would be {11: 'wp'}
        """
        piece_dict = {}
        board = browser.find_element(By.TAG_NAME, "wc-chess-board")
        positions = board.find_elements(By.TAG_NAME, "div")
        # Selects each div compenent that was turned into text
        for piece in positions:
            current_piece = ""
            current_position = ""
            # Deletes the quotation marks and
            # splits the div text component into individual values
            piece_text = str(piece.get_attribute("class")).split(sep=" ")
            # Iterates over each individual value
            for text in piece_text: #div br piece-88
                # Test to see if the value is a 2 character piece identifier
                if len(text) == 2:
                    if sort_color is True:
                        if self.color[0] == text[0]: # Test for correct color
                            # If not correct color break
                            break
                        current_piece = text
                    elif sort_color is False:
                        current_piece = text
                try:
                    int(text[-2:]) # Test for 2 chars cast to int
                except ValueError:
                    pass
                else:
                    current_position = text[-2:]
            # Update dictionary if values aren't empty
            if current_position and current_piece:
                piece_dict[current_position] = current_piece
        return piece_dict

    def set_positions(self, browser: Chrome) -> None:
        """
        Calls the create_dict function to create a dictionary with piece and location information.
        Uses that information to set the positions of each piece that is currently alive.

        Args:
            page_source (Chrome.page_source):
                Current page source from the selenium browser.
        """
        piece_dict = self._create_dict(browser=browser)
        piece_list = self._alive_pieces()
        for position, piece in piece_dict.items():
            for player_piece in piece_list:
                if piece[-1] == player_piece.char_identifier:
                    player_piece.set_position(position)
                    piece_list.remove(player_piece)
                    break
        if len(piece_list) != 0: #If there is still a piece left in piece_list,
            for piece in piece_list: #it wasn't found in the HTML and it must be dead
                piece.board_position = "00"

    def set_attribute(self, page_source, class_name) -> str:
        '''
        A bit of repeat logic in figuring out 
        which attribute to set when there are exactly 2 attributes.
        For example, 2 usernames, 2 clocks.
        '''
        page = BeautifulSoup(page_source, "html.parser")
        attributes = page.find_all(class_=class_name)
        flipped = page.find(class_="flipped")
        attribute = ""
        if flipped is not None:
            if self.color == "black":
                attribute = attributes[1].get_text()
            elif self.color == "white":
                attribute = attributes[0].get_text()
        elif flipped is None:
            if self.color == "black":
                attribute = attributes[0].get_text()
            elif self.color == "white":
                attribute = attributes[1].get_text()
        return attribute

    def set_username(self, page_source) -> str:
        username = self.set_attribute(page_source, "user-username-white")
        return username

    def set_time(self, page_source) -> str:
        clock_time = self.set_attribute(page_source, "clock-time-monospace")
        return clock_time

    def _alive_pieces(self) -> list:
        pieces = [piece for piece in self.pieces if piece.board_position != "00"]
        return pieces

    def is_turn(self, browser: Chrome) -> bool:
        try:
            browser.find_element(
                By.CLASS_NAME, f"clock-component.clock-bottom.clock-{self.color}.clock-player-turn")
        except NoSuchElementException:
            return False
        return True


    def retrieve_final_moves(self, browser: Chrome, all_pieces = None, piece_list = None):
        final_moves = []
        if piece_list is None:
            piece_list = self._alive_pieces()
        if all_pieces is None:
            all_pieces = self._create_dict(browser=browser, sort_color=False)
        for piece in piece_list:
            moves = piece.return_final_moves(all_pieces)
            if len(moves) > 0:
                for move in moves.values():
                    final_moves.append((piece, move))
        return final_moves

    def retrieve_non_check_moves(self, browser: Chrome, opponent):
        player_potential_moves = self.retrieve_final_moves(browser=browser)
        all_the_pieces = self._create_dict(browser=browser, sort_color=False)
        opponent_alive_pieces_copy = opponent._alive_pieces()
        opponent_current_positions = {
            piece.board_position: piece for piece in opponent._alive_pieces()}
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
            opponent_moves = {move: "Value don't matter" for piece, move in
                              opponent.retrieve_final_moves(
                                  browser=browser,
                                  all_pieces=all_the_pieces,
                                  piece_list=opponent_alive_pieces_copy)}
            try:
                if str(piece) == "King":
                    opponent_moves[move]
                elif str(piece) != "King":
                    opponent_moves[self.king.board_position]
            except KeyError:
                non_check_moves.append((piece, move))
            finally:
                all_the_pieces.pop(move)
                all_the_pieces[piece.board_position] = f"{self.color[0]}{piece.char_identifier}"
            if capture_piece is not None:
                opponent_alive_pieces_copy.append(capture_piece)
        if len(non_check_moves) == 0:
            return None
        return non_check_moves
