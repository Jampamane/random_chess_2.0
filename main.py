from player import Player
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
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
    print(f"{bcolors.WARNING}Letting the page load for 5 seconds.{bcolors.ENDC}")
    time.sleep(5)

    #Creates 2 player objects: white and black
    try: #Determines if the player is white or black based on if the board is flipped
        assert browser.find_element(By.CLASS_NAME, "flipped")
        player = Player("black", browser.page_source)
        opponent = Player("white", browser.page_source)
    except:
        player = Player("white", browser.page_source)
        opponent = Player("black", browser.page_source)
    finally:
        player()
        opponent()
        action_chains = ActionChains(browser)


    while True:
        if player.is_turn(browser.page_source) == True:
            opponent.check_for_move(browser.page_source)
            opponent.set_positions(browser.page_source, opponent.alive_pieces())
            player.set_positions(browser.page_source, player.alive_pieces())
            time.sleep(1)
            player_moves = player.retrieve_non_check_moves(browser.page_source, opponent)
            if player_moves == None:
                print("Checkmate bro, you lose")
                return
            print(f"{player.username} has {bcolors.WARNING}{len(player_moves)}{bcolors.ENDC} available moves")
            random_piece, random_move = random.choice(player_moves)
            try:
                piece = browser.find_element(By.CLASS_NAME, f"piece.{player.color[0]}{random_piece.char_identifier}.square-{random_piece.board_position}")
            except:
                piece = browser.find_element(By.CLASS_NAME, f"piece.square-{random_piece.board_position}.{player.color[0]}{random_piece.char_identifier}")
            finally:
                piece.click()
                try:
                    square = browser.find_element(By.CLASS_NAME, f"hint.square-{random_move}")
                except:
                    square = browser.find_element(By.CLASS_NAME, f"capture-hint.square-{random_move}")
                finally: 
                    action_chains.drag_and_drop(piece, square).perform()
                    time.sleep(1)
                    try:
                        player.check_for_move(browser.page_source)
                        player.set_positions(browser.page_source, player.alive_pieces())
                        opponent.set_positions(browser.page_source, opponent.alive_pieces())
                    except:
                        player.set_positions(browser.page_source, player.alive_pieces())
                        opponent.set_positions(browser.page_source, opponent.alive_pieces())


if __name__ == "__main__":
    #Establish the selenium browser
    print(f"{bcolors.WARNING}Establishing browser.{bcolors.ENDC}")
    options = ChromeOptions()
    options.add_argument("--headless") #Start the browser in headless mode
    options.add_argument("log-level=3") #So it doesn't spam the console with messages
    browser = Chrome(options=options)
    browser.get("https://www.chess.com/")

    #Login to www.chess.com
    print(f"{bcolors.WARNING}Attempting to login.{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    time.sleep(1)
    home_page_login = browser.find_elements(By.CLASS_NAME, "login")
    home_page_login[1].click()
    print(f"{bcolors.WARNING}Redirected to the login page.{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    time.sleep(1)
    login_email = browser.find_element(By.CLASS_NAME, "login-email")
    login_email.send_keys(ChessLogin.username)
    login_password = browser.find_element(By.CLASS_NAME, "login-password")
    login_password.send_keys(ChessLogin.password)
    login_button = browser.find_element(By.CLASS_NAME, "login-space-top-large")
    login_button.click()
    print(f"{bcolors.WARNING}Credentials submitted.{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    time.sleep(1)
    try:
        assert "home" in browser.current_url
        print(f"{bcolors.OKGREEN}Login successful!{bcolors.ENDC}")
    except:
        print(f"{bcolors.FAIL}LOGIN FAILED{bcolors.ENDC}")
        quit()

    
    while True:
        main(browser)
        continue_ = input("Would you like to play again? (y/n) ")
        if continue_.lower() == "y" or continue_.lower() == "yes":
            main(browser)
        elif continue_.lower() == "n" or continue_.lower() == "no":
            quit()