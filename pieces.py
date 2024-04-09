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
            move_dict = (self.possible_moves[move])
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
                collisions[move] = piece
            except:
                pass
        if len(collisions) == 0:
            return None
        else:
            return collisions
    def final_moves(self, move_list, collisions):
        final_moves = []
        for indx, move in move_list:
            try:
                collision_piece = collisions[move]
                if collision_piece[0] == self.color[0]:
                    pass
                else:
                    final_moves.append(move)
            except:
                final_moves.append(move)
        if len(final_moves) == 0:
            return None
        else:
            return final_moves
    def return_final_moves(self, all_the_pieces):
        potential_moves = self.get_potential_moves()
        on_the_board = self.on_the_board(potential_moves)
        collisions = self.detect_collisions(on_the_board, all_the_pieces)
        final_moves_list = self.final_moves(on_the_board, collisions)
        if final_moves_list == None:
            return None
        else:
            final_moves_tuple = []
            for move in final_moves_list:
                final_moves_tuple.append((self, move))
            return final_moves_tuple
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "p"
        if self.color == "white":
            self.possible_moves = {1:{"forward": 1, "horizontal": 0}, 
                                   2:{"forward": 2, "horizontal": 0}, 
                                   3:{"forward": 1, "horizontal": 1},
                                   4:{"forward": 1, "horizontal":-1}}
        if self.color == "black":
            self.possible_moves = {1:{"forward":-1, "horizontal": 0}, 
                                   2:{"forward":-2, "horizontal": 0}, 
                                   3:{"forward":-1, "horizontal": 1},
                                   4:{"forward":-1, "horizontal":-1}}
    def final_moves(self, move_list, collisions):
        final_moves = []
        jumping = False
        for indx, move in move_list:
            try:
                collision_piece = collisions[move]
                if indx == 1:
                    jumping = True

                elif indx == 3 or indx == 4:
                    if collision_piece[0] == self.color[0]:
                        pass
                    else:
                        final_moves.append(move)
            except:
                if indx == 2:
                    if jumping == True:
                        pass
                    elif self.color == "black" and int(self.board_position[1]) == 7:
                        final_moves.append(move)
                    elif self.color == "white" and int(self.board_position[1]) == 2:
                        final_moves.append(move)
                elif indx == 3 or indx == 4:
                    pass
                else:
                    final_moves.append(move)

        if len(final_moves) == 0:
            return None
        else:
            return final_moves
    
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "n"
        self.possible_moves =  {1:{"forward": 2, "horizontal": 1}, 
                                2:{"forward": 2, "horizontal":-1}, 
                                3:{"forward":-2, "horizontal": 1},
                                4:{"forward":-2, "horizontal":-1},
                                5:{"forward": 1, "horizontal": 2}, 
                                6:{"forward": 1, "horizontal":-2}, 
                                7:{"forward":-1, "horizontal": 2},
                                8:{"forward":-1, "horizontal":-2}}

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "k"
        self.possible_moves =  {1:{"forward": 1, "horizontal": 0}, 
                                2:{"forward":-1, "horizontal": 0}, 
                                3:{"forward": 0, "horizontal": 1},
                                4:{"forward": 0, "horizontal":-1},
                                5:{"forward": 1, "horizontal": 1}, 
                                6:{"forward": 1, "horizontal":-1}, 
                                7:{"forward":-1, "horizontal": 1},
                                8:{"forward":-1, "horizontal":-1}}
        
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "q"
        self.possible_moves =  {1:{"forward":-1, "horizontal": 0}, 
                                2:{"forward":-2, "horizontal": 0}, 
                                3:{"forward":-3, "horizontal": 0},
                                4:{"forward":-4, "horizontal": 0},
                                5:{"forward":-5, "horizontal": 0}, 
                                6:{"forward":-6, "horizontal": 0}, 
                                7:{"forward":-7, "horizontal": 0},
                                8:{"forward":-8, "horizontal": 0},
                                9:{"forward": 1, "horizontal": 0}, 
                                10:{"forward":2, "horizontal": 0}, 
                                11:{"forward":3, "horizontal": 0},
                                12:{"forward":4, "horizontal": 0},
                                13:{"forward":5, "horizontal": 0}, 
                                14:{"forward":6, "horizontal": 0}, 
                                15:{"forward":7, "horizontal": 0},
                                16:{"forward":8, "horizontal": 0},
                                17:{"forward": 0,"horizontal": 1}, 
                                18:{"forward": 0,"horizontal": 2}, 
                                19:{"forward": 0,"horizontal": 3},
                                20:{"forward": 0,"horizontal": 4},
                                21:{"forward": 0,"horizontal": 5}, 
                                22:{"forward": 0,"horizontal": 6}, 
                                23:{"forward": 0,"horizontal": 7},
                                24:{"forward": 0,"horizontal": 8},
                                25:{"forward":0, "horizontal":-1}, 
                                26:{"forward":0, "horizontal":-2}, 
                                27:{"forward":0, "horizontal":-3},
                                28:{"forward":0, "horizontal":-4},
                                29:{"forward":0, "horizontal":-5}, 
                                30:{"forward":0, "horizontal":-6}, 
                                31:{"forward":0, "horizontal":-7},
                                32:{"forward":0, "horizontal":-8},
                                33:{"forward":-1,"horizontal":-1}, 
                                34:{"forward":-2,"horizontal":-2}, 
                                35:{"forward":-3,"horizontal":-3},
                                36:{"forward":-4,"horizontal":-4},
                                37:{"forward":-5,"horizontal":-5}, 
                                38:{"forward":-6,"horizontal":-6}, 
                                39:{"forward":-7,"horizontal":-7},
                                40:{"forward":-8,"horizontal":-8},
                                41:{"forward":1, "horizontal": 1}, 
                                42:{"forward":2, "horizontal": 2}, 
                                43:{"forward":3, "horizontal": 3},
                                44:{"forward":4, "horizontal": 4},
                                45:{"forward":5, "horizontal": 5}, 
                                46:{"forward":6, "horizontal": 6}, 
                                47:{"forward":7, "horizontal": 7},
                                48:{"forward":8, "horizontal": 8},
                                49:{"forward":-1,"horizontal": 1}, 
                                50:{"forward":-2,"horizontal": 2}, 
                                51:{"forward":-3,"horizontal": 3},
                                52:{"forward":-4,"horizontal": 4},
                                53:{"forward":-5,"horizontal": 5}, 
                                54:{"forward":-6,"horizontal": 6}, 
                                55:{"forward":-7,"horizontal": 7},
                                56:{"forward":-8,"horizontal": 8},
                                57:{"forward":1, "horizontal":-1}, 
                                58:{"forward":2, "horizontal":-2}, 
                                59:{"forward":3, "horizontal":-3},
                                60:{"forward":4, "horizontal":-4},
                                61:{"forward":5, "horizontal":-5}, 
                                62:{"forward":6, "horizontal":-6}, 
                                63:{"forward":7, "horizontal":-7},
                                64:{"forward":8, "horizontal":-8}}
        self.down_line = {indx: value for indx, value in self.possible_moves.items() if indx <= 8}
        self.up_line = {indx: value for indx, value in self.possible_moves.items() if indx > 8 and indx <= 16}
        self.right_line = {indx: value for indx, value in self.possible_moves.items() if indx > 16 and indx <= 24}
        self.left_line = {indx: value for indx, value in self.possible_moves.items() if indx > 24 and indx <= 32}
        self.down_left_line = {indx: value for indx, value in self.possible_moves.items() if indx > 32 and indx <= 40}
        self.up_right_line = {indx: value for indx, value in self.possible_moves.items() if indx > 40 and indx <= 48}
        self.down_right_line = {indx: value for indx, value in self.possible_moves.items() if indx > 48 and indx <= 56}
        self.up_left_line = {indx: value for indx, value in self.possible_moves.items() if indx > 56 and indx <= 64}
        self.lines = [self.down_line, self.up_line, self.right_line, self.left_line,
                      self.down_left_line, self.up_right_line, self.down_right_line, self.up_left_line]
    
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
                    try:
                        collision_piece = collisions[test_square]
                        if collision_piece[0] == self.color[0]:
                            break
                        else:
                            final_moves.append(test_square)
                            break
                    except:
                        final_moves.append(test_square)
                except:
                    break
        if len(final_moves) == 0:
            return None
        else:
            return final_moves
        
class Bishop(Queen):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "b"
        self.possible_moves = {indx: move for indx, move in self.possible_moves.items() if indx > 32}
        self.lines = [self.down_left_line, self.up_right_line, self.down_right_line, self.up_left_line]
        

class Rook(Queen):
    def __init__(self, color):
        super().__init__(color)
        self.char_identifier = "r"
        self.possible_moves = {indx: move for indx, move in self.possible_moves.items() if indx <= 32}
        self.lines = [self.down_line, self.up_line, self.right_line, self.left_line]