from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChessLogin():
    '''
    Hey this is my login to chess.com. Don't use it. It's mine.
    '''
    def __init__(self):
        self.username = "jampamane"
        self.password = "NhHfCg8Gi7qLXnd9696?Qob#ejPzARMjMm!B$6Ed"

    def login(self, browser, console):
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

        login_email.send_keys(self.username)

        login_password = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                By.ID, "password")))

        login_password.send_keys(self.password)

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
            console.print("Login successful!", style="green")
        else:
            console.print("LOGIN FAILED", style="red")
            quit()
