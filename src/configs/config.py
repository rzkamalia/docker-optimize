import os

from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]