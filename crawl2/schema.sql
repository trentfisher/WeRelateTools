CREATE TABLE page (
       name TEXT,
       PRIMARY KEY(name)
);
CREATE TABLE vers (
       name TEXT,
       id TEXT,
       ts TIMESTAMP,
       user TEXT,
       score TEXT,
       scorever TEXT,
       PRIMARY KEY (name, id)
);
