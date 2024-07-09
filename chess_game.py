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
from rich.layout import Layout
from rich.panel import Panel
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from validate_url import Validate
from player import Player
from pieces import Piece

class Game():


    ABSOLUTE_PATH = os.path.dirname(__file__)
    LOGIN_RELATIVE_PATH = "login.json"
    COOKIES_RELATIVE_PATH = "cookies.json"
    LOGIN_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, LOGIN_RELATIVE_PATH)
    COOKIES_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, COOKIES_RELATIVE_PATH)


    def __init__(self, headless=False) -> None:
        self.console = Console()
        with self.console.status("Setting up chess..."):
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
            self.action_chains = ActionChains(self.browser)
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


    def _get_soupy_pieces(self) -> list[str]:
        positions = []
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        board = soup.find("wc-chess-board")
        divs = board.find_all("div")
        for position in divs:
            try:
                if "piece" in str(position).lower():
                    positions.append(str(position))
            except AttributeError:
                pass
        return positions


    def _is_game_over(self) -> bool:
        try:
            self.browser.find_element(By.CLASS_NAME, "result-row")
        except NoSuchElementException:
            return False
        return True


    def _update_positions(self, player: Player, opponent: Player) -> None:
        pieces = self._get_soupy_pieces()
        player.set_positions(pieces=pieces)
        opponent.set_positions(pieces=pieces)
        player.retrieve_non_check_moves(pieces=pieces, opponent=opponent)
        opponent.retrieve_non_check_moves(pieces=pieces, opponent=player)



    def _move_piece(self, piece: Piece, move: str, opponent: Player) -> None:
        p = None
        square = None
        try:
            p = self.browser.find_element(
                By.CLASS_NAME,
                f"piece.{piece.color[0]}{piece.char_identifier}"
                f".square-{piece.board_position}")
        except NoSuchElementException:
            p = self.browser.find_element(
                By.CLASS_NAME,
                f"piece.square-{piece.board_position}"
                f".{piece.color[0]}{piece.char_identifier}")
        finally:
            p.click()

        try:
            opponent.piece_positions[move]
        except KeyError:
            square = self.browser.find_element(
                By.CLASS_NAME, f"hint.square-{move}")
        else:
            square = self.browser.find_element(
                By.CLASS_NAME, f"capture-hint.square-{move}")
        finally:
            self.action_chains.drag_and_drop(p, square).perform()
            piece.set_position(position=move)


    def _create_chess_table(self, player: Player, opponent: Player) -> Table:
        chess_board = {}
        emoji = {"p": "P",
                 "n": "N",
                 "r": "R",
                 "b": "B",
                 "k": "K",
                 "q": "Q"}
        for x in range(1, 9):
            for y in range(1, 9):
                pos = str(f"{x}{y}")
                try:
                    p = player.piece_positions[pos]
                    chess_board[pos] = (emoji[p[1]], "green bold")
                except KeyError:
                    try:
                        o = opponent.piece_positions[pos]
                        chess_board[pos] = (emoji[o[1]], "red bold")
                    except KeyError:
                        chess_board[pos] = ("  ", "white")

        table = Table(title="Chess Game", show_header=False)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)
        table.add_column(justify="center", width=2)

        if player.color == "white":
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
        elif player.color == "black":
            for z in range(1, 9):
                table.add_row(
                    f"[{chess_board[str(f'8{z}')][1]}]{chess_board[str(f'8{z}')][0]}",
                    f"[{chess_board[str(f'7{z}')][1]}]{chess_board[str(f'7{z}')][0]}",
                    f"[{chess_board[str(f'6{z}')][1]}]{chess_board[str(f'6{z}')][0]}",
                    f"[{chess_board[str(f'5{z}')][1]}]{chess_board[str(f'5{z}')][0]}",
                    f"[{chess_board[str(f'4{z}')][1]}]{chess_board[str(f'4{z}')][0]}",
                    f"[{chess_board[str(f'3{z}')][1]}]{chess_board[str(f'3{z}')][0]}",
                    f"[{chess_board[str(f'2{z}')][1]}]{chess_board[str(f'2{z}')][0]}",
                    f"[{chess_board[str(f'1{z}')][1]}]{chess_board[str(f'1{z}')][0]}"
                    )
                table.add_section()

        top_player = Table(show_header=False, show_lines=False, show_edge=False)
        top_string = self.browser.find_elements(By.CLASS_NAME, "player-component")[0].text.replace("\n", " ").upper()
        top_player.add_row(f"[red bold]{top_string}")
        top_player.add_section()
        top_player.add_row(str(opponent.potential_moves))
        top_player.add_section()
        top_player.add_row(f"Total moves: [cyan bold]{len(opponent.potential_moves)}")
        bottom_player = Table(show_header=False, show_lines=False, show_edge=False)
        bottom_string = self.browser.find_elements(By.CLASS_NAME, "player-component")[1].text.replace("\n", " ").upper()
        bottom_player.add_row(f"[green bold]{bottom_string}")
        bottom_player.add_section()
        bottom_player.add_row(str(player.potential_moves))
        bottom_player.add_section()
        bottom_player.add_row(f"Total moves: [cyan bold]{len(player.potential_moves)}")

        layout = Layout()
        layout.split_row(
            Layout(name="table"),
            Layout(name="info")
        )
        layout["info"].split_column(
            Layout(name="top_player"),
            Layout(name="bottom_player")
        )
        layout["table"].size = 50
        layout["table"].update(Panel(table))
        layout["top_player"].update(Panel(top_player))
        layout["bottom_player"].update(Panel(bottom_player))
        return layout


    def _fetch_result(self, player_color: str) -> bool:
        result_dict = {
            "white": 0,
            "black": 0
        }
        result = self.browser.find_element(By.CLASS_NAME, "result-row").text
        result = result.split("-")
        result_dict["white"] = int(result[0])
        result_dict["black"] = int(result[1])

        if result_dict[player_color] == 1:
            return True
        if result_dict[player_color] == 0:
            return False
        return None


    def play_game(self, game_type: str="1 min") -> None:
        self._start_game(game_type=game_type)

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
        self.action_chains = ActionChains(self.browser)
        with Live(self._create_chess_table(player=player, opponent=opponent)) as live:
            while self._is_game_over() is False:
                if player.is_turn(self.browser) is True:
                    self._update_positions(player=player, opponent=opponent)
                    live.update(self._create_chess_table(player=player, opponent=opponent))
                    player_moves = player.retrieve_non_check_moves(pieces=self._get_soupy_pieces(), opponent=opponent)
                    assert len(player_moves) != 0
                    random_piece, random_move = random.choice(player_moves)
                    self._move_piece(piece=random_piece, move=random_move, opponent=opponent)
                    self._update_positions(player=player, opponent=opponent)
                live.update(self._create_chess_table(player=player, opponent=opponent))
            self._update_positions(player=player, opponent=opponent)
            live.update(self._create_chess_table(player=player, opponent=opponent))

        results = self._fetch_result(player_color=player.color)
        if results is True:
            self.console.print("[green bold]You win!", justify="center")
        elif results is False:
            self.console.print("[red bold]You lose!", justify="center")
        elif results is None:
            self.console.print("[yellow bold]Draw!", justify="center")
