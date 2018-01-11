DROP TABLE page;
DROP TABLE namespace;
DROP TABLE person;
DROP TABLE family;

CREATE TABLE namespace (
       id   INT NOT NULL AUTO_INCREMENT,
       name varchar(40) NOT NULL UNIQUE,
       PRIMARY KEY (id)
);
CREATE TABLE page (
       id        INT NOT NULL AUTO_INCREMENT,
       namespace INT,
       name      VARCHAR(60),
       updtm     TIMESTAMP,
       fetchtm   TIMESTAMP,
       PRIMARY KEY (id,namespace,name),
       FOREIGN KEY (namespace) REFERENCES namespace(id)
);

CREATE TABLE person (
       pageid  INT,
       surname VARCHAR(50),
       given   VARCHAR(50),
       parentfamily INT,               
       text    TEXT,
       FOREIGN KEY (pageid) REFERENCES page(id)
);

CREATE TABLE family (
       pageid  INT,
       text    TEXT,
       FOREIGN KEY (pageid) REFERENCES page(id)
);
