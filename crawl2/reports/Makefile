
DB=../wr.db

SQLFILES=$(wildcard *.sql)
CSVFILES=$(patsubst %.sql,%.csv,$(SQLFILES))

GPFILES=$(wildcard *.gnuplot)
PNGFILES=$(patsubst %.gnuplot,%.png,$(GPFILES))

reports: $(CSVFILES)
charts: $(PNGFILES)

clean:
	rm -f $(CSVFILES) $(PNGFILES)

# need this data for each chart
user-first-last.png: user-alltime.csv
user-first-len.png: user-alltime.csv

verdump.csv:
	(echo '.mode csv'; echo '.headers on'; echo 'select * from vers') | sqlite3 $(DB) > $@
%.csv: %.sql
	sqlite3 $(DB) < $< > $@ || rm -f $@
%.png: %.gnuplot
	gnuplot -e "set terminal png; set output '$@'" $<
