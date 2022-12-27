import click

from app.cli.validations import check_amount_format
from app.custom_exc.custom_exc import AmountFormatException, NegativeOrNullAmountException
from app.service.service import Service


@click.command()
@click.option('--client', type=str)
@click.option('--amount', type=str)
@click.option('--description', type=str)
def deposit(client, amount, description):
    try:
        check_amount_format(amount)

        service = Service()
        service.check_state()

        password = click.prompt('Please enter a password', type=str, hide_input=True)
        service.make_deposit(client, password, amount, description)
    except AmountFormatException as exc:
        print(exc)
    except NegativeOrNullAmountException as exc:
        print(exc)
    except Exception as exc:
        print(f'<UNEXPECTED ERROR>: {exc}')
