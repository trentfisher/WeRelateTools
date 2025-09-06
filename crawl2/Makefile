
DB=wr.db

setup:
	yum install -y sqlite
	test -d venv && python3 -m venv venv
	(. venv/bin/activate; pip install requests python-dateutil)

initdb:
	sqlite3 $(DB) < schema.sql

reports: verdump.csv tot.csv tot-month.sql tot-monthly.sql user-all.csv user-month.csv verify-newver.sql
verdump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
%.csv: %.sql
	sqlite3 $(DB) < $< > $@ || rm -f $@
