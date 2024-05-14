"""Defines all of the chess pieces and all of the movement rules."""

from piece_potential_moves import Moves


class Piece():
    """
    Defines all of the basic characteristics of a chess piece.
    All of the chess piece classes inherit from Piece.
    
    Args:
        color (str): Either "white" or "black".
    """
    def __init__(self, color: str) -> None:
        self.color = color
        self.board_position = "11"
        # These 2 variables get overwritten by the
        # classes that inherit from Piece:
        self.char_identifier = ""
        self.possible_moves = {}

    def __str__(self) -> str:
        match self.char_identifier:
            case "p":
                return "Pawn"
            case "n":
                return "Knight"
            case "b":
                return "Bishop"
            case "r":
                return "Rook"
            case "k":
                return "King"
            case "q":
                return "Queen"

    def set_position(self, position: str) -> None:
        """Set the position of the piece on the board.
        
        Args:
            position (str): 
                2 character identifier for
                where the piece is on the board.
                Example: '45' would be D5.
        """
        self.board_position = position

    def current_position(self) -> str:
        """Fetch the current position of the piece.

        Returns:
            board_posistion (str): 
                2 character identifier for where the piece is on the board.
                Example: '45' would be D5.
        """
        return self.board_position

    def _get_potential_moves(self) -> dict:
        """
        Create a dictionary of all the possible squares on the board that a 
        piece could move to, regardless if there is another piece 
        in the way or if the move is off of the board.

        Returns:
            moves (dict): 
                Dictionary object for all of the possible moves.
                Keys are move numbers, values are board positions.
                Example: {1: '12', 2: '22'}
                Returns empty dictionary if piece has been captured
                or if no available moves.
        """
        if self.board_position == "00":
            return {}
        horizontal_pos = int(self.board_position[0])
        vertical_pos = int(self.board_position[1])
        moves_dict = {}
        for indx, move in self.possible_moves.items():
            potential_horizontal = horizontal_pos + move["horizontal"]
            potential_vertical = vertical_pos + move["forward"]
            potential_move = str(potential_horizontal) + str(potential_vertical)
            moves_dict[indx] = potential_move
        return moves_dict

    def _on_the_board(self) -> dict:
        """
        Create a dictionary of all of the moves that don't go off of the board.
        Calls the internal function _get_potential_moves() and then
        filters out 'off the board' moves.

        Returns:
            moves (dict): 
                Dictionary object for all of the possible moves.
                Keys are move numbers, values are board positions.
                Example: {1: 12, 2: 22}
                Returns empty dictionary if piece has been captured
                or if no available moves.
        """
        potential_moves = self._get_potential_moves()
        if len(potential_moves) == 0:
            return {}
        moves_on_the_board = {}
        for indx, move in potential_moves.items():
            if len(move) == 2:
                if int(move[0]) >= 1 and int(move[0]) <= 8:
                    if int(move[1]) >= 1 and int(move[1]) <= 8:
                        moves_on_the_board[indx] = move
        return moves_on_the_board

    def _detect_collisions(self, move_dict: dict, all_piece_positions: dict) -> dict:
        """
        Create a dictionary of all of the potential collisions 
        given the potential moves of the piece.

        Args:
            move_dict (dict): 
                Dictionary of all of the potential moves of the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}

            all_piece_positions (dict):
                Dictionary of every piece position on the board.
                Keys are board positions, and values are 2 char identifiers.
                Example: {32: wr, 18: bk}

        Returns:
            collisions (dict): 
                Dictionary of all the collisions.
                Keys are board positions, and values are 2 char identifiers.
                Example: {32: wr, 18: bk}
                Returns empty dictionary if no potential moves.
        """
        if len(move_dict) == 0:
            return {}
        collisions = {}
        for move in move_dict.values():
            try:
                piece = all_piece_positions[move]
            except KeyError:
                pass
            else:
                collisions[move] = piece
        return collisions

    def _final_moves(self, move_dict: dict, collisions: dict) -> dict:
        """
        Final piece of logic to determine all of the valid moves for the piece.
        Uses collisions to figure out valid moves.
        This method is overwritten in a couple 
        of classes that inherit from the Piece class.
        This method is used by the Knight class and the King class.

        Args:
            move_dict (dict):
                Dictionary of all of the potential moves of the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}

            collisions (dict): 
                Dictionary of all the collisions.
                Keys are board positions, and values are 2 char identifiers.
                Example: {32: wr, 18: bk}

        Returns:
            final_moves (dict):
                Dictionary of all the final valid moves for the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}
                Returns empty dictionary if no potential moves.
        """
        if len(move_dict) == 0:
            return {}
        final_moves = {}
        for indx, move in move_dict.items():
            try:
                collision_piece = collisions[move]
            except KeyError:
                final_moves[indx] = move
            else:
                if collision_piece[0] != self.color[0]:
                    final_moves[indx] = move
        return final_moves

    def return_final_moves(self, all_piece_positions) -> dict:
        """Determine all of the valid moves for a piece.

        Args:
            all_piece_positions (dict):
                Dictionary of every piece position on the board.
                Keys are board positions, and values are 2 char identifiers.
                Example: {32: wr, 18: bk}

        Returns:
            final_moves (dict):
                Dictionary of all the final valid moves for the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}
                Returns empty dictionary if no final moves.
        """
        moves_on_the_board = self._on_the_board()
        collisions = self._detect_collisions(moves_on_the_board, all_piece_positions)
        final_moves = self._final_moves(moves_on_the_board, collisions)
        return final_moves

