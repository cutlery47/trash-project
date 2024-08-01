CREATE TABLE users (
    id            integer primary key,
    role          varchar(8),
    email         varchar(64),
    password      varchar(128)
);