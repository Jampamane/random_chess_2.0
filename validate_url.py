
from typing import Any
import requests
from rich.console import Console


class Validate():
    '''
    This is just to validate that the url is actually a good url and not a bad one.
    Bad url. Bad bad boy.
    '''
    def __init__(self, url, test_url) -> None:
        '''
        The class initializes and validates the url.
        '''
        self.url = url
        self.test_url = test_url
        self.console = Console()
        try:
            response = requests.get(self.url)
            if not response: #If 400 or greater evaluates falsey
                raise requests.exceptions.ConnectionError
            if not self.test_url in self.url: 
                raise ValueError(f"Are you connecting to {self.test_url}?")
        except requests.exceptions.SSLError:
            self.console.print("INVALID URL", style="red")
            self.console.print("TIMEOUT MAX RETRIES", style="red")
            self.console.print("Are you connecting to an actual URL?", style="yellow")
            self.successful = False
        except requests.exceptions.ConnectionError:
            self.console.print("INVALID URL", style="red")
            self.console.print("FAILED TO CONNECT", style="red")
            self.console.print("Response code for the url is 400 or higher.", style="yellow")
            self.successful = False
        except requests.exceptions.MissingSchema:
            self.console.print("INVALID URL", style="red")
            self.console.print("MISSING SCHEMA", style="red")
            self.console.print("Are you missing https:// at the beggining of the url?", style="yellow")
            self.successful = False
        except ValueError as e:
            self.console.print("INVALID URL", style="red")
            self.console.print("INVALID WEBSITE", style="red")
            self.console.print(str(e), style="yellow")
            self.successful = False
        else:
            self.successful = True

    def success(self) -> bool:
        '''
        Returns if the validation was successful or not.
        Good url. Good good boy.
        '''
        return self.successful