class Pawn(Piece):
    """
    Pawn class, inherits from Piece. 
    Overwrites the _final_moves method.

    Args:
        Piece (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.char_identifier = "p"
        if self.color == "white":
            self.possible_moves = Moves.WHITE_PAWN_MOVES.value
        if self.color == "black":
            self.possible_moves = Moves.BLACK_PAWN_MOVES.value

    def _final_moves(self, move_dict: dict, collisions: dict) -> dict:
        final_moves = {}
        piece_in_the_way_for_two_square_move = False
        for indx, move in move_dict.items():
            if indx == 1:
                try:
                    collision_piece = collisions[move]
                except KeyError:
                    final_moves[indx] = move
                else:
                    piece_in_the_way_for_two_square_move = True

            elif indx == 2:
                try:
                    collision_piece = collisions[move]
                except KeyError:
                    if (self.color == "black"
                    and int(self.board_position[1]) == 7
                    and piece_in_the_way_for_two_square_move is False
                    ):
                        final_moves[indx] = move
                    elif (self.color == "white"
                    and int(self.board_position[1]) == 2
                    and piece_in_the_way_for_two_square_move is False
                    ):
                        final_moves[indx] = move

            elif indx in (3, 4):
                try:
                    collision_piece = collisions[move]
                except KeyError:
                    pass
                else:
                    if collision_piece[0] != self.color[0]:
                        final_moves[indx] = move
        return final_moves

class Knight(Piece):
    """Knight class, inherits from Piece. 

    Args:
        Piece (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.char_identifier = "n"
        self.possible_moves = Moves.KNIGHT_MOVES.value

class King(Piece):
    """King class, inherits from Piece. 

    Args:
        Piece (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.char_identifier = "k"
        self.possible_moves = Moves.KING_MOVES.value

class Queen(Piece):
    """
    Queen class, inherits from Piece. 
    Overwrites the _final_moves method.
    Declares 'lines' of moves, 
    used in the new _final_moves method.

    Args:
        Piece (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.char_identifier = "q"
        self.possible_moves = Moves.QUEEN_MOVES.value

    def _final_moves(self, move_dict: dict, collisions: dict) -> dict:
        """
        Final piece of logic to determine all of the valid moves for the piece.
        Uses collisions to figure out valid moves.
        The Queen instance of _final_moves introduces move 'lines'.
        After 8 move checks it resets until it finds another collision.
        Once a collision is found it moves onto the next line.

        Args:
            move_dict (dict):
                Dictionary of all of the potential moves of the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}

            collisions (dict): 
                Dictionary of all the collisions.
                Keys are board positions, and values are 2 char identifiers.
                Example: {32: wr, 18: bk}

        Returns:
            final_moves (dict):
                Dictionary of all the final valid moves for the piece.
                Keys are move numbers, and values are board positions.
                Example: {1: 12, 2: 22}
                Returns empty dictionary if no potential moves.
        """
        final_moves = {}
        continue_the_line = True
        for indx, move in move_dict.items():
            if indx % 8 == 1:
                continue_the_line = True
            try:
                collision_piece = collisions[move]
            except KeyError:
                if continue_the_line is True:
                    final_moves[indx] = move
            else:
                if collision_piece[0] != self.color[0]:
                    final_moves[indx] = move
                continue_the_line = False
        return final_moves

class Bishop(Queen):
    """
    Bishop class, inherits from Queen, which inherits from Piece. 

    Args:
        Queen (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color) -> None:
        super().__init__(color)
        self.char_identifier = "b"
        self.possible_moves = Moves.BISHOP_MOVES.value

class Rook(Queen):
    """
    Rook class, inherits from Queen, which inherits from Piece. 

    Args:
        Queen (class): Class Pawn inherits from.
        color (str): Either "white" or "black".
    """
    def __init__(self, color) -> None:
        super().__init__(color)
        self.char_identifier = "r"
        self.possible_moves = Moves.ROOK_MOVES.value

