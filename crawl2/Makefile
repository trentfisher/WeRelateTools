
DB=wr.db

setup:
	yum install -y sqlite
	test -d venv && python3 -m venv venv
	(. venv/bin/activate; pip install requests python-dateutil)

initdb:
	sqlite3 $(DB) < schema.sql

reports: verdump.csv tot.csv user-all.csv user-month.csv
verdump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
tot.csv: tot.sql
	sqlite3 $(DB) > $@ < $<
users.csv: users.sql
	sqlite3 $(DB) > $@ < $<
%.csv: %.sql
	sqlite3 $(DB) > $@ < $<
