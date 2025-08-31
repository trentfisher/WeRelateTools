
DB=wr.db

initdb:
	sqlite3 $(DB) < schema.sql

dump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
tot.csv: tot.sql
	sqlite3 $(DB) > $@ < $<
