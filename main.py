import random
import time
from bs4 import BeautifulSoup
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
def main(browser):
    '''
    Main function. Connects to the chess game and runs the
    main loop to play the chess game. Returns once there are
    no more moves.
    '''
    #Connect to the current game being played
    url = input(f"{ByteColors.HEADER}Please enter the url for the chess game: {ByteColors.ENDC}") 
    while not Validate(url, "www.chess.com").success():
        url = input(f"{ByteColors.HEADER}Please enter a valid url: {ByteColors.ENDC}")
    browser.get(url)
    WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "board")))
    #Creates 2 player objects: white and black
    try: #Determines if the player is white or black based on if the board is flipped
        WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "flipped")))
        player = Player("black", browser.page_source)
        opponent = Player("white", browser.page_source)
        player()
        opponent()
    except:
        player = Player("white", browser.page_source)
        opponent = Player("black", browser.page_source)
        player()
        opponent()
    finally:
        action_chains = ActionChains(browser)
    while True:
        if player.is_turn(browser.page_source) == True:
            if player.color == "white":
                if player.has_moved(browser.page_source) == False:
                    pass
                else:
                    opponent_move_piece = opponent.check_for_move(browser.page_source)
                    opponent.set_positions(browser.page_source, opponent.alive_pieces())
                    player.set_positions(browser.page_source, player.alive_pieces())
                    opponent.print_last_move(browser.page_source, opponent_move_piece)
            elif player.color == "black":
                if opponent.has_moved(browser.page_source) == False:
                    opponent_moves = opponent.retrieve_non_check_moves(browser.page_source, player)
                    print(f"{opponent.username} has {ByteColors.WARNING}{len(opponent_moves)}{ByteColors.ENDC} available moves")
                    while opponent.has_moved(browser.page_source) == False:
                        pass
                    opponent_move_piece = opponent.check_for_move(browser.page_source)
                else:
                    opponent_move_piece = opponent.check_for_move(browser.page_source)
                opponent.set_positions(browser.page_source, opponent.alive_pieces())
                player.set_positions(browser.page_source, player.alive_pieces())
                opponent.print_last_move(browser.page_source, opponent_move_piece)
            player_moves = player.retrieve_non_check_moves(browser.page_source, opponent)
            if player_moves == None:
                page = BeautifulSoup(browser.page_source, "html.parser")
                selected_move = page.find(class_ = f"{opponent.color} node selected")
                if selected_move.text[-1] == "#":
                    print(f"{ByteColors.FAIL}GAME OVER{ByteColors.ENDC}")
                    print(f"{ByteColors.FAIL}CHECKMATE{ByteColors.ENDC}")
                else:
                    print(f"{ByteColors.FAIL}GAME OVER{ByteColors.ENDC}")
                    print(f"{ByteColors.WARNING}STALEMATE{ByteColors.ENDC}")
                return
            print(f"{player.username.center(25, '-')} has {ByteColors.WARNING}{str(len(player_moves)).center(2)}{ByteColors.ENDC} available moves between {ByteColors.OKGREEN}{str(len(player.alive_pieces())).center(2)}{ByteColors.ENDC} pieces")
            random_piece, random_move = random.choice(player_moves)
            while True:
                try:
                    piece = browser.find_element(By.CLASS_NAME, f"piece.{player.color[0]}{random_piece.char_identifier}.square-{random_piece.board_position}")
                    piece.click()
                    break
                except:
                    try:
                        piece = browser.find_element(By.CLASS_NAME, f"piece.square-{random_piece.board_position}.{player.color[0]}{random_piece.char_identifier}")
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
                print(f"{ByteColors.OKGREEN}GAME OVER{ByteColors.ENDC}")
                print(f"{ByteColors.OKGREEN}YOU WIN?{ByteColors.ENDC}")
                return
            print(f"{opponent.username.center(25, '-')} has {ByteColors.WARNING}{str(len(opponent_moves)).center(2)}{ByteColors.ENDC} available moves between {ByteColors.OKGREEN}{str(len(opponent.alive_pieces())).center(2)}{ByteColors.ENDC} pieces")
            
if __name__ == "__main__":
    #Establish the selenium browser
    print(f"{ByteColors.WARNING}Establishing browser.{ByteColors.ENDC}")
    options = ChromeOptions()
    options.add_argument("log-level=3") #So it doesn't spam the console with messages
    browser = Chrome(options=options)

    #Login to www.chess.com
    browser.get("https://www.chess.com/")
    print(f"{ByteColors.WARNING}Attempting to login.{ByteColors.ENDC}")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "login")))
    home_page_login = browser.find_elements(By.CLASS_NAME, "login")
    home_page_login[1].click()
    print(f"{ByteColors.WARNING}Redirected to the login page.{ByteColors.ENDC}")
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
    print(f"{ByteColors.WARNING}Credentials submitted.{ByteColors.ENDC}")
    home_username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "home-username-link")))
    #Verify the login succeeded
    try:
        assert "www.chess.com/home" in browser.current_url
        print(f"{ByteColors.OKGREEN}Login successful!{ByteColors.ENDC}")
    except:
        print(f"{ByteColors.FAIL}LOGIN FAILED{ByteColors.ENDC}")
        SystemExit()
    try:
        main(browser)
    except KeyboardInterrupt:
        print(f"{ByteColors.FAIL}GAME ENDED UBRUPTLY{ByteColors.ENDC}")
    main(browser)
    while True:
        try:
            continue_ = input(f"{ByteColors.HEADER}Would you like to play again?{ByteColors.ENDC} (y/n) ")
            if continue_.lower() == "y" or continue_.lower() == "yes":
                main(browser)
            elif continue_.lower() == "n" or continue_.lower() == "no":
                SystemExit()
        except KeyboardInterrupt:
            print(f"{ByteColors.FAIL}GAME ENDED UBRUPTLY{ByteColors.ENDC}")

