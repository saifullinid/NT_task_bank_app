import click

from app.cli.validations import check_date_format
from app.custom_exc.custom_exc import DateFormatException
from app.service.service import Service


@click.command()
@click.option('--client', type=str)
@click.option('--since', type=str)
@click.option('--till', type=str)
def show_bank_statement(client, since, till):
    try:
        check_date_format(since)
        check_date_format(till)

        service = Service()
        service.check_state()

        password = click.prompt('Please enter a password', type=str, hide_input=True)
        service.show_bank_statement(client, password, since, till)
    except DateFormatException as exc:
        print(exc)
    except Exception as exc:
        print(f'<UNEXPECTED ERROR>: {exc}')
