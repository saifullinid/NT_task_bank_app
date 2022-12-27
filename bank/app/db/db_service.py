from datetime import datetime

from psycopg2 import connect

from app.custom_exc.custom_exc import ClientNotFoundException, UniqueClientNameException, AppNotStartedException
from app.db import db_config


class DBService:
    def __init__(self):
        self.connect = connect(dbname=db_config.DBNAME,
                               user=db_config.USER,
                               password=db_config.PASSWORD,
                               host=db_config.HOST,
                               port=db_config.PORT,)

    def check_username(self, username):
        select_client = '''
            SELECT * FROM clients
            WHERE username = (%s);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_client, (username, ))
                if not cursor.fetchone():
                    return True
        raise UniqueClientNameException(username)

    def add_client(self, username, password):
        insert_client = '''
            INSERT INTO clients
            (username, password)
            VALUES (%s, %s);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_client, (username, password))
                print('<INFO>: New client created successfully')

    def add_account(self, username):
        insert_client = '''
           INSERT INTO transactions 
               (date, description, client_id)
               VALUES (%s, 'Creating account', (
                    SELECT clients.id
                        FROM clients
                        WHERE clients.username = (%s)
               ));
        '''

        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d %H:%M:%S')

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_client, (date, username))
                print('<INFO>: New account created successfully')

    def add_transaction(self, client_id, date, description='without description',
                        withdrawals=0, deposits=0, balance=0,
                        message='New account created successfully'):

        insert_transaction = '''
            INSERT INTO transactions
            (date, description, withdrawals, deposits, balance, client_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_transaction,
                               (date, description, withdrawals, deposits, balance, client_id))
                print(f'<INFO>: {message}')

    def get_client(self, username):
        select_client_id = '''
            SELECT * FROM clients
            WHERE username = (%s);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_client_id, (username, ))
                client = cursor.fetchone()
                if client:
                    return client
        raise ClientNotFoundException(username)

    def get_balance(self, client_id):
        select_balance = '''
            SELECT date, balance FROM transactions
            WHERE client_id = (%s)
            ORDER BY date DESC;
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_balance, (client_id, ))
                transaction = cursor.fetchone()
                balance = transaction[-1]
                return balance

    def get_transactions_for_period(self, client_id, since, till):
        # since_date = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
        # till_date = datetime.strptime(till, '%Y-%m-%d %H:%M:%S')
        if since > till:
            since, till = till, since
            print('<INFO> maybe you mixed up the dates, we changed them')

        select_transactions = '''
            SELECT date, description, withdrawals, deposits, balance
                FROM transactions
                WHERE client_id = (%s) AND transactions.date >= (%s) AND transactions.date <= (%s)
            UNION ALL
            SELECT
                NULL,
                'Totals',
                SUM(withdrawals),
                SUM(deposits),
                SUM(deposits) - SUM(withdrawals) + COALESCE((
                    SELECT COALESCE(balance, 0)
                        FROM transactions
                        WHERE client_id = (%s) AND date <= (%s)
                        ORDER BY date DESC
                        LIMIT 1
                    ), 0)
                FROM transactions
                WHERE client_id = (%s) AND date >= (%s) AND date <= (%s)
            ORDER BY date;
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_transactions, (client_id, since, till,
                                                     client_id, since,
                                                     client_id, since, till))
                transactions_list = cursor.fetchall()

                return transactions_list

    def delete_client(self, client_id):
        delete_client = '''
            DELETE FROM clients
            WHERE id = (%s);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_client, (client_id, ))
                print('<INFO>: Client account delete successfully')

    def set_start_state(self):
        insert_state = '''
            INSERT INTO state (state)
            VALUES (TRUE);
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_state)
                print('<INFO> app started')

    def set_stop_state(self):
        delete_state = '''
            DELETE FROM state;
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_state)
                print('<INFO> app stopped')

    def get_state(self):
        select_state = '''
            SELECT * FROM state;
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(select_state)
                if not cursor.fetchone():
                    raise AppNotStartedException()

    def clear_tables(self):
        truncate_tables = '''
            TRUNCATE state, transactions, clients;
        '''

        with self.connect as conn:
            with conn.cursor() as cursor:
                cursor.execute(truncate_tables)
