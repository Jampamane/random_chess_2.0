import requests
from bcolors import ByteColors

class Validate():
    '''
    This is just to validate that the url is actually a good url and not a bad one.
    Bad url. Bad bad boy.
    '''
    def __init__(self, url = "", test_url = False) -> None:
        '''
        The class initializes and validates the url.
        '''
        try:
            response = requests.get(url, timeout=10)
            if not response:
                raise requests.exceptions.ConnectionError
            if test_url:
                assert test_url in url, f"Are you connecting to {test_url}?"
            self.successful = True
        except requests.exceptions.SSLError:
            err_msg = "Are you connecting to an actual URL?"
            print(f"{ByteColors.FAIL}{'INVALID URL'.center(len(err_msg), '-')}")
            print(f"{'TIMEOUT MAX RETRIES'.center(len(err_msg), '-')}{ByteColors.ENDC}")
            print(f"{ByteColors.WARNING}{err_msg.center(len(err_msg), '-')}{ByteColors.ENDC}")
            self.successful = False
        except requests.exceptions.ConnectionError:
            err_msg = "Response code for the url is 400 or higher."
            print(f"{ByteColors.FAIL}{'INVALID URL'.center(len(err_msg), '-')}")
            print(f"{'FAILED TO CONNECT'.center(len(err_msg), '-')}{ByteColors.ENDC}")
            print(f"{ByteColors.WARNING}{err_msg.center(len(err_msg), '-')}{ByteColors.ENDC}")
            self.successful = False
        except requests.exceptions.MissingSchema:
            err_msg = "Are you missing https:// at the beggining of the url?"
            print(f"{ByteColors.FAIL}{'INVALID URL'.center(len(err_msg), '-')}")
            print(f"{'MISSING SCHEMA'.center(len(err_msg), '-')}{ByteColors.ENDC}")
            print(f"{ByteColors.WARNING}{err_msg.center(len(err_msg), '-')}{ByteColors.ENDC}")
            self.successful = False
        except AssertionError as e:
            err_msg = str(e)
            print(f"{ByteColors.FAIL}{'INVALID URL'.center(len(err_msg), '-')}")
            print(f"{'INVALID WEBSITE'.center(len(err_msg), '-')}{ByteColors.ENDC}")
            print(f"{ByteColors.WARNING}{err_msg.center(len(err_msg), '-')}{ByteColors.ENDC}")
            self.successful = False
    def success(self) -> bool:
        '''
        Returns if the validation was successful or not.
        Good url. Good good boy.
        '''
        return self.successful
