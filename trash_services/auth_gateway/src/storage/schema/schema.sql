CREATE TABLE users (
    id            integer primary key,
    role          varchar(8),
    email         varchar(64),
    password      varchar(128),
    firstname     varchar(64),
    surname       varchar(64)
);

CREATE INDEX id_index ON users USING btree (id);
