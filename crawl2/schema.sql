CREATE TABLE page (
       name TEXT,
       PRIMARY KEY(name)
);
CREATE TABLE vers (
       name     TEXT,
       id       TEXT,
       ts       TIMESTAMP,
       user     TEXT,
       score    INTEGER,
       scorever INTEGER,
       newver   INTEGER,
       PRIMARY KEY (name, id)
);
