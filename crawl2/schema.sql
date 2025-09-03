CREATE TABLE relations (
       name             TEXT,
       child_of_family  TEXT,
       spouse_of_family TEXT,
       husband          TEXT,
       wife             TEXT,
       child            TEXT,
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
