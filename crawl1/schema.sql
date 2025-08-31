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
       name      VARCHAR(1024),
       updtm     TIMESTAMP,
       fetchtm   TIMESTAMP,
--       ts       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
       PRIMARY KEY (id,namespace,name),
       FOREIGN KEY (namespace) REFERENCES namespace(id)
);

CREATE TABLE person (
       pageid   INT,
       pagename VARCHAR(256),
       surname  VARCHAR(256),
       given    VARCHAR(256),
       text     TEXT,
       PRIMARY KEY (pagename),
       FOREIGN KEY (pageid) REFERENCES page(id)
);

CREATE TABLE family (
       id       INT NOT NULL AUTO_INCREMENT,
       pagename VARCHAR(256),
       text     TEXT,
       ts       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
