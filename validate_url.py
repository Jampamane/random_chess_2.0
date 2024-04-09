import requests

class Validate():
    '''
    This is just to validate that the url is actually a good url and not a bad one.
    Bad url. Bad bad boy.
    '''
    def __init__(self, url = "", test_url = False) -> None:
        '''
        Once the class initializes it validates the url.
        '''
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        try:
            response = requests.get(url, timeout=10)
            if not response:
                raise requests.exceptions.ConnectionError
            if test_url:
                assert test_url in url, f"Are you connecting to {test_url}?"
            self.successful = True
        except requests.exceptions.SSLError:
            errormessage = "Are you connecting to an actual URL?"
            print(f"{FAIL}{'INVALID URL'.center(len(errormessage), '-')}")
            print(f"{'TIMEOUT MAX RETRIES'.center(len(errormessage), '-')}{ENDC}")
            print(f"{WARNING}{errormessage.center(len(errormessage), '-')}{ENDC}")
            self.successful = False
        except requests.exceptions.ConnectionError:
            errormessage = "Response code for the url is 400 or higher."
            print(f"{FAIL}{'INVALID URL'.center(len(errormessage), '-')}")
            print(f"{'FAILED TO CONNECT'.center(len(errormessage), '-')}{ENDC}")
            print(f"{WARNING}{errormessage.center(len(errormessage), '-')}{ENDC}")
            self.successful = False
        except requests.exceptions.MissingSchema:
            errormessage = "Are you missing https:// at the beggining of the url?"
            print(f"{FAIL}{'INVALID URL'.center(len(errormessage), '-')}")
            print(f"{'MISSING SCHEMA'.center(len(errormessage), '-')}{ENDC}")
            print(f"{WARNING}{errormessage.center(len(errormessage), '-')}{ENDC}")
            self.successful = False
        except AssertionError as e:
            errormessage = str(e)
            print(f"{FAIL}{'INVALID URL'.center(len(errormessage), '-')}")
            print(f"{'INVALID WEBSITE'.center(len(errormessage), '-')}{ENDC}")
            print(f"{WARNING}{errormessage.center(len(errormessage), '-')}{ENDC}")
            self.successful = False
    def success(self) -> bool:
        '''
        Returns if the validation was successful or not.
        Good url. Good good boy.
        '''
        return self.successful
    
