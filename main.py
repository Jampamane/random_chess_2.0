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

def login():
    #Login to www.chess.com
    browser.get("https://www.chess.com/")
    console.print("Navigating to the login page...")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "login")))
    
    home_page_login = browser.find_elements(By.CLASS_NAME, "login")
    home_page_login[1].click()

    console.print("Redirected to the login page...")
    console.print("Attempting to login...")

    login_email = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.ID, "username")))
    
    login_email.send_keys(ChessLogin.username)

    login_password = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.ID, "password")))
    
    login_password.send_keys(ChessLogin.password)

    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "login-space-top-large")))
    
    login_button.click()

    console.print("[green]Credentials submitted![/]")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "home-username-link")))
    
    #Verify the login succeeded
    if "www.chess.com/home" in browser.current_url:
        print(f"{ByteColors.OKGREEN}Login successful!{ByteColors.ENDC}")
    else:
        print(f"{ByteColors.FAIL}LOGIN FAILED{ByteColors.ENDC}")
        SystemExit()

def create_table(name):
    table = Table(title=name)

    table.add_column("White # of moves")
    table.add_column("White actual move")
    table.add_column("White time left")
    table.add_column("Black # of moves")
    table.add_column("Black actual move")
    table.add_column("Black time left")

    return table
def main():
    '''
    Main function. Connects to the chess game and runs the
    main loop to play the chess game. Returns once there are
    no more moves.
    '''
    
    table = create_table("Chess Game")
    console.print(table)

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
        
    
    with Live(table) as live:
        while True:
            if player.is_turn(browser.page_source) is True:
                if player.color == "white":
                    if player.has_moved(browser.page_source) is True:
                        opponent_move_piece = opponent.check_for_move(browser.page_source)
                        opponent.set_positions(browser.page_source, opponent.alive_pieces())
                        player.set_positions(browser.page_source, player.alive_pieces())
                        opponent.print_last_move(browser.page_source, opponent_move_piece)
                elif player.color == "black":
                    if opponent.has_moved(browser.page_source) is False:
                        opponent_moves = opponent.retrieve_non_check_moves(browser.page_source, player)
                        while opponent.has_moved(browser.page_source) is False:
                            pass
                        opponent_move_piece = opponent.check_for_move(browser.page_source)
                    else:
                        opponent_move_piece = opponent.check_for_move(browser.page_source)
                    opponent.set_positions(browser.page_source, opponent.alive_pieces())
                    player.set_positions(browser.page_source, player.alive_pieces())
                    opponent.print_last_move(browser.page_source, opponent_move_piece)
                player_moves = player.retrieve_non_check_moves(browser.page_source, opponent)
                if player_moves is None:
                    page = BeautifulSoup(browser.page_source, "html.parser")
                    selected_move = page.find(class_ = f"{opponent.color} node selected")
                    if selected_move.text[-1] == "#":
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
                        piece.click()
                        break
                    except:
                        try:
                            piece = browser.find_element(
                                By.CLASS_NAME, 
                                f"piece.square-{random_piece.board_position}"
                                f".{player.color[0]}{random_piece.char_identifier}")
                            piece.click()
                        except:
                            pass
                while True:
                    try:
                        square = browser.find_element(By.CLASS_NAME, f"hint.square-{random_move}")
                        action_chains.drag_and_drop(piece, square).perform()
                        break
                    except:
                        try:
                            square = browser.find_element(By.CLASS_NAME, f"capture-hint.square-{random_move}")
                            action_chains.drag_and_drop(piece, square).perform()
                            break
                        except:
                            pass
                player.set_positions(browser.page_source, player.alive_pieces())
                opponent.set_positions(browser.page_source, opponent.alive_pieces())
                player.print_last_move(browser.page_source, random_piece)
                opponent_moves = opponent.retrieve_non_check_moves(browser.page_source, player)
                if opponent_moves is None:
                    console.print("GAME OVER", style="green")
                    console.print("YOU WIN?", style="green")
                    return
            
            live.update(str(len(player_moves)),
                        str(random_move),
                        "Potato",
                        str(len(opponent_moves)),
                        str(opponent_move_piece),
                        "tomato")
            


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

    with console.status(
    "Setting up...", spinner="material",
    ):
        options = ChromeOptions()
        options.add_argument("--headless") #Run in headless mode
        options.add_argument("log-level=3") #So it doesn't spam the console with messages
        browser = Chrome(options=options) #Establish the selenium browser

        #login()
        time.sleep(0.5)
        console.print("Accessing chess game url...")
        browser.get(args.url) #Connect to the current game being played
        console.print("Letting the page load...")
        time.sleep(3)
    
    with console.status(
    "[blue]Playing chess...", spinner="dots",
    ):
        main()