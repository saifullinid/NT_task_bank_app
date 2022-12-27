from datetime import datetime

from app.custom_exc.custom_exc import AmountFormatException, NegativeOrNullAmountException, DateFormatException


def check_amount_format(amount):
    try:
        fl_amount = float(amount)
    except ValueError:
        raise AmountFormatException(amount)
    if round(fl_amount, 2) != fl_amount:
        raise AmountFormatException(amount)
    if fl_amount <= 0:
        raise NegativeOrNullAmountException(amount)


def check_date_format(date):
    try:
        datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if len(date) != 19:
            raise ValueError
    except ValueError:
        raise DateFormatException(date)
