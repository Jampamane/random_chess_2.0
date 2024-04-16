import random
from argparse import ArgumentParser
import time
import selenium
from bs4 import BeautifulSoup
import rich
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
from bcolors import ByteColors
from player import Player
from validate_url import Validate
from chess_login import ChessLogin



def main():
    '''
    Main function. Connects to the chess game and runs the
    main loop to play the chess game. Returns once there are
    no more moves.
    '''

    #Creates 2 player objects: white and black
    try: #Determines if the player is white or black based on if the board is flipped
        browser.find_element(By.CLASS_NAME, "flipped")
    except selenium.common.exceptions.NoSuchElementException:
        player = Player("white", browser.page_source)
        opponent = Player("black", browser.page_source)
    else:
        player = Player("black", browser.page_source)
        opponent = Player("white", browser.page_source)
    finally:
        action_chains = ActionChains(browser)
        
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
            



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-url")
    args = parser.parse_args()
    console = Console()
    try:
        if not args.url:
            raise ValueError("Chess game requires a url.")
        if Validate(args.url, "www.chess.com").success() is False:
            raise ReferenceError("Chess game requires a valid url.")
    except ValueError as e:
        console.print(e, style="red")
        console.print("Type -url and then the url for the chess game.", style="red")
        quit()
    except ReferenceError as e:
        console.print(e, style="red")
        quit()

    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    browser = Chrome(options=options) #Establish the selenium browser

    with console.status(
    "Setting up...", spinner="material",
    ):
        ChessLogin().login(browser, console)
        time.sleep(0.5)
        console.print("Accessing chess game url...")
        browser.get(args.url) #Connect to the current game being played
        console.print("Letting the page load...")
        WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "clock-player-turn")))
    
    with console.status(
    "[blue]Playing chess...", spinner="dots",
    ):
        main()