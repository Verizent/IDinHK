import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("CURRENCY_TOKEN")

def checkCurrency():
    response = requests.get(TOKEN)
    return response.json()
