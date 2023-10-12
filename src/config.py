"""
Loading a token for a bot from environment
variables and token for a payment system
"""
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_FOR_BOT')
TOKEN_UPAY = os.getenv('TOKEN_FOR_UPAY')
