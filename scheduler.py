"""
This is a scheduler. It's need for run script periodically(Daily).
"""
import schedule
from time import sleep
from task import get_currency_exchange
from config import params

schedule.every().day.at("23:55").do(get_currency_exchange, **params)

while True:
    schedule.run_pending()
    sleep(60)
