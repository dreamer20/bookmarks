DROP TABLE IF EXISTS bookmarks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id serial PRIMARY KEY,
    login varchar(16) UNIQUE NOT NULL CHECK (regexp_like(login, '^[a-zA-Z]\w{2,}$')),
    hashed_password text NOT NULL
);

CREATE TABLE bookmarks (
    id serial PRIMARY KEY,
    url text,
    owner_id integer REFERENCES users
);