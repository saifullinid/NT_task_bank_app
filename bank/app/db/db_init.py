from psycopg2 import connect
from psycopg2.extras import execute_values
from werkzeug.security import generate_password_hash

from app.db import db_config


def db_init():
    create_clients_table_sql = '''
        CREATE TABLE clients (
            id serial NOT NULL PRIMARY KEY,
            username varchar(32) UNIQUE NOT NULL,
            password varchar(128) NOT NULL
        );
    '''
    create_transactions_table_sql = '''
        CREATE TABLE transactions (
            id serial NOT NULL PRIMARY KEY,
            date timestamp,
            description varchar(64),
            withdrawals decimal(11, 2) NOT NULL DEFAULT 0,
            deposits decimal(11, 2) NOT NULL DEFAULT 0,
            balance decimal(11, 2) DEFAULT 0 CHECK (balance >= 0),
            client_id integer NOT NULL,
            CONSTRAINT fk_tr_client_id
                FOREIGN KEY (client_id)
                REFERENCES clients (id)
                ON DELETE CASCADE
        );
    '''
    create_state_table_sql = '''
        CREATE TABLE state (
            id serial NOT NULL PRIMARY KEY,
            state boolean NOT NULL
        );
    '''

    conn = connect(dbname=db_config.DBNAME,
                   user=db_config.USER,
                   password=db_config.PASSWORD,
                   host=db_config.HOST,
                   port=db_config.PORT,)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(create_clients_table_sql)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(create_transactions_table_sql)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(create_state_table_sql)

    with conn:
        with conn.cursor() as cursor:
            execute_values(cursor,
                           '''INSERT INTO clients (username, password) VALUES %s;''',
                           [('Jack Daniels', generate_password_hash('password')),
                            ('Jameson', generate_password_hash('password')),
                            ('Jim Beam', generate_password_hash('password')),
                            ('Clan MacGregor', generate_password_hash('password')),
                            ('Black Jack', generate_password_hash('password'))])

    with conn:
        with conn.cursor() as cursor:
            execute_values(cursor,
                           '''INSERT INTO transactions 
                           (date, description, client_id) VALUES %s''',
                           [('2020-10-15 21:45:30', 'Creating account', 1),
                            ('2020-10-17 21:45:30', 'Creating account', 2),
                            ('2020-10-20 00:45:30', 'Creating account', 3),
                            ('2020-09-20 05:08:30', 'Creating account', 4),
                            ('2020-05-10 05:08:30', 'Creating account', 5)])

    conn.close()


if __name__ == '__main__':
    db_init()
