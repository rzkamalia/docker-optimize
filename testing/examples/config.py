import os

from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]