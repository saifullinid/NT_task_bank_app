class CustomException(Exception):
    pass


class UniqueClientNameException(CustomException):
    def __init__(self, username):
        self.message = f'client named <{username}> already exists'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class ClientNotFoundException(CustomException):
    def __init__(self, username):
        self.message = f'client with this <{username}> not found'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class IncorrectPasswordException(CustomException):
    def __init__(self, username):
        self.message = f'incorrect password for client <{username}>'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class NegativeBalanceException(CustomException):
    def __init__(self, balance):
        self.message = f'transaction canceled: negative balance <{balance:.2f}> is not allowed'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class NegativeOrNullAmountException(CustomException):
    def __init__(self, amount):
        self.message = f'transaction canceled: amount should be > 0.\nAmount entered <{amount}>'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class AmountFormatException(CustomException):
    def __init__(self, amount: object) -> object:
        self.message = f'incorrect amount format, should be <0000.00> or <0000>\nAmount entered <{amount}>'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class DateFormatException(CustomException):
    def __init__(self, date):
        self.message = f'incorrect date format <{date}>, should be YYYY-MM-DD HH:MM:SS'

    def __str__(self):
        return f'<ERROR>: {self.message}'


class AppNotStartedException(CustomException):
    def __init__(self):
        self.message = f'app not started'

    def __str__(self):
        return f'<ERROR>: {self.message}'
