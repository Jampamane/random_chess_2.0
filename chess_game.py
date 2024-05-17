import random
from argparse import ArgumentParser
import time
import selenium
from bs4 import BeautifulSoup
import rich
import os
import json
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.live import Live
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from validate_url import Validate
from player import Player

class Game():


    ABSOLUTE_PATH = os.path.dirname(__file__)
    LOGIN_RELATIVE_PATH = "login.json"
    COOKIES_RELATIVE_PATH = "cookies.json"
    LOGIN_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, LOGIN_RELATIVE_PATH)
    COOKIES_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, COOKIES_RELATIVE_PATH)


    def __init__(self, headless=False) -> None:
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        if headless is True:
            options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        with open(self.LOGIN_ABSOLUTE_PATH, "r", encoding="utf-8") as file:
            creds = json.load(file)
            self.username = creds['username']
            self.password = creds['password']

        self.browser = Chrome(options=options)
        self.browser.get("https://www.chess.com")
        if os.path.exists(self.COOKIES_ABSOLUTE_PATH):
            self._load_cookies()
            self.browser.get("https://www.chess.com/login")
            if 'login' in self.browser.current_url:
                self._login()
        else:
            self._login()


    def _save_cookies(self):
        # Get and store cookies after login
        cookies = self.browser.get_cookies()

        # Store cookies in a file
        with open(self.COOKIES_ABSOLUTE_PATH, 'w', encoding="utf-8") as file:
            file.write(json.dumps(cookies, indent=1))
        print('New Cookies saved successfully')


    def _load_cookies(self):
        # Load cookies to a vaiable from a file
        with open(self.COOKIES_ABSOLUTE_PATH, 'r', encoding="utf-8") as file:
            cookies = json.load(file)
        # Set stored cookies to maintain the session
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        print('Cookies successfully loaded')

        self.browser.refresh() # Refresh Browser after login


    def _login(self):
        self.browser.get("https://www.chess.com/login")

        login_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "login-space-top-large")))

        input_fields = self.browser.find_elements(By.CLASS_NAME, "cc-input-component")
        for field in input_fields:
            if field.get_attribute("aria-label") == "Username or Email":
                field.send_keys(self.username)
            elif field.get_attribute("aria-label") == "Password":
                field.send_keys(self.password)

        login_button.click()
        time.sleep(1)

        #Verify the login succeeded
        if not "www.chess.com/home" in self.browser.current_url:
            raise ValueError("Login failed! Please provide valid credentials")
        self._save_cookies()


    def _start_game(self, game_type: str) -> None:
        if game_type not in ["1 min", "3 min", "5 min", "10 min", "30 min"]:
            raise ValueError("Please provide a valid game type.")
        self.browser.get("https://www.chess.com/play/online")
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "selector-button-button"))
                ).click()
        time.sleep(1)
        

        buttons = self.browser.find_elements(By.CLASS_NAME, "time-selector-button-button")
        for button in buttons:
            if button.text == game_type:
                button.click()
                break

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME,
                "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full"))
                ).click()

        WebDriverWait(self.browser, 20).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "clock-player-turn")))


    def _is_game_over(self) -> bool:
        try:
            self.browser.find_element(By.CLASS_NAME, "result-row")
        except NoSuchElementException:
            return False
        return True

    def _update_positions(self, player: Player, opponent: Player) -> None:
        player.set_positions(browser=self.browser)
        opponent.set_positions(browser=self.browser)

    def _move_piece(self, piece, move):
        action_chain = ActionChains(self.browser)

        while True:
            try:
                p = self.browser.find_element(
                    By.CLASS_NAME,
                    f"piece.{piece.color[0]}{piece.char_identifier}"
                    f".square-{piece.board_position}")
            except NoSuchElementException:
                pass
            else:
                break
            try:
                p = self.browser.find_element(
                    By.CLASS_NAME, 
                    f"piece.square-{piece.board_position}"
                    f".{piece.color[0]}{piece.char_identifier}")
            except NoSuchElementException:
                pass
            else:
                break

        p.click()

        while True:
            try:
                square = self.browser.find_element(
                    By.CLASS_NAME, f"hint.square-{move}")
            except NoSuchElementException:
                pass
            else:
                break
            try:
                square = self.browser.find_element(
                    By.CLASS_NAME, f"capture-hint.square-{move}")
            except NoSuchElementException:
                pass
            else:
                break

        action_chain.drag_and_drop(p, square).perform()

    def _create_chess_table(self, player: Player, opponent: Player) -> Table:
        chess_board = {}
        for x in range(1, 9):
            for y in range(1, 9):
                pos = str(f"{x}{y}")
                try:
                    p = player.piece_positions[pos]
                    chess_board[pos] = (p[1].upper(), "green bold")
                except KeyError:
                    try:
                        o = opponent.piece_positions[pos]
                        chess_board[pos] = (o[1].upper(), "red bold")
                    except KeyError:
                        chess_board[pos] = (" ", "white")
                    
        table = Table(title="Chess Game")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")

        for z in reversed(range(1, 9)):
            table.add_row(
                f"[{chess_board[str(f'1{z}')][1]}]{chess_board[str(f'1{z}')][0]}",
                f"[{chess_board[str(f'2{z}')][1]}]{chess_board[str(f'2{z}')][0]}",
                f"[{chess_board[str(f'3{z}')][1]}]{chess_board[str(f'3{z}')][0]}",
                f"[{chess_board[str(f'4{z}')][1]}]{chess_board[str(f'4{z}')][0]}",
                f"[{chess_board[str(f'5{z}')][1]}]{chess_board[str(f'5{z}')][0]}",
                f"[{chess_board[str(f'6{z}')][1]}]{chess_board[str(f'6{z}')][0]}",
                f"[{chess_board[str(f'7{z}')][1]}]{chess_board[str(f'7{z}')][0]}",
                f"[{chess_board[str(f'8{z}')][1]}]{chess_board[str(f'8{z}')][0]}"
                )
            table.add_section()
        return table

    def play_game(self, game_type: str="1 min"):
        #self._start_game(game_type=game_type)
        self.browser.get("https://www.chess.com/game/live/107290000534?username=jampamane")
        WebDriverWait(self.browser, 20).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "clock-player-turn")))
        time.sleep(1)
        #Creates 2 player objects: white and black
        try: #Determines if the player is white or black based on if the board is flipped
            self.browser.find_element(By.CLASS_NAME, "board.flipped")
        except NoSuchElementException:
            player = Player(color="white")
            opponent = Player(color="black")
        else:
            player = Player(color="black")
            opponent = Player(color="white")
        self._update_positions(player=player, opponent=opponent)
        t = self._create_chess_table(player=player, opponent=opponent)
        console = Console()
        console.print(t)


        #while self._is_game_over() is False:
        #    if player.is_turn(self.browser) is True:
        #        self._update_positions(player=player, opponent=opponent)
        #        player_moves = player.retrieve_non_check_moves(self.browser, opponent)
        #        random_piece, random_move = random.choice(player_moves)
        #        self._move_piece(piece=random_piece, move=random_move)
        #        self._update_positions(player=player, opponent=opponent)















    # XX if black, check for move
    # XX calculate total moves
    # XX pick random move
    # XX move the piece
    # XX wait for enemy to move
    
    #This is the main function for v1 of random chess bot.
    """
    def main():
    #Calls the color class to create a player object and an enemy object of the appropriate color
    PlayerCol = color()
    a = chess.Player("Player", PlayerCol)
    if PlayerCol == "black":
        b = chess.Player("Opponent", "white")
        b.determineEnemyMove(a.getPiecePositions(), b.getPiecePositions(), a.pieceList)
    else:
        b = chess.Player("Opponent", "black")
    findPiece(a.pieceList, a.getPiecePositions(), b.getPiecePositions(), b.pieceList)
    a.updatePieceList()
    while True:
        if keyboard.is_pressed("p"):
            quit()
        if keyboard.is_pressed("l"):
            b.determineEnemyMove(a.getPiecePositions(), b.getPiecePositions(), a.pieceList)
            findPiece(a.pieceList, a.getPiecePositions(), b.getPiecePositions(), b.pieceList)
            a.updatePieceList()
        if a.turn() == True:
            b.determineEnemyMove(a.getPiecePositions(), b.getPiecePositions(), a.pieceList)
            findPiece(a.pieceList, a.getPiecePositions(), b.getPiecePositions(), b.pieceList)
            a.updatePieceList()
    """

    # This is the previous main function that became super long and complicated
    '''
    while True:
        if player.is_turn(browser.page_source) is True:
            player_moves = player.retrieve_non_check_moves(browser.page_source, opponent)
            if player_moves is None:
                page = BeautifulSoup(browser.page_source, "html.parser")
                selected_move = page.find(class_ = f"{opponent.color} node selected")
                if "#" in str(selected_move.text):
                    console.print("GAME OVER", style="red")
                    console.print("CHECKMATE", style="red")
                else:
                    console.print("GAME OVER", style="red")
                    console.print("STALEMATE", style="red")
                return
            random_piece, random_move = random.choice(player_moves)
            while True:
                try:
                    piece = browser.find_element(
                        By.CLASS_NAME,
                        f"piece.{player.color[0]}{random_piece.char_identifier}"
                        f".square-{random_piece.board_position}")
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                else:
                    piece.click()
                    break
                try:
                    piece = browser.find_element(
                        By.CLASS_NAME, 
                        f"piece.square-{random_piece.board_position}"
                        f".{player.color[0]}{random_piece.char_identifier}")
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                else:
                    piece.click()
                    break
            while True:
                try:
                    square = browser.find_element(By.CLASS_NAME, f"hint.square-{random_move}")
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                else:
                    action_chains.drag_and_drop(piece, square).perform()
                    break
                try:
                    square = browser.find_element(By.CLASS_NAME, f"capture-hint.square-{random_move}")
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                else:
                    action_chains.drag_and_drop(piece, square).perform()
                    break

            player.set_positions(browser.page_source, player.alive_pieces())
            opponent.set_positions(browser.page_source, opponent.alive_pieces())
            player.print_last_move(browser.page_source, random_piece)
            opponent_moves = opponent.retrieve_non_check_moves(browser.page_source, player)
            if opponent_moves is None:
                console.print("GAME OVER", style="green")
                console.print("YOU WIN?", style="green")
                return
            '''