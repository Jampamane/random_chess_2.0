from player import Player
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bcolors import bcolors
from selenium.webdriver import Chrome
from validate_url import Validate
from selenium.webdriver.chrome.options import Options as ChromeOptions
from chess_login import ChessLogin



def main(browser):
    #Connect to the current game being played
    url = input(f"{bcolors.HEADER}Please enter the url for the chess game: {bcolors.ENDC}") 
    while not Validate(url, "www.chess.com").success():
        url = input(f"{bcolors.HEADER}Please enter a valid url: {bcolors.ENDC}")
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
                    print(f"{opponent.username} has {bcolors.WARNING}{len(opponent_moves)}{bcolors.ENDC} available moves")
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
                    print(f"{bcolors.FAIL}GAME OVER{bcolors.ENDC}")
                    print(f"{bcolors.FAIL}CHECKMATE{bcolors.ENDC}")
                else:
                    print(f"{bcolors.FAIL}GAME OVER{bcolors.ENDC}")
                    print(f"{bcolors.WARNING}STALEMATE{bcolors.ENDC}")
                return
            print(f"{player.username.center(25, '-')} has {bcolors.WARNING}{str(len(player_moves)).center(2)}{bcolors.ENDC} available moves between {bcolors.OKGREEN}{str(len(player.alive_pieces())).center(2)}{bcolors.ENDC} pieces")
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
            if opponent_moves == None:
                print(f"{bcolors.OKGREEN}GAME OVER{bcolors.ENDC}")
                print(f"{bcolors.OKGREEN}YOU WIN?{bcolors.ENDC}")
                return
            print(f"{opponent.username.center(25, '-')} has {bcolors.WARNING}{str(len(opponent_moves)).center(2)}{bcolors.ENDC} available moves between {bcolors.OKGREEN}{str(len(opponent.alive_pieces())).center(2)}{bcolors.ENDC} pieces")


if __name__ == "__main__":
    #Establish the selenium browser
    print(f"{bcolors.WARNING}Establishing browser.{bcolors.ENDC}")
    options = ChromeOptions()
    options.add_argument("log-level=1") #So it doesn't spam the console with messages
    browser = Chrome(options=options)

    #Login to www.chess.com
    browser.get("https://www.chess.com/")
    print(f"{bcolors.WARNING}Attempting to login.{bcolors.ENDC}")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "login")))
    home_page_login = browser.find_elements(By.CLASS_NAME, "login")
    home_page_login[1].click()
    print(f"{bcolors.WARNING}Redirected to the login page.{bcolors.ENDC}")
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
    print(f"{bcolors.WARNING}Credentials submitted.{bcolors.ENDC}")
    home_username = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "home-username-link")))
    
    #Verify the login succeeded
    try:
        assert "www.chess.com/home" in browser.current_url
        print(f"{bcolors.OKGREEN}Login successful!{bcolors.ENDC}")
    except:
        print(f"{bcolors.FAIL}LOGIN FAILED{bcolors.ENDC}")
        quit()

    try:
        main(browser)
    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}GAME ENDED UBRUPTLY{bcolors.ENDC}")
    
    main(browser)
    while True:
        try:
            continue_ = input(f"{bcolors.HEADER}Would you like to play again?{bcolors.ENDC} (y/n) ")
            if continue_.lower() == "y" or continue_.lower() == "yes":
                main(browser)
            elif continue_.lower() == "n" or continue_.lower() == "no":
                quit()
        except KeyboardInterrupt:
            print(f"{bcolors.FAIL}GAME ENDED UBRUPTLY{bcolors.ENDC}")