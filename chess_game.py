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
from validate_url import Validate
from chess_login import ChessLogin
from player import Player

class Game():
    def __init__(self) -> None:
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        with open("login.json") as file:
            creds = json.load(file)
            self.username = creds['username']
            self.password = creds['password']

        self.browser = Chrome(options=options)
        self.browser.get("https://www.chess.com")
        if 'cookies.json' in os.listdir():
            self.loadCookies()
            self.browser.get("https://www.chess.com/login")
            if 'login' in self.browser.current_url:
                self.login()
        else:
            self.login()

    def saveCookies(self):
        # Get and store cookies after login
        cookies = self.browser.get_cookies()

        # Store cookies in a file
        with open('cookies.json', 'w') as file:
            file.write(json.dumps(cookies, indent=1))
        print('New Cookies saved successfully')

    def loadCookies(self):
        # Check if cookies file exists
        if 'cookies.json' in os.listdir():

            # Load cookies to a vaiable from a file
            with open('cookies.json', 'r') as file:
                cookies = json.load(file)

            # Set stored cookies to maintain the session
            for cookie in cookies:
                self.browser.add_cookie(cookie)
            print('Cookies successfully loaded')
        else:
            print('No cookies file found')
        
        self.browser.refresh() # Refresh Browser after login

    def login(self):

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "login")))

        home_page_login = self.browser.find_elements(By.CLASS_NAME, "login")
        home_page_login[1].click()

        login_email = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.ID, "username")))

        login_email.send_keys(self.username)

        login_password = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.ID, "password")))

        login_password.send_keys(self.password)

        login_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "login-space-top-large")))

        login_button.click()
        time.sleep(1)

        #Verify the login succeeded
        if not "www.chess.com/home" in self.browser.current_url:
            raise ValueError("Login failed! Please provide valid credentials")
        else:
            self.saveCookies()

        #WebDriverWait(self.browser, 10).until(
        #EC.presence_of_element_located((
        #    By.CLASS_NAME, "clock-player-turn")))
        #
        ##TODO REPLACE WITH element.get_dom_element()
        ##Creates 2 player objects: white and black
        #try: #Determines if the player is white or black based on if the board is flipped
        #    self.browser.find_element(By.CLASS_NAME, "flipped")
        #except selenium.common.exceptions.NoSuchElementException:
        #    self.player = Player(color="white", page_source=self.browser.page_source)
        #    self.opponent = Player(color="black", page_source=self.browser.page_source)
        #else:
        #    self.player = Player(color="black", page_source=self.browser.page_source)
        #    self.opponent = Player(color="white", page_source=self.browser.page_source)
        #finally:
        #    self.action_chains = ActionChains(self.browser)

    def _move_player(self):
        while self.player.is_turn(self.browser.page_source) == False:
            pass
        else:
            self.player.set_positions()

    def play_game(self):
        print("Hello!")












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