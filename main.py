import pyautogui
import keyboard
import winsound
from player import Player
import random
import queen
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from bcolors import bcolors
from selenium.webdriver import Chrome
from validate_url import Validate
from selenium.webdriver.chrome.options import Options as ChromeOptions
from chess_login import ChessLogin


def main(browser):
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

    for piece in player.alive_pieces(): #This is a change hey look a change
        all_the_pieces = player.create_dict(browser.page_source, sort_color=False)
        potential_moves = piece.get_potential_moves()
        on_the_board = piece.on_the_board(potential_moves)
        collision = piece.detect_collisions(on_the_board, all_the_pieces)
        final_moves = piece.final_moves(on_the_board, collision)
        print(f"{bcolors.WARNING}{str(piece)}'s potential moves: {potential_moves}{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}{str(piece)}'s on the board moves: {on_the_board}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}{str(piece)}'s detected collisions: {collision}{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}{str(piece)}'s final moves: {final_moves}{bcolors.ENDC}")


'''
    while True:
        if player.is_turn(browser.page_source) == True:
            opponent_move = opponent.check_for_move(browser.page_source)
            if opponent_move == "capture":
                opponent.set_positions(browser.page_source, opponent.alive_pieces())
                player.set_positions(browser.page_source, player.alive_pieces())
            elif opponent_move == "checkmate":
                print("gameover man")
                quit()
            elif opponent_move == "lose":
                print("gameover man")
                quit()
            elif opponent_move == "win":
                print("wow you won")
                quit()
            elif opponent_move == True:
                opponent.set_positions(browser.page_source, opponent.alive_pieces())
            elif opponent_move == False:
                pass

        if opponent.is_turn(browser.page_source) == True:
            player_move = player.check_for_move(browser.page_source)
            if player_move == "capture":
                player.set_positions(browser.page_source, player.alive_pieces())
                opponent.set_positions(browser.page_source, opponent.alive_pieces())
            elif player_move == "checkmate":
                print("you win!")
                quit()
            elif player_move == "lose":
                print("gameover man")
                quit()
            elif player_move == "win":
                print("wow you won")
                quit()
            elif player_move == True:
                player.set_positions(browser.page_source, player.alive_pieces())
            elif player_move == False:
                pass
'''

if __name__ == "__main__":
    #Establish the selenium browser
    print(f"{bcolors.WARNING}Establishing browser.{bcolors.ENDC}")
    options = ChromeOptions()
    options.add_argument("--headless") #Start the browser in headless mode
    options.add_argument("log-level=3") #So it doesn't spam the console with messages
    browser = Chrome(options=options)
    browser.get("https://www.chess.com/")

    #Login to www.chess.com
    #print(f"{bcolors.WARNING}Attempting to login.{bcolors.ENDC}")
    #print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    #time.sleep(1)
    #home_page_login = browser.find_elements(By.CLASS_NAME, "login")
    #home_page_login[1].click()
    #print(f"{bcolors.WARNING}Redirected to the login page.{bcolors.ENDC}")
    #print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    #time.sleep(1)
    #login_email = browser.find_element(By.CLASS_NAME, "login-email")
    #login_email.send_keys(ChessLogin.username)
    #login_password = browser.find_element(By.CLASS_NAME, "login-password")
    #login_password.send_keys(ChessLogin.password)
    #login_button = browser.find_element(By.CLASS_NAME, "login-space-top-large")
    #login_button.click()
    #print(f"{bcolors.WARNING}Credentials submitted.{bcolors.ENDC}")
    #print(f"{bcolors.WARNING}Letting the page load for 1 second.{bcolors.ENDC}")
    #time.sleep(1)
    #try:
    #    assert "home" in browser.current_url
    #    print(f"{bcolors.OKGREEN}Login successful!{bcolors.ENDC}")
    #except:
    #    print(f"{bcolors.FAIL}LOGIN FAILED{bcolors.ENDC}")
    #    quit()

    #Connect to the current game being played
    #url = input(f"{bcolors.HEADER}Please enter the url for the chess game: {bcolors.ENDC}") 
    url = f"https://www.chess.com/game/live/104885610928?username={ChessLogin.username}"
    while not Validate(url, "www.chess.com").success():
        url = input(f"{bcolors.HEADER}Please enter a valid url: {bcolors.ENDC}")
    browser.get(url)
    print(f"{bcolors.WARNING}Letting the page load for 3 seconds.{bcolors.ENDC}")
    time.sleep(3)
    main(browser)