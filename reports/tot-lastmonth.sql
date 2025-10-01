-- .parameter init
-- .parameter set foo "bar"
-- .parameter set startdate "date('now', 'start of month', '-1 month')"
-- .parameter set enddate   "date('now', 'start of month')"
-- .parameter list
CREATE TEMP TABLE params (k TEXT, v TEXT, PRIMARY KEY(k));
INSERT INTO params VALUES ('startdate', date('now', 'start of month', '-1 month'));
INSERT INTO params VALUES ('enddate',   date('now', 'start of month'));
.read tot.sql
