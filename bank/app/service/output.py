from datetime import datetime

from prettytable import PrettyTable


def table_output_bank_statement(input_list, headers_row, first_row):
    bank_statement = PrettyTable()
    bank_statement.field_names = headers_row

    bank_statement.custom_format['date'] = lambda column, value:\
        '' if not value else f'{datetime.strftime(value, "%Y-%m-%d %H:%M:%S")}'
    bank_statement.custom_format['withdrawals'] = lambda column, value:\
        '' if not value else f'${value}'
    bank_statement.custom_format['deposits'] = lambda column,  value:\
        '' if not value else f'${value}'
    bank_statement.custom_format['balance'] = lambda column, value: f'${value}'

    bank_statement.align['description'] = 'l'
    bank_statement.align['withdrawals'] = 'r'
    bank_statement.align['deposits'] = 'r'
    bank_statement.align['balance'] = 'r'

    bank_statement.add_row(first_row)
    bank_statement.add_rows(input_list)

    print(bank_statement)
