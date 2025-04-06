import colorama
import os
from dotenv import load_dotenv

from utils import generate_response, welcome_message
from api import start_api

if __name__ == "__main__":
    colorama.init(autoreset=True)
    print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + welcome_message())

    load_dotenv()
    start_api()
