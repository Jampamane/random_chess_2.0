import pieces
import piece_potential_moves
import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from rich.table import Table
from rich.console import Console
from player import White
from player import Black

def create_table(page_source, player, opponent):
    table = Table()
    table.add_column("White move")
    table.add_column("Black move")
    soup = BeautifulSoup(page_source, "html.parser")
    move_list = soup.find("wc-move-list")
    moves = move_list.find_all(class_="move-list-row")
    for move in moves:
        try:
            white_move = move.find(class_="white-move").text.strip()
        except AttributeError:
            white_move = ""
        try:
            black_move = move.find(class_="black-move").text.strip()
        except AttributeError:
            black_move = ""
        table.add_row(white_move, black_move)
    return table

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = Chrome(options=options)
browser.get("https://www.chess.com/game/live/104974826636?username=jampamane")

player = White()
opponent = Black()
table = create_table(browser.page_source, player, opponent)
console = Console()
console.print(table)