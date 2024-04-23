import moves

class Piece():
    def __init__(self, color):
        self.color = color
        self.board_position = "00"

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

    def set_position(self, position):
        self.board_position = position

    def current_position(self):
        return self.board_position

    def get_potential_moves(self):
        if self.board_position == "00":
            return None
        horizontal_position = int(self.board_position[0])
        vertical_position = int(self.board_position[1])
        move_list = []
        for indx, move in enumerate(self.possible_moves, 1):
            move_dict = self.possible_moves[move]
            potential_horizontal = horizontal_position + move_dict["horizontal"]
            potential_vertical = vertical_position + move_dict["forward"]
            potential_move = str(potential_horizontal) + str(potential_vertical)
            move_list.append((indx, potential_move))
        return move_list

    def on_the_board(self, move_list):
        on_the_board = []
        for indx, move in move_list:
            if len(move) == 2:
                if int(move[0]) >= 1 and int(move[0]) <= 8:
                    if int(move[1]) >= 1 and int(move[1]) <= 8:
                        on_the_board.append((indx, move))
        return on_the_board

    def detect_collisions(self, move_list, all_piece_positions):
        collisions = {}
        for indx, move in move_list:
            try:
                piece = all_piece_positions[move]
            except KeyError:
                pass
            else:
                collisions[move] = piece
        if len(collisions) == 0:
            return None
        return collisions

    def final_moves(self, move_list, collisions):
        final_moves = []
        for indx, move in move_list:
            try:
                collision_piece = collisions[move]
            except KeyError:
                final_moves.append(move)
            else:
                if collision_piece[0] == self.color[0]:
                    pass
                else:
                    final_moves.append(move)
        if len(final_moves) == 0:
            return None
        return final_moves

    def return_final_moves(self, all_the_pieces):
        potential_moves = self.get_potential_moves()
        on_the_board = self.on_the_board(potential_moves)
        collisions = self.detect_collisions(on_the_board, all_the_pieces)
        final_moves_list = self.final_moves(on_the_board, collisions)
        if final_moves_list is None:
            return None
        final_moves_tuple = []
        for move in final_moves_list:
            final_moves_tuple.append((self, move))
        return final_moves_tuple

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "p"
        if self.color == "white":
            self.possible_moves = moves.WHITE_PAWN_MOVES
        if self.color == "black":
            self.possible_moves = moves.BLACK_PAWN_MOVES

    def final_moves(self, move_list, collisions):
        final_moves = []
        jumping = False
        for indx, move in move_list:
            try:
                collision_piece = collisions[move]
            except KeyError:
                if indx == 2:
                    if jumping is True:
                        pass
                    elif self.color == "black" and int(self.board_position[1]) == 7:
                        final_moves.append(move)
                    elif self.color == "white" and int(self.board_position[1]) == 2:
                        final_moves.append(move)
                elif indx in (3, 4):
                    pass
                else:
                    final_moves.append(move)
            else:
                if indx == 1:
                    jumping = True
                elif indx in (3, 4):
                    if collision_piece[0] == self.color[0]:
                        pass
                    else:
                        final_moves.append(move)
        if len(final_moves) == 0:
            return None
        return final_moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "n"
        self.possible_moves = moves.KNIGHT_MOVES

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "k"
        self.possible_moves = moves.KING_MOVES

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "q"
        self.possible_moves = moves.QUEEN_MOVES
        self.down_line = {indx: value for indx, value in
                          self.possible_moves.items() if indx <= 8}
        self.up_line = {indx: value for indx, value in
                        self.possible_moves.items() if indx > 8 and indx <= 16}
        self.right_line = {indx: value for indx, value in
                           self.possible_moves.items() if indx > 16 and indx <= 24}
        self.left_line = {indx: value for indx, value in
                          self.possible_moves.items() if indx > 24 and indx <= 32}
        self.down_left_line = {indx: value for indx, value in
                               self.possible_moves.items() if indx > 32 and indx <= 40}
        self.up_right_line = {indx: value for indx, value in
                              self.possible_moves.items() if indx > 40 and indx <= 48}
        self.down_right_line = {indx: value for indx, value in
                                self.possible_moves.items() if indx > 48 and indx <= 56}
        self.up_left_line = {indx: value for indx, value in
                             self.possible_moves.items() if indx > 56 and indx <= 64}
        self.lines = [self.down_line, self.up_line, self.right_line, self.left_line,
                      self.down_left_line, self.up_right_line, 
                      self.down_right_line, self.up_left_line]
    
    def final_moves(self, move_list, collisions):
        final_moves = []
        potential_moves = {move: indx for indx, move in move_list}
        horizontal_position = int(self.board_position[0])
        vertical_position = int(self.board_position[1])
        for line in self.lines:
            for move in line:
                test_horizontal = int(line[move]["horizontal"]) + horizontal_position
                test_vertical = int(line[move]["forward"]) + vertical_position
                test_square = str(test_horizontal) + str(test_vertical)
                try:
                    potential_moves[test_square]
                except KeyError:
                    break
                else:
                    try:
                        collision_piece = collisions[test_square]
                    except KeyError:
                        final_moves.append(test_square)
                    else:
                        if collision_piece[0] == self.color[0]:
                            break
                        final_moves.append(test_square)
                        break
        if len(final_moves) == 0:
            return None
        return final_moves

class Bishop(Queen):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "b"
        self.possible_moves = {indx: move for indx, move in 
                               self.possible_moves.items() if indx > 32}
        self.lines = [self.down_left_line, self.up_right_line, 
                      self.down_right_line, self.up_left_line]

class Rook(Queen):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "r"
        self.possible_moves = {indx: move for indx, move in 
                               self.possible_moves.items() if indx <= 32}
        self.lines = [self.down_line, self.up_line, 
                      self.right_line, self.left_line]
