from datetime import datetime

import pytest

from app.service.service import Service
from tests.utility_class import UtilityClass


@pytest.fixture(autouse=True)
def start_end_fixture():
    tests_utility = UtilityClass()
    tests_utility.start_app()
    yield tests_utility
    tests_utility.client_del()
    tests_utility.stop_app()


@pytest.mark.usefixtures('start_end_fixture')
def test_client_registration(start_end_fixture):
    tests_utility = start_end_fixture

    result = tests_utility.client_reg()
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            'Repeat for confirmation: \n'\
                            '<INFO>: New client created successfully\n'\
                            '<INFO>: New account created successfully\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_client_delete(start_end_fixture):
    tests_utility = start_end_fixture
    tests_utility.client_reg()

    result = tests_utility.client_del()
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<INFO>: Client account delete successfully\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_deposit(start_end_fixture):
    tests_utility = start_end_fixture
    tests_utility.client_reg()

    result = tests_utility.deposit(1000)
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<INFO>: Deposit operation was successful\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_withdraw(start_end_fixture):
    tests_utility = start_end_fixture
    tests_utility.client_reg()
    tests_utility.deposit(10000)

    result = tests_utility.withdraw(1000)
    assert result.exit_code == 0
    assert result.output == 'Please enter a password: \n'\
                            '<INFO>: Withdrawal operation was successful\n'


@pytest.mark.usefixtures('start_end_fixture')
def test_show_bank_st(start_end_fixture):
    exp_prev_balance_row = ['', 'Previous balance', '', '', '30000.00']
    exp_data = [
        ['ATM deposit', '0.00', '10000.00', '40000.00'],
        ['ATM withdraw', '5000.00', '0.00', '35000.00'],
        ['ATM deposit', '0.00', '20000.00', '55000.00'],
        ['ATM withdraw', '10000.00', '0.00', '45000.00'],
        ['ATM deposit', '0.00', '5000.50', '50000.50'],
        ['ATM withdraw', '500.00', '0.00', '49500.50']
    ]
    exp_total_row = ['Totals', '15500.00', '35000.50', '49500.50']

    tests_utility = start_end_fixture
    tests_utility.client_reg()

    tests_utility.deposit(30000)

    since_date = datetime.now()

    for index, data in enumerate(exp_data):
        if index % 2 == 0:
            tests_utility.deposit(float(data[2]))
        else:
            tests_utility.withdraw(float(data[1]))

    till_date = datetime.now()

    service = Service()
    transactions_list, prev_balance_row = service.show_bank_statement(
        'something_name', 'password', since_date, till_date
    )

    for index, data in enumerate(prev_balance_row):
        assert str(data) == str(exp_prev_balance_row[index])

    for index, data in enumerate(transactions_list[:-1]):
        for sub_index, sub_data in enumerate(data[1:]):
            assert str(sub_data) == str(exp_data[index][sub_index])

    for index, data in enumerate(transactions_list[-1][1:]):
        assert str(data) == str(exp_total_row[index])


if __name__ == '__main__':
    test_client_registration()
    test_client_delete()
    test_deposit()
    test_withdraw()
    test_show_bank_st()

