
DB=wr.db

setup:
	yum install -y sqlite
	test -d venv && python3 -m venv venv
	(. venv/bin/activate; pip install requests python-dateutil)

initdb:
	sqlite3 $(DB) < schema.sql

dump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
tot.csv: tot.sql
	sqlite3 $(DB) > $@ < $<
