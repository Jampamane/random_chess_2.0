from pieces import Pawn
from pieces import Knight
from pieces import Rook
from pieces import Bishop
from pieces import King
from pieces import Queen
from bs4 import BeautifulSoup
from bcolors import bcolors

class Player():
    def __init__(self, color, page_source):
        self.color = color
        if self.color == "white":
            self.text_color = bcolors.OKCYAN
        elif self.color == "black":
            self.text_color = bcolors.OKBLUE
        self.username = f"{self.text_color}{self.set_username(page_source).upper()}{bcolors.ENDC}"
        self.time_left = self.set_time(page_source)
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
        self.pieces = [self.pawn1, self.pawn2, self.pawn3, self.pawn4, self.pawn5, self.pawn6, self.pawn7, self.pawn8,
                       self.rook1, self.rook2, self.kight1, self.kight2, self.bishop1, self.bishop2, self.king, self.queen]
        self.set_positions(page_source, self.pieces)

    def __call__(self) -> None:
        print(f"{self.username} is {self.text_color}{self.color.upper()}{bcolors.ENDC} and they have {bcolors.FAIL}{self.time_left}{bcolors.ENDC} left on the clock")
        print(f"{self.username} has {bcolors.WARNING}{len(self.alive_pieces())}{bcolors.ENDC} pieces left on the board \n")

    def create_dict(self, page_source, sort_color = True) -> dict:
        '''
        Reads the browser's HTML and creates a dictionary with piece and location information.
        '''
        piece_dict = {}
        page = BeautifulSoup(page_source, "html.parser")
        board = page.find("wc-chess-board")
        positions = board.find_all("div", lambda text: "piece" in text.lower())
        pieces = [str(piece) for piece in positions]
        for piece in pieces: #Selects each div compenent that was turned into text

            replaced = piece.replace("\"", "") #Deletes the quotation marks
            split = replaced.split() #Splits the div text component into individual values
           
            for text in split:  #Iterates over each individual value
                try:
                    assert len(text) == 2 #Test to see if the value is a 2 character piece identifier
                    if sort_color == True:
                        try:
                            assert self.color[0] == text[0] #Test to see if it's the correct color (white or black)
                        except: #If not correct color set both to None and break
                            current_piece = None
                            current_position = None
                            break
                    current_piece = text
                except:
                    pass

                try:
                    assert int(text[-2:]) #Test to see if the last 2 characters can be cast to an int
                    current_position = text[-2:]
                except:
                    pass
            
            if current_position and current_piece: #Update dictionary only if correct color
                piece_dict[current_position] = current_piece

        return piece_dict

    def set_positions(self, page_source, piece_list) -> None:
        '''
        Calls the create_dict function to create a dictionary with piece and location information.
        Uses that information to set the initial position of each piece.
        '''
        dict_ = self.create_dict(page_source).items()
        piece_list_copy = [piece for piece in piece_list]
        for position, piece in dict_:
            for player_piece in piece_list_copy:
                if piece[-1] == player_piece.char_identifier:
                    player_piece.set_position(position)
                    piece_list_copy.remove(player_piece)
                    break

        if len(piece_list_copy): #If there is still a piece left in piece_list, it wasn't found in the HTML and it must be dead
            for piece in piece_list_copy:
                piece.board_position = "00"

    def set_attribute(self, page_source, class_name) -> str:
        '''
        A bit of repeat logic in figuring out which attribute to set when there are exactly 2 attributes.
        For example, 2 usernames, 2 clocks.
        '''
        page = BeautifulSoup(page_source, "html.parser")
        attributes = page.find_all(class_=class_name)
        attribute = ""
        try:
            assert page.find(class_="flipped")
            if self.color == "black":
                attribute = attributes[1].get_text()
            elif self.color == "white":
                attribute = attributes[0].get_text()
        except:
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
    
    def alive_pieces(self) -> list:
        pieces = [piece for piece in self.pieces if piece.board_position != "00"]
        return pieces
    
    def is_turn(self, page_source) -> bool:
        page = BeautifulSoup(page_source, "html.parser")
        if page.find(class_=f"{self.color} node selected") == None:
            return True
        else:
            return False

    def is_check(self, move):
        if "+" in str(move):
            print(f"{bcolors.WARNING}{'CHECK'.center(25, '-')}{bcolors.ENDC}")
            return True
        else:
            return False
        
    def is_capture(self, move):
        if "x" in str(move):
            print(f"{bcolors.WARNING}{'CAPTURE'.center(25, '-')}{bcolors.ENDC}")
            return True
        else:
            return False
        
    def is_checkmate(self, move):
        if "#" in str(move):
            print(f"{bcolors.FAIL}{'CHECKMATE'.center(25, '-')}{bcolors.ENDC}")
            return True
        else:
            return False
        
    def is_game_over(self, page_source):
        page = BeautifulSoup(page_source, "html.parser")
        if page.find(class_="white game-result") != None:
            if self.color == "white":
                print(f"{bcolors.OKGREEN}{'YOU WIN'.center(25, '-')}{bcolors.ENDC}")
                return "win"
            else:
                print(f"{bcolors.FAIL}{'YOU LOSE'.center(25, '-')}{bcolors.ENDC}")
                return "lose"
        elif page.find(class_="black game-result") != None:
            if self.color == "black":
                print(f"{bcolors.OKGREEN}{'YOU WIN'.center(25, '-')}{bcolors.ENDC}")
                return "win"
            else:
                print(f"{bcolors.FAIL}{'YOU LOSE'.center(25, '-')}{bcolors.ENDC}")
                return "lose"
        else:
            return False

    def check_for_move(self, page_source) -> bool:
        piece_dict = self.create_dict(page_source)
        piece_list = self.alive_pieces()
        for piece in piece_list:
            try:
                piece_dict[piece.board_position]
            except:
                if str(piece) == "Pawn":
                    if (self.color == "white" and int(piece.board_position[1]) == 7) or (self.color == "black" and int(piece.board_position[1]) == 2):
                        self.pieces.remove(piece)
                        piece = Queen(self.color)
                        self.pieces.append(piece)
                page = BeautifulSoup(page_source, "html.parser")
                move = page.find(class_=f"{self.color} node selected")
                print(f"{self.username} moved their {self.text_color}{str(piece).upper()}{bcolors.ENDC} to {self.text_color}{move.text.upper()}{bcolors.ENDC}")
                return True
        return False
        
    
    def retrieve_final_moves(self, page_source, all_pieces = None):
        piece_list = self.alive_pieces()
        final_moves = []
        if not all_pieces:
            all_pieces = self.create_dict(page_source, sort_color=False)
        for piece in piece_list:
            moves = piece.return_final_moves(all_pieces)
            try:
                for move in moves:
                    final_moves.append(move)
            except:
                pass
        return final_moves

    def retrieve_non_check_moves(self, page_source, opponent):
        player_potential_moves = self.retrieve_final_moves(page_source)
        all_the_pieces = self.create_dict(page_source, sort_color=False)
        non_check_moves = []
        for piece, move in player_potential_moves:
            all_the_pieces.pop(piece.board_position)
            all_the_pieces[move] = f"{self.color[0]}{piece.char_identifier}"
            opponent_moves = {move: "Value don't matter" for piece, move in opponent.retrieve_final_moves(page_source, all_the_pieces)}
            try:
                if str(piece) == "King":
                    opponent_moves[move]
                else:
                    opponent_moves[self.king.board_position]
            except:
                non_check_moves.append((piece, move))
            finally:
                all_the_pieces.pop(move)
                all_the_pieces[piece.board_position] = f"{self.color[0]}{piece.char_identifier}"
        if len(non_check_moves) == 0:
            return None
        else:
            return non_check_moves