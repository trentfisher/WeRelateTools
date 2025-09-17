
DB=../wr.db

SQLFILES=$(wildcard *.sql)
CSVFILES=$(patsubst %.sql,%.csv,$(SQLFILES))
reports: $(CSVFILES)

clean:
	rm -f $(CSVFILES)

verdump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
%.csv: %.sql
	sqlite3 $(DB) < $< > $@ || rm -f $@
