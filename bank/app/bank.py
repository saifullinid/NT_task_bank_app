import click

from app.cli.client_delete import client_delete
from app.cli.client_registration import client_registration
from app.cli.deposit import deposit
from app.cli.show_bank_statement import show_bank_statement
from app.cli.withdraw import withdraw
from app.service.service import Service


@click.group()
def bank_app():
    pass


@bank_app.command()
def start():
    try:
        service = Service()
        service.set_app_start_state()
    except Exception as exc:
        print(f'<UNEXPECTED ERROR>: {exc}')


@bank_app.command()
def stop():
    try:
        service = Service()
        service.set_app_stop_state()
        service.clear_tables()
    except Exception as exc:
        print(f'<UNEXPECTED ERROR>: {exc}')


bank_app.add_command(client_registration)
bank_app.add_command(client_delete)
bank_app.add_command(deposit)
bank_app.add_command(withdraw)
bank_app.add_command(show_bank_statement)

if __name__ == '__main__':
    bank_app()
