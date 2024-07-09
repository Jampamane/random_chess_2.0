"""Contains object that handles initialization, file creation, and web traversal."""
import time
import json
import os
from rich.console import Console
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class Traversal:
    """Handles initialization, file creation and web traversal."""

    ABSOLUTE_PATH = os.path.dirname(__file__)
    LOGIN_RELATIVE_PATH = "login.json"
    COOKIES_RELATIVE_PATH = "cookies.json"
    LOGIN_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, LOGIN_RELATIVE_PATH)
    COOKIES_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, COOKIES_RELATIVE_PATH)

    def __init__(self, headless=False) -> None:
        self.console = Console()
        self.console.print("Setting up chess...")
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        if headless is True:
            options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        self.console.print("Initializing browser...")
        self.browser = Chrome(options=options)
        self.console.print("Navigating to chess.com...")
        self.browser.get("https://www.chess.com")
        self.action_chains = ActionChains(self.browser)
        self.console.print("Searching for cookies...")
        cookies_loaded = False
        if os.path.exists(self.COOKIES_ABSOLUTE_PATH):
            self.console.print("Cookies found!", style = "green")
            self._load_cookies()
            self.browser.get("https://www.chess.com/login")
            time.sleep(1)
            if 'login' in self.browser.current_url:
                self.console.print("Cookies expired!", style = "red")
                if os.path.exists(self.LOGIN_ABSOLUTE_PATH):
                    self.console.print("Login credentials found!", style = "green")
                else:
                    self.console.print("Login credentials not found!", style = "red")
                    self._get_credentials()
            else:
                cookies_loaded = True
        else:
            self.console.print("Cookies not found!", style = "red")
            if os.path.exists(self.LOGIN_ABSOLUTE_PATH):
                self.console.print("Login credentials found!", style = "green")
            else:
                self.console.print("Login credentials not found!", style = "red")
                self._get_credentials()

        if cookies_loaded is False:
            while self._login() is False:
                self._get_credentials()


    def _save_cookies(self):
        # Get and store cookies after login
        self.console.print("Saving cookies...", style = "yellow")
        cookies = self.browser.get_cookies()

        # Store cookies in a file
        with open(self.COOKIES_ABSOLUTE_PATH, 'w', encoding="utf-8") as file:
            file.write(json.dumps(cookies, indent=1))
        self.console.print("New Cookies saved successfully!", style = "green")


    def _load_cookies(self):
        # Load cookies to a vaiable from a file
        self.console.print("Loading cookies...", style = "yellow")
        with open(self.COOKIES_ABSOLUTE_PATH, 'r', encoding="utf-8") as file:
            cookies = json.load(file)
        # Set stored cookies to maintain the session
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        self.console.print("Cookies successfully loaded!", style = "green")
        self.browser.refresh() # Refresh Browser after login


    def _get_credentials(self):
        username = input("Please provide your username: ")
        password = input("Please provide your password: ")
        credentials = {
            "username": username,
            "password": password
        }
        with open(self.LOGIN_ABSOLUTE_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(credentials))


    def _login(self) -> bool:
        self.console.print("Logging in...", style = "yellow")
        self.browser.get("https://www.chess.com/login")
        with open(self.LOGIN_ABSOLUTE_PATH, "r", encoding="utf-8") as file:
            creds = json.load(file)
            username = creds['username']
            password = creds['password']

        login_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, "login-space-top-large")))

        input_fields = self.browser.find_elements(By.CLASS_NAME, "cc-input-component")
        for field in input_fields:
            if field.get_attribute("aria-label") == "Username or Email":
                field.send_keys(username)
            elif field.get_attribute("aria-label") == "Password":
                field.send_keys(password)

        login_button.click()
        time.sleep(1)

        #Verify the login succeeded
        if not "www.chess.com/home" in self.browser.current_url:
            self.console.print("Login failed! Please provide valid credentials.", style = "red")
            return False
        self.console.print("Log in successful!", style = "green")
        self._save_cookies()
        return True


    def _start_game(self, game_type: str) -> None:
        self.console.print("Starting game...", style = "yellow")
        self.console.print(f"The game type you have chosen is {game_type}")
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
                "cc-button-component.cc-button-primary.cc-button-xx-large.cc-button-full"))
                ).click()

        self.console.print("Waiting for game to start...")

        WebDriverWait(self.browser, 20).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "clock-player-turn")))

        self.console.print("Game found!", style = "green")
