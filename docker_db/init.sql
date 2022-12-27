CREATE USER nt_task SUPERUSER PASSWORD 'mysuperpassword';
CREATE DATABASE nt_task OWNER nt_task;
GRANT ALL PRIVILEGES ON DATABASE nt_task TO nt_task;
\connect nt_task nt_task;
CREATE TABLE clients (
    id serial NOT NULL PRIMARY KEY,
    username varchar(32) UNIQUE NOT NULL,
    password varchar(128) NOT NULL
);
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
CREATE TABLE state (
    id serial NOT NULL PRIMARY KEY,
    state boolean NOT NULL
);