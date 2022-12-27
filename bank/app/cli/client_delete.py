import click

from app.service.service import Service


@click.command()
@click.option('--client', type=str)
def client_delete(client):
    try:
        service = Service()
        service.check_state()

        password = click.prompt('Please enter a password', type=str, hide_input=True)
        service.delete_client_account(client, password)
    except Exception as exc:
        print(f'<UNEXPECTED ERROR>: {exc}')
