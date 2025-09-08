
DB=wr.db

setup:
	yum install -y sqlite
	test -d venv && python3 -m venv venv
	(. venv/bin/activate; pip install requests python-dateutil beautifulsoup4)
initdb:
	sqlite3 $(DB) < schema.sql

progress:
	echo 'select count(*) as c, (CAST(count(*) as REAL)/4377477*100) from relations' | sqlite3 $(DB)

reports: verdump.csv tot.csv tot-month.csv tot-monthly.csv user-all.csv user-month.csv verify-newver.csv
verdump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
%.csv: %.sql
	sqlite3 $(DB) < $< > $@ || rm -f $@
