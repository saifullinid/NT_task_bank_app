import pytest

from tests.utility_class import UtilityClass


@pytest.fixture()
def start_end_fixture():
    tests_utility = UtilityClass()
    tests_utility.start_app()
    yield tests_utility
    tests_utility.client_del()
    tests_utility.stop_app()


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_UniqueClientNameException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    result = tests_utility.client_reg()
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            'Repeat for confirmation: \n'\
                            '<ERROR>: client named <something_name> already exists\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_ClientNotFoundException(start_end_fixture):
    tests_utility = start_end_fixture

    result = tests_utility.client_del()
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<ERROR>: client with this <something_name> not found\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_IncorrectPasswordException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    result = tests_utility.client_del(password='123456789')
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<ERROR>: incorrect password for client <something_name>\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_NegativeBalanceException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    tests_utility.deposit(1000)
    result = tests_utility.withdraw(2000)
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<ERROR>: transaction canceled: negative balance <-1000.00> is not allowed\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_NegativeOrNullAmountException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    result = tests_utility.deposit(-1000)
    assert result.exit_code == 0
    assert result.output == '<ERROR>: transaction canceled: amount should be > 0.\n'\
                            f'Amount entered <{-1000}>\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_AmountFormatException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    result = tests_utility.deposit('23423.568')
    assert result.exit_code == 0
    assert result.output == '<ERROR>: incorrect amount format, should be <0000.00> or <0000>\n'\
                            'Amount entered <23423.568>\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_bank_app_DateFormatException(start_end_fixture):
    tests_utility = start_end_fixture

    tests_utility.client_reg()
    result = tests_utility.show_bank_st('2020-01-02 00:00:00', '2023-01-02')
    assert result.exit_code == 0
    assert result.output == '<ERROR>: incorrect date format <2023-01-02>, should be YYYY-MM-DD HH:MM:SS\n'


def test_bank_app_AppNotStartedException():
    tests_utility = UtilityClass()

    result = tests_utility.client_reg()
    assert result.exit_code == 0
    assert result.output == '<ERROR>: app not started\n'


if __name__ == '__main__':
    test_bank_app_UniqueClientNameException()
    test_bank_app_ClientNotFoundException()
    test_bank_app_IncorrectPasswordException()
    test_bank_app_NegativeBalanceException()
    test_bank_app_NegativeOrNullAmountException()
    test_bank_app_DateFormatException()
    test_bank_app_AppNotStartedException()
