
DB=wr.db

setup:
	sudo yum install -y sqlite
	test -d venv || python3 -m venv venv
	(. venv/bin/activate; pip install requests python-dateutil beautifulsoup4)
initdb:
	sqlite3 $(DB) < schema.sql

progress:
	echo 'select count(*) as c, (CAST(count(*) as REAL)/4377477*100) from relations' | sqlite3 $(DB)

reports:
	$(MAKE) -C reports reports

