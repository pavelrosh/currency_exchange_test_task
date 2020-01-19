"""
This is a config file.
What for?

For set up logger, environment variables reader, needed for project,
variables and parameters.
"""
from environs import Env
import logging


def get_logger(log_format='%(asctime)s %(levelname)-8s %(message)s',
               log_name='', log_file_info='action.log', log_file_error='error.log'):
    """
    Function for set up custom logger. In this case custom mean writing errors and actions
    in detached files.
    """

    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    file_handler_info = logging.FileHandler(log_file_info, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(log_file_error, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)
    log.setLevel(logging.INFO)
    return log

# initialisation logger
logger = get_logger()

# setting up and read environmental variables
env = Env()
env.read_env()
KEY = env('KEY')

# Variables needed for access to API.
EXCHANGE_SITE_URL = 'https://free.currconv.com/'
EXCHANGE_API_ROUTE = 'api/v7/convert?q={}&compact=ultra&apiKey={}'

# Here you can set different currencies.
params = {'main_currency': 'USD', 'currencies': ('EUR', 'GBP', 'UAH')}
