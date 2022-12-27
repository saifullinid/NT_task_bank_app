import sys
from datetime import datetime
from decimal import Decimal

from werkzeug.security import generate_password_hash, check_password_hash

from app.service.output import table_output_bank_statement
from app.custom_exc.custom_exc import UniqueClientNameException, ClientNotFoundException, \
    IncorrectPasswordException, NegativeBalanceException, DateFormatException, AppNotStartedException
from app.db.db_service import DBService


class Service:
    @staticmethod
    def check_state():
        db_service = DBService()
        try:
            db_service.get_state()
        except AppNotStartedException as exc:
            print(exc)
            sys.exit()
        finally:
            db_service.connect.close()

    @staticmethod
    def set_app_start_state():
        db_service = DBService()
        db_service.set_start_state()

    @staticmethod
    def set_app_stop_state():
        db_service = DBService()
        db_service.set_stop_state()

    @staticmethod
    def get_client(client_name, db_service):
        client_id, client_name, password_hash = db_service.get_client(client_name)
        return client_id, client_name, password_hash

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(password_hash, password, username):
        if check_password_hash(password_hash, password):
            return True
        raise IncorrectPasswordException(username)

    @staticmethod
    def check_balance(balance):
        if balance < 0:
            raise NegativeBalanceException(balance)

    def registration_client_account(self, client_name, password):
        db_service = DBService()
        try:
            db_service.check_username(client_name)
            db_service.add_client(client_name, self.set_password(password))
            db_service.add_account(client_name)
        except UniqueClientNameException as exc:
            print(exc)
        finally:
            db_service.connect.close()

    def delete_client_account(self, client_name, password):
        db_service = DBService()
        try:
            client_id, client_name, password_hash = self.get_client(client_name, db_service)
            self.check_password(password_hash, password, client_name)
            db_service.delete_client(client_id)
        except ClientNotFoundException as exc:
            print(exc)
        except IncorrectPasswordException as exc:
            print(exc)
        finally:
            db_service.connect.close()

    def make_deposit(self, client_name, password, amount, description):
        db_service = DBService()
        try:
            date = datetime.now()

            client_id, client_name, password_hash = self.get_client(client_name, db_service)
            self.check_password(password_hash, password, client_name)

            balance = db_service.get_balance(client_id)
            amount = round(Decimal(amount), 2)
            new_balance = balance + amount
            db_service.add_transaction(client_id, date=date, description=description,
                                       deposits=amount, balance=new_balance,
                                       message='Deposit operation was successful')
        except ClientNotFoundException as exc:
            print(exc)
        except IncorrectPasswordException as exc:
            print(exc)
        except DateFormatException as exc:
            print(exc)
        finally:
            db_service.connect.close()

    def make_withdraw(self, client_name, password, amount, description):
        db_service = DBService()
        try:
            date = datetime.now()

            client_id, client_name, password_hash = self.get_client(client_name, db_service)
            self.check_password(password_hash, password, client_name)

            balance = db_service.get_balance(client_id)
            amount = round(Decimal(amount), 2)
            new_balance = balance - amount
            self.check_balance(new_balance)

            db_service.add_transaction(client_id, date=date, description=description,
                                       withdrawals=amount, balance=new_balance,
                                       message='Withdrawal operation was successful')
        except ClientNotFoundException as exc:
            print(exc)
        except IncorrectPasswordException as exc:
            print(exc)
        except DateFormatException as exc:
            print(exc)
        except NegativeBalanceException as exc:
            print(exc)
        finally:
            db_service.connect.close()

    def show_bank_statement(self, client_name, password, since, till):
        db_service = DBService()
        transactions_list = []
        prev_balance_row = None
        try:
            client_id, client_name, password_hash = self.get_client(client_name, db_service)
            self.check_password(password_hash, password, client_name)

            transactions_list = db_service.get_transactions_for_period(client_id, since, till)
            if transactions_list[0][0]:
                prev_balance = transactions_list[0][-1] \
                               - transactions_list[0][-2] \
                               + transactions_list[0][-3]

                prev_balance_row = ['', 'Previous balance', '', '', prev_balance]
                headers_row = ['date', 'description', 'withdrawals', 'deposits', 'balance']

                table_output_bank_statement(transactions_list, headers_row, prev_balance_row)
            else:
                print('<INFO>: no transactions found on these dates')
        except ClientNotFoundException as exc:
            print(exc)
        except IncorrectPasswordException as exc:
            print(exc)
        except DateFormatException as exc:
            print(exc)
        finally:
            db_service.connect.close()
        return transactions_list, prev_balance_row

    def clear_tables(self):
        db_service = DBService()
        db_service.clear_tables()
        db_service.connect.close()

# s = Service()
# s.make_deposit('Jack Daniels', 'password', 500, 'ATM deposit', date='2021-02-10 12:00:00')
# s.make_deposit('Jack Daniels', 'password', 200, 'ATM deposit', date='2021-02-15 12:00:00')
# s.make_deposit('Jack Daniels', 'password', 150, 'ATM deposit', date='2021-02-22 12:00:00')
# s.make_withdraw('Jack Daniels', 'password', 150, 'ATM withdrawals', date='2021-10-01 12:00:00')
# s.make_withdraw('Jack Daniels', 'password', 150, 'ATM withdrawals', date='2021-10-02 12:00:00')
# s.make_withdraw('Jack Daniels', 'password', 150, 'ATM withdrawals', date='2021-10-05 12:00:00')
#
# s.make_deposit('Jim Beam', 'password', 300, 'ATM deposit', date='2021-01-10 12:00:00')
# s.make_withdraw('Jim Beam', 'password', 250, 'ATM withdrawals', date='2021-05-01 12:00:00')
# s.make_deposit('Jim Beam', 'password', 600, 'ATM deposit', date='2021-06-15 12:00:00')
# s.make_deposit('Jim Beam', 'password', 450, 'ATM deposit', date='2021-08-22 12:00:00')
# s.make_withdraw('Jim Beam', 'password', 250, 'ATM withdrawals', date='2021-09-02 12:00:00')
# s.make_withdraw('Jim Beam', 'password', 150, 'ATM withdrawals', date='2021-10-05 12:00:00')
#
# s.make_deposit('Clan MacGregor', 'password', 1300, 'ATM deposit', date='2021-01-10 12:00:00')
# s.make_withdraw('Clan MacGregor', 'password', 1250, 'ATM withdrawals', date='2021-05-01 12:00:00')
# s.make_deposit('Clan MacGregor', 'password', 2600, 'ATM deposit', date='2021-06-15 12:00:00')
# s.make_deposit('Clan MacGregor', 'password', 5450, 'ATM deposit', date='2021-08-22 12:00:00')
# s.make_withdraw('Clan MacGregor', 'password', 1250, 'ATM withdrawals', date='2021-09-02 12:00:00')
# s.make_withdraw('Clan MacGregor', 'password', 1150, 'ATM withdrawals', date='2021-10-05 12:00:00')
# s.show_bank_statement_all()
# s.show_bank_statement('Clan MacGregor', 'password', '2019-06-14 12:00:00', '2022-11-06 12:00:00')
# s.make_withdraw('Clan MacGregor', 'password', 10000, 'ATM withdrawals', date='2021-11-05 12:00:00')
# s.registration_client_account('Johnnie Walker', 'password')
