from click.testing import CliRunner
from app.bank import bank_app


class UtilityClass:
    def __init__(self):
        self.runner = CliRunner()

    def start_app(self):
        self.runner.invoke(
            bank_app,
            ['start', ]
        )

    def stop_app(self):
        self.runner.invoke(
            bank_app,
            ['stop', ]
        )

    def client_reg(self, client_name='something_name', password='password'):
        result = self.runner.invoke(
            bank_app,
            ['client-registration', '--client', client_name],
            input='\n'.join([password, password])
        )
        return result

    def client_del(self, client_name='something_name', password='password\n'):
        result = self.runner.invoke(
            bank_app,
            ['client-delete', '--client', client_name],
            input=password
        )
        return result

    def deposit(self, amount, client_name='something_name', password='password\n'):
        result = self.runner.invoke(
            bank_app,
            ['deposit',
             '--client', client_name,
             '--amount', amount,
             '--description', 'ATM deposit'],
            input=password
        )
        return result

    def withdraw(self, amount, client_name='something_name', password='password\n'):
        result = self.runner.invoke(
            bank_app,
            ['withdraw',
             '--client', client_name,
             '--amount', amount,
             '--description', 'ATM withdraw'],
            input=password
        )
        return result

    def show_bank_st(self, since, till, client_name='something_name', password='password\n'):
        result = self.runner.invoke(
            bank_app,
            ['show-bank-statement',
             '--client', client_name,
             '--since', since,
             '--till', till],
            input=password
        )
        return result
