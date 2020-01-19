"""
This is file with base logic.
Here two functions for getting and saving exchange rate data.
"""

import requests
from json import dumps
from datetime import date
from config import EXCHANGE_API_ROUTE, EXCHANGE_SITE_URL, KEY, logger


def check_if_currencies_exist(currencies_to_check: tuple = ('EUR', 'GBP', 'UAH')):
    """
    This function is needed for checking input parameters(currencies),
    it's mean that if you try to put wrong currency name parameters, you will get a error.
    ex. 'UAH', 'USD' - right currencies, 'LOLOL' - wrong one.

    Logic:
        - Create link to API route that will return all available currencies.
        - Make a request within created link and save new data.
        - Check if request and data is ok.
        - Check if all given currencies are in list that we got from API.
        - If so return True, else an error and False.
    """
    url = EXCHANGE_SITE_URL + "api/v7/currencies?apiKey=" + KEY
    all_currencies = requests.get(url=url)
    if all_currencies.status_code == 200:
        all_currencies = all_currencies.json()
        all_currencies = [k for k, _ in all_currencies['results'].items()]
        result = all(currency in all_currencies for currency in currencies_to_check)
        return result
    else:
        logger.error(f"Can't access to next API route {url}")


def get_currency_exchange(main_currency: str = 'USD', currencies: tuple = ('EUR', 'GBP', 'UAH')):
    """
    This function is needed for getting rate and save it in file.
    Logic:
        - Check if input currencies are ok.
        - If so, create url for future request to API.
        - Request this url, if response is ok save data as json.
        - Save this json in file with name of current date. ex.: exchange_rate_history/2020-01-19
    """
    if check_if_currencies_exist((main_currency, )) and check_if_currencies_exist(currencies):
        logger.info("Checked currencies successfully!")
        currencies = ([main_currency + '_' + c for c in currencies]
                      + [c + '_' + main_currency for c in currencies])
        url = EXCHANGE_SITE_URL + EXCHANGE_API_ROUTE.format(','.join(currencies), KEY)
        response = requests.get(url=url)

        if response.status_code == 200:
            data = response.json()
            with open('exchange_rate_history/' + str(date.today()), 'w+') as f:
                f.write(dumps(data))
            logger.info(f"Rate for today({str(date.today())}) was wrote successfully!")
        else:
            logger.error(f"Some error while requesting next API route {url}, status code: {res.status_code}")
    else:
        logger.error('Wrong input currency!')
