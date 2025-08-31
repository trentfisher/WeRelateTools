
DB=wr.db

initdb:
	sqlite3 wr.db < schema.sql

dump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 wr.db > dump.csv
